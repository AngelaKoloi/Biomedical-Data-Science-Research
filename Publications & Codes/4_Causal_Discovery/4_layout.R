library(visNetwork)
library(glue)
library(igraph)
library(htmlwidgets)

load("tpc_graph005.RData")
adj_matrix <- as(graph@graph, "matrix")
g <- graph_from_adjacency_matrix(adj_matrix, mode = "directed")
nodes <- data.frame(id = V(g)$name, label = V(g)$name)
# Assuming 'adj_matrix' is your adjacency matrix
# Create an edges data frame from the adjacency matrix
edge_list <- which(adj_matrix != 0, arr.ind = TRUE)
edges <- data.frame(from = rownames(adj_matrix)[edge_list[, 1]], to = colnames(adj_matrix)[edge_list[, 2]])



# Updated labels to replace the previous column names
renamed_labels <- list(
  "MDD" = "MDD", 
  "hs.CRP" = "hs-CRP",                    # High-sensitivity C-Reactive Protein
  "CVD" = "CVD", 
  "aIL6" = "IL-6",                        # Interleukin-6
  "TNF.a" = "TNF-a",                      # Tumor Necrosis Factor-alpha
  "AGP" = "Glycoprotein",                          # Alpha-1-Acid Glycoprotein
  "ApoA1" = "ApoA1",                      # Apolipoprotein A1
  "ApoB" = "ApoB",                        # Apolipoprotein B
  "Remnant.Chol" = "Remnant Cholesterol", # Remnant Cholesterol
  "VLDL.Chol" = "VLDL Cholesterol",       # Very-Low-Density Lipoprotein Cholesterol
  "HDL.Chol" = "HDL Cholesterol",         # High-Density Lipoprotein Cholesterol
  "HDL.2.Chol" = "HDL-2 Cholesterol",     # High-Density Lipoprotein 2 Cholesterol
  "HDL.3.Chol" = "HDL-3 Cholesterol",     # High-Density Lipoprotein 3 Cholesterol
  "VLDL.Diameter" = "VLDL Diameter",      # Very-Low-Density Lipoprotein Diameter
  "HDL.Diameter" = "HDL Diameter",        # High-Density Lipoprotein Diameter
  "Diacylglycerol" = "Diacylglycerol",               # Diacylglycerol
  "Serum.Trig" = "Serum Triglycerides",   # Serum Triglycerides
  "VLDL.Trig" = "VLDL Triglycerides",     # Very-Low-Density Lipoprotein Triglycerides
  "LDL.Trig" = "LDL Triglycerides",       # Low-Density Lipoprotein Triglycerides
  "HDL.Trig" = "HDL Triglycerides",       # High-Density Lipoprotein Triglycerides
  "Monounsaturated.FAs" = "Monouns.Fatty Acids",         # Monounsaturated Fatty Acids
  "Total.FAs" = "Total Fatty Acids",                  # Total Fatty Acids
  "FAs.chain.length" = "Fatty Acids Chain Length",           # Fatty Acids Chain Length
  "aAce" = "Acetate",                      # Acetate
  "Tyrosine" = "Tyrosine",                     # Tyrosine
  "Isoleucine" = "Isoleucine"                    # Isoleucine
)





# Apply the renamed labels
nodes$label <- sapply(nodes$label, function(x) renamed_labels[[x]])



# Assign node shapes
baseline_variables <- c("AGP", "aAce",  "ApoA1", "ApoB", "Diacylglycerol",
                        "FAs.chain.length", "HDL.Chol", "HDL.Diameter", "HDL.Trig", "HDL.2.Chol",
                        "HDL.3.Chol", "aIL6", "Isoleucine", "LDL.Trig", "Monounsaturated.FAs", 
                        "Remnant.Chol", "Serum.Trig", "TNF.a", "Total.FAs", "Tyrosine", "VLDL.Chol", 
                        "VLDL.Diameter", "VLDL.Trig", "hs.CRP" )
follow_up_variables <- c(  "MDD",             
                         "CVD")
# Assign shapes based on baseline or follow-up
nodes$shape <- ifelse(nodes$id %in% baseline_variables, 'square', 'dot')




# Define custom colors
color_map <- list(
  'MDD' = '#2667FF',
  'Metabolites' = '#FF6347',
  'CVD' = '#90EE90', 
  'Inflammation' = '#FFD700'
  
)




variable_groups <- list(
  'MDD' = c('MDD'),
  'Metabolites' = c(
                     'Glycoprotein',
                     'ApoA1',
                     'ApoB',
                     'Remnant Cholesterol',
                     'VLDL Cholesterol',
                     'HDL Cholesterol',
                     'HDL-2 Cholesterol',
                     'HDL-3 Cholesterol',
                     'VLDL Diameter',
                     'HDL Diameter',
                     'Diacylglycerol',
                     'Serum Triglycerides',
                     'VLDL Triglycerides',
                     'LDL Triglycerides',
                     'HDL Triglycerides',
                     'MUFA',
                     'TotFA',
                     'FALen',
                     'Ace',
                     'Tyr',
                     'Ile'),
  
  'Inflammation' = c('hs-CRP',
                     'IL-6',
                     'TNF-a'),
  
  'CVD' = c('CVD')
)

# Assign colors
nodes$color <- sapply(nodes$label, function(x) {
  group <- sapply(variable_groups, function(v) !is.null(v) && x %in% v)
  if (any(group, na.rm = TRUE)) {
    return(color_map[[names(variable_groups)[which(group)[1]]]])
  } else {
    return('#FF6347')  # Default color if no group matches
  }
})

assign_custom_positions <- function(nodes, baseline_vars, follow_up_vars) {
  # Initialize positions with default NA
  positions <- data.frame(id = nodes$id, x = NA, y = NA, stringsAsFactors = FALSE)
  
  # Define layout parameters
  left_x <- -400  # Position on the left for MDD and CVD
  middle_x <- 0
  grid_spacing <- 150
  grid_cols <- 4  # Number of columns in the grid
  current_y <- 0
  
  # Explicitly place 'MDD' and 'CVD' on the left
  positions[positions$id == "MDD", ] <- list("MDD", - 500, current_y -400)
  positions[positions$id == "CVD", ] <- list("CVD",400, current_y - 400)
  
  # Arrange baseline variables in a grid at the center
  for (i in seq_along(baseline_vars)) {
    row <- (i - 1) %/% grid_cols  # Row index
    col <- (i - 1) %% grid_cols   # Column index
    x_pos <- middle_x + (col - grid_cols / 2) * grid_spacing
    y_pos <- current_y - (row * grid_spacing)
    positions[positions$id == baseline_vars[i], c("x", "y")] <- list(x_pos, y_pos)
  }
  

  # Ensure all positions are assigned
  if (any(is.na(positions$x) | is.na(positions$y))) {
    warning("Some nodes do not have assigned positions!")
  }
  
  return(positions)
}

# Custom positioning of nodes
positions <- assign_custom_positions(nodes, baseline_variables, follow_up_variables)
nodes <- merge(nodes, positions, by = "id", all.x = TRUE)


# Create and display the network visualization
net <- visNetwork(nodes, edges) %>%
  visEdges(arrows = 'to') %>%
  visOptions(highlightNearest = TRUE, nodesIdSelection = TRUE) %>%
  visPhysics(stabilization = FALSE) %>%
  visNodes(fixed = TRUE)

# Display the network
print(net)


#saveWidget(net, file = "network005.html", selfcontained = TRUE)

