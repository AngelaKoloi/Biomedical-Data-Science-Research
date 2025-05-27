# 🫀 AI-Powered Coronary Artery Disease Prediction

[![DOI](https://img.shields.io/badge/DOI-10.1093%2Fehjdh%2Fztae049-blue)](https://doi.org/10.1093/ehjdh/ztae049)  
**Machine learning pipeline for early CAD detection using routine biomarkers and synthetic data augmentation**  
📄 *Published in* ***European Heart Journal – Digital Health***

---

## 🧪 Scientific Approach

### 1. Synthetic Patient Generation  
📓 `synthetic_data_generation.ipynb`

Utilizes advanced generative modeling techniques to create high-fidelity virtual patients:
- Gaussian Copula distributions  
- Conditional GANs (cGANs)  
- Variational Autoencoders (VAEs)

---

### 2. Augmented Machine Learning  
📓 `ML_model.ipynb`

Implements robust, interpretable ML models with:
- Gradient Boosting and Random Forest classifiers  
- SHAP-based feature importance analysis  
- Stratified cross-validation for performance reliability

---

## 🚀 Quick Start

```bash
# Step 1: Generate synthetic cohort
jupyter notebook synthetic_data_generation.ipynb

# Step 2: Train prediction models
jupyter notebook ML_model.ipynb
