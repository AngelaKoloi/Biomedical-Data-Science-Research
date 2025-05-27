# MDD-CVD Metabolic Pathways Analysis

**DOI:** [10.1093/ehjopen/oeaf038](https://doi.org/10.1093/ehjopen/oeaf038)

## 🔍 Analysis Pipeline

### 1. Network Construction (Young Finns Study)
**Objective:** Identify metabolites bridging depression symptoms and CVD risk  
**Output:** Mixed Graphical Model (MGM) with stable edges

| File | Analysis Type | Key Functionality |
|------|--------------|------------------|
| `1_preprocess.ipynb` | Data Preparation | • Missing data imputation<br>• Covariate adjustment |
| `2_network_model.R` | Mixed Graphical Model | • Multi-layer network inference<br>• Edge stability testing |
| `3_postprocess.ipynb` | Network Validation | • Bootstrap stability checks<br>• Jointness score calculation |

### 2. External Validation (UK Biobank)

| File | Analysis Type | Key Functionality |
|------|--------------|------------------|
| `UKB_validation.R` | Covariate Testing | • Age/sex/smoking adjustment<br>• PHQ-9 symptom associations |

### 3. Causal Inference (Mendelian Randomization)

| File | Analysis Type | Key Functionality |
|------|--------------|------------------|
| `MR_analysis.R` | Two-Sample MR | • IVW/Wald ratio methods<br>• Pleiotropy-robust sensitivity tests |

## 🚀 Quick Start

```bash
# Install dependencies (R)
install.packages(c("mgm", "qgraph", "TwoSampleMR", "ggplot2"))

# Run pipeline
Rscript 2_network_model.R              # Main network analysis
Rscript MR_analysis.R --exposure metabolite --outcome CAD  # MR
