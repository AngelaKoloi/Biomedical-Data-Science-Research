# Metabolomic Signatures Linking Depressive Symptoms to Atherosclerotic CVD: UK Biobank Network & Mediation Analysis

[![Paper Status](https://img.shields.io/badge/Status-Submitted-yellow)](https://doi.org/your-doi-here)

## 🔬 Study Overview
Tripartite network and mediation analysis identifying metabolomic pathways connecting specific depressive symptoms (PHQ-9) to incident cardiovascular disease in UK Biobank participants (N=35,711).

**Key Findings:**
- 4 significant symptom-metabolite-CVD pathways surviving full covariate adjustment
- Alpha-1-glycoprotein acetyls (AGP) mediates appetite-fatigue-CVD links
- Monounsaturated fatty acids (MUFAs) mediate appetite-sleep-CVD pathways

## 📂 Analysis Pipeline

### Stage 1: Data Preparation
| File | Purpose | Key Features |
|------|---------|--------------|
| [`cleaning_NMR_UKB.ipynb`](cleaning_NMR_UKB.ipynb) | NMR metabolomics processing | • Outlier handling<br>• Batch effect correction<br>• Metabolite normalization |
| [`cleaning_merge_data.ipynb`](cleaning_merge_data.ipynb) | Dataset integration | • PHQ-9 symptom merging<br>• CVD case definition (ICD-10)<br>• Covariate harmonization |

### Stage 2: Core Analyses
| File | Analysis Type | Key Functionality |
|------|--------------|------------------|
| [`network-analysis-tripartite.ipynb`](network-analysis-tripartite.ipynb) | Tripartite Network | • Partial correlation networks<br>• Symptom-metabolite-CVD edge detection<br>• Bootstrap stability validation |
| [`mediation.ipynb`](mediation.ipynb) | Longitudinal Mediation | • 6-year incident CVD analysis<br>• 3-tier covariate adjustment:<br>  &nbsp;&nbsp;1. Age/sex<br>  &nbsp;&nbsp;2. SES/lifestyle/meds<br>  &nbsp;&nbsp;3. BMI<br>• FDR-corrected p-values |

## 🚀 Quick Start

### 1. Set Up Python Environment
```bash
# Create conda environment (recommended)
conda create -n ukb_metab python=3.11
conda activate ukb_metab

# Install core packages
pip install jupyter pandas numpy scipy statsmodels seaborn matplotlib networkx
pip install pingouin pymer4

