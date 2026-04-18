from pathlib import Path

import numpy as np

import mesa
from agents import SugarAgent
## Using discrete cell space for this model that enforces von Neumann neighborhoods
from mesa.discrete_space import OrthogonalVonNeumannGrid
from mesa.discrete_space.property_layer import PropertyLayer


class SugarScapeModel(mesa.Model):
    ## Helper function to calculate Gini coefficient, used in plot
    def calc_gini(self):
        agent_sugars = [a.sugar for a in self.agents]
        if len(agent_sugars) == 0:
            return 0
        if sum(agent_sugars) == 0:
            return 0
        sorted_sugars = sorted(agent_sugars)
        n = len(sorted_sugars)
        x = sum(el * (n - ind) for ind, el in enumerate(sorted_sugars)) / (n * sum(sorted_sugars))
        return 1 + (1 / n) - 2 * x

    # MODIFICATION: track inequality by residency group
    def calc_mean_inland_wealth(self):
        inland = [a.sugar for a in self.agents if a.residency_status == "inland"]
        return float(np.mean(inland)) if inland else 0.0

    def calc_mean_coastal_wealth(self):
        coastal = [a.sugar for a in self.agents if a.residency_status == "coastal"]
        return float(np.mean(coastal)) if coastal else 0.0

    def calc_coastal_share(self):
        if len(self.agents) == 0:
            return 0.0
        coastal_count = sum(1 for a in self.agents if a.residency_status == "coastal")
        return coastal_count / len(self.agents)

    def is_coastal(self, cell):
        _, y = cell.coordinate
        return y >= self.height - self.coastal_start

    ## Define initiation, inherit seed property from parent class
    def __init__(
        self,
        width=50,
        height=50,
        initial_population=200,
        endowment_min=25,
        endowment_max=50,
        metabolism_min=1,
        metabolism_max=5,
        vision_min=1,
        vision_max=5,
        # MODIFICATION: new institutional and mobility parameters
        coastal_share=0.30,
        initial_coastal_ratio=0.25,
        mobility_threshold=100,
        mobility_probability=0.05,
        seed=None,
    ):
        super().__init__(rng=seed)
        ## Instantiate model parameters
        self.width = width
        self.height = height
        ## Set model to run continuously
        self.running = True

        # MODIFICATION: define which part of the map counts as the coastal region
        self.coastal_share = coastal_share
        self.coastal_start = int(round(self.height * self.coastal_share))
        self.mobility_threshold = mobility_threshold
        self.mobility_probability = mobility_probability

        ## Create grid
        self.grid = OrthogonalVonNeumannGrid(
            (self.width, self.height), torus=False, random=self.random
        )

        ## Define datacollector, which calculates current Gini coefficient
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Gini": self.calc_gini,
                "MeanInlandWealth": self.calc_mean_inland_wealth,
                "MeanCoastalWealth": self.calc_mean_coastal_wealth,
                "CoastalShare": self.calc_coastal_share,
            },
        )

        ## Import sugar distribution from raster, define grid property
        # Note: The map initially appeared flipped in the visualization, so I transpose it here
        # This fixes a mismatch between how the array is indexed and how the grid is displayed
        self.sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map-coastal.txt").T
        self.grid.add_property_layer(
            PropertyLayer.from_data("sugar", self.sugar_distribution)
        )

        all_cells = list(self.grid.all_cells.cells)
        n_coastal = int(round(initial_population * initial_coastal_ratio))
        n_inland = initial_population - n_coastal

        coastal_cells = [cell for cell in all_cells if self.is_coastal(cell)]
        inland_cells = [cell for cell in all_cells if not self.is_coastal(cell)]

        # MODIFICATION: initial status assignment and region-specific placement
        coastal_positions = self.random.sample(coastal_cells, k=min(n_coastal, len(coastal_cells)))
        inland_positions = self.random.sample(inland_cells, k=min(n_inland, len(inland_cells)))
        positions = coastal_positions + inland_positions
        statuses = (["coastal"] * len(coastal_positions)) + (["inland"] * len(inland_positions))

        ## Create agents, give them random properties, and place them randomly on the map
        SugarAgent.create_agents(
            self,
            len(positions),
            positions,
            sugar=self.rng.integers(endowment_min, endowment_max, (len(positions),), endpoint=True),
            metabolism=self.rng.integers(metabolism_min, metabolism_max, (len(positions),), endpoint=True),
            vision=self.rng.integers(vision_min, vision_max, (len(positions),), endpoint=True),
            residency_status=statuses,
        )

        ## Initialize datacollector
        self.datacollector.collect(self)

    ## Define step: Sugar grows back at constant rate of 1, all agents move, then all agents consume, then all see if they die. Then model calculated Gini coefficient.
    def step(self):
        self.grid.sugar.data = np.minimum(self.grid.sugar.data + 1, self.sugar_distribution)
        self.agents.shuffle_do("move")
        self.agents.shuffle_do("gather_and_eat")
        # MODIFICATION: mobility happens after accumulation, before next round of movement
        self.agents.shuffle_do("try_mobility_transition")
        self.agents.shuffle_do("see_if_die")
        self.datacollector.collect(self)
