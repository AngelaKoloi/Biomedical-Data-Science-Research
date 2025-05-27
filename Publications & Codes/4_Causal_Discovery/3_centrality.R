# Load required libraries
library(igraph)
library(ggplot2)
library(reshape2)

# Load the data
load("tpc_graph005.RData")
adj_matrix <- as(graph@graph, "matrix")
g <- graph_from_adjacency_matrix(adj_matrix, mode = "directed")



# Define the mapping for renaming
rename_mapping <- list(
  "hs.CRP" = "hs-CRP",
  "aIL6" = "IL-6",
  "TNF.a" = "TNF-a",
  "AGP" = "Glycoprotein",
  "ApoA1" = "ApoA1",
  "ApoB" = "ApoB",
  "Remnant.Chol" = "Remnant Cholesterol",
  "VLDL.Chol" = "VLDL Cholesterol",
  "HDL.Chol" = "HDL Cholesterol",
  "HDL.2.Chol" = "HDL-2 Cholesterol",
  "HDL.3.Chol" = "HDL-3 Cholesterol",
  "VLDL.Diameter" = "VLDL Diameter",
  "HDL.Diameter" = "HDL Diameter",
  "Diacylglycerol" = "Diacylglycerol",
  "Serum.Trig" = "Serum Triglycerides",
  "VLDL.Trig" = "VLDL Triglycerides",
  "LDL.Trig" = "LDL Triglycerides",
  "HDL.Trig" = "HDL Triglycerides",
  "Monounsaturated.FAs" = "Monouns. Fatty Acids",
  "Total.FAs" = "Total Fatty Acids",
  "FAs.chain.length" = "Fatty Acids Chain Length",
  "aAce" = "Acetate",
  "Tyrosine" = "Tyrosine",
  "Isoleucine" = "Isoleucine"
)

# Rename the nodes
V(g)$name <- sapply(V(g)$name, function(node_name) {
  if (node_name %in% names(rename_mapping)) {
    rename_mapping[[node_name]]
  } else {
    node_name
  }
})

# Load required libraries
library(igraph)
library(ggplot2)
library(reshape2)
library(scales)


# Define the variables of interest
variables_of_interest <- c("Isoleucine", "Glycoprotein", "Fatty Acids Chain Length", "Acetate", 
                           "Tyrosine", "HDL Diameter", "TNF-a", "LDL Triglycerides", "IL-6", 'hs-CRP')


# Calculate Betweenness Centrality for the entire graph
betweenness_centrality <- betweenness(g, directed = TRUE)



# Combine Betweenness Centrality into a data frame
centrality_df <- data.frame(
  Node = V(g)$name,
  Betweenness = betweenness_centrality
)

# Filter the centrality data frame to include only the variables of interest
centrality_df <- centrality_df[centrality_df$Node %in% variables_of_interest, ]

# Sort the data frame by Betweenness in descending order
centrality_df <- centrality_df[order(-centrality_df$Betweenness), ]

# Create a factor for Node to preserve the order
centrality_df$Node <- factor(centrality_df$Node, levels = centrality_df$Node)

# Calculate the mean Betweenness as the threshold
threshold <- mean(centrality_df$Betweenness)

# Create the plot
ggplot(centrality_df, aes(x = Node, y = Betweenness, fill = Betweenness > threshold)) +
  geom_bar(stat = "identity", width = 0.7) +
  geom_hline(yintercept = threshold, linetype = "dashed", color = "red", size = 0.5) +
  scale_fill_manual(values = c("#CCCCCC", "#3366CC"), 
                    labels = c("Below Average", "Above Average"),
                    name = "Betweenness Centrality") +
  scale_y_continuous(labels = comma_format(big.mark = ",", decimal.mark = ".")) +
  coord_flip() +
  labs(
   # title = "Betweenness Centrality of Selected Nodes in Metabolic Network",
   # subtitle = "Dashed line represents the mean Betweenness Centrality",
    x = NULL,
    y = "Betweenness Centrality"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14, margin = margin(b = 10)),
    plot.subtitle = element_text(size = 10, color = "darkgray", margin = margin(b = 20)),
    axis.text.y = element_text(size = 10),
    axis.text.x = element_text(size = 8),
    axis.title.x = element_text(margin = margin(t = 10)),
    legend.position = "bottom",
    legend.title = element_text(size = 10),
    legend.text = element_text(size = 8),
    panel.grid.major.y = element_blank(),
    panel.grid.minor.x = element_blank()
  )

ggsave("betweenness_centrality_graph.png", width = 10, height = 6, dpi = 600)

