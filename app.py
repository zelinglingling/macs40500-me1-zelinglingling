from model import SugarScapeModel
from mesa.visualization import Slider, SolaraViz, make_plot_component
from mesa.visualization.components.matplotlib_components import make_mpl_space_component
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle

## Define agent portrayal (color, size, shape)
def agent_portrayal(agent):
    if agent.residency_status == "coastal" and agent.origin == "inland":
        color = "green"
    elif agent.residency_status == "coastal":
        color = "red"
    else:
        color = "blue"
    return AgentPortrayalStyle(
        color=color,
        marker="o",
        size=10,
    )

## Define map portrayal, with yellower squares having more sugar than white squares
def propertylayer_portrayal(layer):
    return PropertyLayerStyle(
        color="yellow", alpha=0.8, colorbar=True, vmin=0, vmax=4
    )

## Define model space component based on above
sugarscape_space = make_mpl_space_component(
    agent_portrayal=agent_portrayal,
    propertylayer_portrayal=propertylayer_portrayal,
    post_process=None,
    draw_grid=False,
)

## Define Gini plot
GiniPlot = make_plot_component("Gini")
WealthGapPlot = make_plot_component(["MeanInlandWealth", "MeanCoastalWealth"])
CoastalSharePlot = make_plot_component("CoastalShare")

## Define variable model parameters
model_params = {
    "seed": {"type": "InputText", "value": 42, "label": "Random Seed"},
    "width": 50,
    "height": 50,
    "initial_population": Slider("Initial Population", value=200, min=50, max=500, step=10),
    "endowment_min": Slider("Min Initial Endowment", value=25, min=5, max=30, step=1),
    "endowment_max": Slider("Max Initial Endowment", value=50, min=30, max=100, step=1),
    "metabolism_min": Slider("Min Metabolism", value=1, min=1, max=3, step=1),
    "metabolism_max": Slider("Max Metabolism", value=5, min=3, max=8, step=1),
    "vision_min": Slider("Min Vision", value=1, min=1, max=3, step=1),
    "vision_max": Slider("Max Vision", value=5, min=3, max=8, step=1),
    # MODIFICATION: institutional and mobility controls
    "coastal_share": Slider("Coastal Region Share", value=0.30, min=0.10, max=0.50, step=0.05),
    "initial_coastal_ratio": Slider("Initial Coastal Residency Ratio", value=0.25, min=0.05, max=0.50, step=0.05),
    "mobility_threshold": Slider("Mobility Wealth Threshold", value=100, min=40, max=150, step=5),
    "mobility_probability": Slider("Mobility Probability", value=0.05, min=0.00, max=0.30, step=0.01),
}

## Instantiate model
model = SugarScapeModel()

## Define all aspects of page
page = SolaraViz(
    model,
    components=[
        sugarscape_space,
        GiniPlot,
        WealthGapPlot,
        CoastalSharePlot,
    ],
    model_params=model_params,
    name="Sugarscape with Residency Restrictions",
    play_interval=150,
)
## Return page
page
