import math
## Using experimental agent type with native "cell" property that saves its current position in cellular grid
from mesa.discrete_space import CellAgent

## Helper function to get distance between two cells
def get_distance(cell_1, cell_2):
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)


class SugarAgent(CellAgent):
    def __init__(
        self,
        model,
        cell,
        sugar=0,
        metabolism=0,
        vision=0,
        residency_status="inland",
    ):
        super().__init__(model)
        self.cell = cell
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        # MODIFICATION: hukou-like status that determines access to coastal cells
        self.residency_status = residency_status
        self.origin = residency_status

    ## Define movement action
    def move(self):
        ## Determine currently empty cells within line of sight
        possibles = [
            cell
            for cell in self.cell.get_neighborhood(self.vision, include_center=False)
            if cell.is_empty
        ]
        possibles.append(self.cell)

        # MODIFICATION: inland agents cannot move into coastal cells
        if self.residency_status == "inland":
            possibles = [cell for cell in possibles if not self.model.is_coastal(cell)]

        # Failsafe: if filtering removes all targets, stay in place.
        if not possibles:
            return

        ## Score each possible target
        def cell_score(cell):
            return cell.sugar

        scores = [cell_score(cell) for cell in possibles]
        max_score = max(scores)

        candidates = [
            possibles[i]
            for i in range(len(possibles))
            if math.isclose(scores[i], max_score, rel_tol=1e-06)
        ]

        min_dist = min(get_distance(self.cell, cell) for cell in candidates)
        final_candidates = [
            cell
            for cell in candidates
            if math.isclose(get_distance(self.cell, cell), min_dist, rel_tol=1e-02)
        ]

        self.cell = self.random.choice(final_candidates)

    ## consumer sugar in current cell, depleting it, then consumer metabolism
    def gather_and_eat(self):
        self.sugar += self.cell.sugar
        self.cell.sugar = 0
        self.sugar -= self.metabolism

    # MODIFICATION: conditional upward mobility into coastal residency
    def try_mobility_transition(self):
        if (
            self.residency_status == "inland"
            and self.sugar >= self.model.mobility_threshold
        ):
            if self.random.random() < self.model.mobility_probability:
                self.residency_status = "coastal"
                coastal_cells = [
                    c for c in self.model.grid.all_cells.cells
                    if self.model.is_coastal(c) and c.is_empty
                ]
                if coastal_cells:
                    self.cell = self.random.choice(coastal_cells)

    ## If an agent has zero or negative sugar, it dies and is removed from the model
    def see_if_die(self):
        if self.sugar <= 0:
            self.remove()
