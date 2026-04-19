# macs40500-me1-zelinglingling

## Project Overview

This project extends the classic Sugarscape model by introducing a spatial and institutional modification to study inequality in resource access. It combines a coastal–inland resource gradient with a hukou-like residency restriction to examine how structural constraints shape agent mobility and long-term outcomes.

## Model Modification

Two main changes are introduced:

### Spatial Resource Gradient
Resources are distributed unevenly across the grid, creating a structured environmental inequality. Sugar levels are highest in coastal regions and gradually decrease toward inland areas. This spatial gradient is designed to mimic real-world geographic disparities in resource availability.s

### Residency Restriction
Agents are assigned a residency status that constrains their mobility. Coastal agents can move freely across the grid, while inland agents are restricted from entering coastal regions.

To incorporate a limited pathway for upward mobility, inland agents are allowed a probabilistic transition to coastal status once they accumulate sufficient wealth. This mechanism captures the possibility of status change while preserving structural constraints.

## File Structure

```text
.
├── agents.py              # Defines agent behavior and decision rules
├── model.py               # Core Sugarscape model with modifications
├── app.py                 # Solara visualization interface
├── make_map.py            # Script to generate spatial sugar distribution
├── sugar-map-coastal.txt  # Pre-generated resource map
└── README.md
```

## Statement of External Tools and Resources

This project was primarily completed using course materials. AI tools (e.g., ChatGPT) were used for limited technical support, including debugging, generating the spatial sugar map, and correcting issues related to map visualization orientation.

