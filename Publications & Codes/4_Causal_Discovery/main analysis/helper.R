library(igraph)
library(glue)

# Function to convert graph to igraph format
convert_to_igraph <- function(graph) {
  if (inherits(graph, "pcAlgo")) {
    graph <- graph@graph
  }
  igraph_graph <- igraph::igraph.from.graphNEL(graph)
  return(igraph_graph)
}

# Function to calculate frequencies of connections (direct or indirect) between two nodes
calculate_connection_frequencies <- function(original_graph, bootstrap_graphs, node_a, node_b) {
  path_string <- paste(node_a, "->", node_b)
  
  # Initialize a counter for the connection
  connection_count <- 0
  
  # Iterate over all bootstrap graphs
  for (g in bootstrap_graphs) {
    g_igraph <- convert_to_igraph(g)
    if (node_a %in% V(g_igraph)$name && node_b %in% V(g_igraph)$name) {
      # Check if there is a path (direct or indirect) between the nodes
      if (length(all_simple_paths(g_igraph, from = node_a, to = node_b)) > 0) {
        connection_count <- connection_count + 1
      }
    }
  }
  
  # Calculate percentage (divide by total number of graphs)
  total_graphs <- length(bootstrap_graphs)
  connection_percentage <- (connection_count / total_graphs) * 100
  
  # Create a result data frame
  result <- data.frame(
    Path = path_string,
    Count = connection_count,
    Percentage = connection_percentage
  )
  
  return(result)
}

# Load the graphs
load("tpc_graph0075.RData")
original_graph <- graph
load("bootstrap_tpc.RData")
graphs_0 <- results_0
load("bootstrap_tpc_10.RData")
graphs_10 <- results_10
load("bootstrap_tpc_20.RData")
graphs_20 <- results_20
all_graphs <- c(graphs_0, graphs_10, graphs_20)

# Convert the original graph to igraph format
original_igraph <- convert_to_igraph(original_graph)

# Set node names
node_a_list <- c("LDL.Trig")
node_b <- "CVD"

# Loop through each source node and calculate connection frequencies
all_results <- list()
for (node_a in node_a_list) {
  cat(glue("\nCalculating connection (direct or indirect) from {node_a} to {node_b}...\n"))
  
  # Calculate connection frequencies
  connection_frequencies <- calculate_connection_frequencies(original_igraph, all_graphs, node_a, node_b)
  
  # Store the result
  all_results[[node_a]] <- connection_frequencies
  
  # Print the result
  if (nrow(connection_frequencies) > 0) {
    cat(glue("Connection Frequencies for {node_a} -> {node_b}:\n"))
    print(connection_frequencies)
  }
}

# Combine all results into a single data frame
combined_results <- do.call(rbind, all_results)

# Print combined results
cat("\nCombined Results:\n")
print(combined_results)

