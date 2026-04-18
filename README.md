# macs40500-me1-zelinglingling

## Project Overview

This project extends the classic Sugarscape model by introducing a spatial and institutional modification to study inequality in resource access. It combines a coastal–inland resource gradient with a hukou-like residency restriction to examine how structural constraints shape agent mobility and long-term outcomes.

## Model Modification

Two main changes are introduced:

### Spatial Resource Gradient
Resources are unevenly distributed across the grid:
- Higher sugar levels at the edges (coastal regions)
- Lower sugar levels toward the center (inland regions)
- A smooth gradient with noise creates more realistic variation

### Residency Restriction
Agents are assigned a residency status:
- Coastal agents can move freely
- Inland agents cannot enter coastal regions

To allow limited mobility, inland agents have a one-time probabilistic chance to transition into coastal status.

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

