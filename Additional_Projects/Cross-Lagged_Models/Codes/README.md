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
**Collaborators:**  
- **Tycho Stam**  
  ‣ BSc Candidate in Computational Science  
  ‣ GitHub: [kingilsildor](https://github.com/kingilsildor)  

*This work was conducted at the Computational Science Lab (CSL) as part of supervised bachelor's research.*
