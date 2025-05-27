# Cross-Lagged Model Analysis Project

## 📋 Project Overview
This repository contains code for analyzing longitudinal relationships between depression symptoms and cardiovascular risk factors using cross-lagged modeling. The project was developed as part of bachelor's research at the University of Amsterdam.

## 🚀 Quick Start
1. Clone this repository
2. Install dependencies: `pip install -r config.txt`
3. Run preprocessing: `python src/preprocess.py`
4. Run analysis: `Rscript src/networkanalysis.R`

## 🔧 Key Files
| File | Purpose |
|------|---------|
| `preprocess.ipynb` | Cleans data & handles missing values |
| `networkanalysis.R` | Main analysis (GLMNET implementation) |
| `calculate_descriptive.ipynb` | Supplemental statistics |

## ⏳ Runtime Notes
- Analysis time depends on hardware and bootstrap iterations
- For faster plotting: 
  ```r
  coef <- build_coef()  # Run once
  set_coef(coef)        # Reuse for different plots
  
## 📊 Output Files
The analysis generates three types of output files:
- **Visualizations**: Network plots (`.png`, `.svg`)
- **Model Data**: Coefficient tables (`.csv`) 
- **Reports**: Diagnostic summaries (`.html`)

## 👥 Research Context
This project was developed through a supervised research collaboration with:
**Tycho Stam** (BSc Candidate, CSL) ([GitHub](https://github.com/kingilsildor))
*Computational Science Lab, Institute of Informatics, University of Amsterdam*
