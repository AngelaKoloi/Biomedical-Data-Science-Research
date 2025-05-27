# MDD-CVD Causal Network Analysis

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.bpsgos.2025.100528-blue)](https://doi.org/10.1016/j.bpsgos.2025.100528)

## 🔍 Analysis Pipeline

### 1. Feature Selection (Machine Learning & Expert Input)
- **Objective**: Identify key omics biomarkers predictive of MDD
- **Output**: Reduced biomarker set for causal analysis

### 2. Main Causal Discovery Analysis
| File | Analysis Type | Key Functionality |
|------|--------------|-------------------|
| [`1_tpc_causal_discovery.R`](1_tpc_causal_discovery.R) | Tiered PC Algorithm | • Temporal tier constraints<br>• Directed acyclic graph construction |
| [`2_tpc_bootstrap.R`](2_tpc_bootstrap.R) | Stability Validation | • 100-iteration bootstrap<br>• Edge consistency testing |
| [`3_centrality.R`](3_centrality.R) | Network Metrics | • Betweenness centrality<br>• Pathway importance ranking |
| [`4_layout.R`](4_layout.R) | Interactive Visualization | • Custom node positioning<br>• Dynamic network exploration |
| [`helper.R`](helper.R) | Connection Analysis | • Edge frequency quantification<br>• Statistical validation |

## 🚀 Quick Start
```bash
# Install dependencies
install.packages(c("tpc", "pcalg", "visNetwork", "ggplot2"))

# Run full pipeline
Rscript 1_tpc_causal_discovery.R  # Causal discovery
Rscript 2_tpc_bootstrap.R        # Stability analysis
Rscript 3_centrality.R           # Network metrics
Rscript 4_layout.R               # Visualization
