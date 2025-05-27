
# Load necessary libraries
library(stats)
library(pcalg)
library(tpc)
library(micd)
library(parallel)

data <- read.csv("currentMDD.csv")

column_names <- colnames(data)

# Wrap column names in quotes and print as a comma-separated string
quoted_column_names <- paste0('"', column_names, '"')
cat(paste(quoted_column_names, collapse = ", "))



tier1 <- c( "MDD",  "AGP",  "ApoA1", "ApoB", "Diacylglycerol","aAce", "aIL6",
              "FAs.chain.length", "HDL.Chol", "HDL.Diameter", "HDL.Trig", "HDL.2.Chol",
              "HDL.3.Chol", "Isoleucine", "LDL.Trig", "Monounsaturated.FAs", 
              "Remnant.Chol", "Serum.Trig", "TNF.a", "Total.FAs", "Tyrosine", "VLDL.Chol", 
              "VLDL.Diameter", "VLDL.Trig", "hs.CRP")

tier2 <- c(   "CVD" )   



tiered_variables <- c(tier1, tier2)
data <- data[, tiered_variables]

# Create the tiers vector based on the reordered data
tiers <- c(rep(1, length(tier1)), rep(2, length(tier2)))
print(tiers)



# Prepare forbidden edges
forbEdges <- matrix(FALSE, ncol = length(colnames(data)), nrow = length(colnames(data)),
                    dimnames = list(colnames(data), colnames(data)))

# Populate the forbidden edges matrix so that MDD cannot cause Heart Condition
if ("MDD" %in% colnames(data) && "CVD" %in% colnames(data)) {
  forbEdges["MDD", "CVD"] <- TRUE
}

# Populate the forbidden edges matrix so that cvd cannot cause mdd
if ("CVD" %in% colnames(data) && "MDD" %in% colnames(data)) {
  forbEdges["CVD", "MDD"] <- TRUE
}


# Ensure MDD can be influenced by all variables by keeping MDD column FALSE (no forbidden edges to MDD)
forbEdges[, "MDD"] <- TRUE

# Check the forbidden edges matrix
print(forbEdges)




# Loop through all variables in tier1 and forbid edges from "MDD" to these variables
for (var in tier1) {
  if (var %in% colnames(data)) {
    forbEdges["MDD", var] <- FALSE  # Forbid MDD from causing each variable in tier1
  }
}

# Ensure MDD can still be influenced by all variables in tier1 by keeping the reverse edges FALSE
forbEdges[tier1, "MDD"] <- TRUE

forbEdges[tier2, "MDD"] <- TRUE

# Loop through all variables in tier 2, except eheart05, and forbid edges from eheart05 to those variables
#for (var2 in tier2) {
 # if (var2 != "Heart.Condition" && "Heart.Condition" %in% colnames(data) && var2 %in% colnames(data)) {
   # forbEdges[var2, "Heart.Condition"] <- FALSE  # Allow other variables in tier 2 to cause eheart05
   # forbEdges["Heart.Condition", var2] <- TRUE   # Forbid eheart05 from causing any other variable in tier 2
  #}
#}

suff.all <- getSuff(data, test = "gaussCItest")
str(suff.all)
is.list(suff.all)
?tpc
graph <- tpc(
  suffStat = suff.all,
  indepTest = gaussCItest,
  skel.method = "stable.parallel",
  labels = as.character(colnames(data)),
  alpha = 0.05,
  tiers = tiers,
  forbEdges = forbEdges,
  numCores = detectCores()-1,
  verbose = FALSE
)

save(graph, file = "tpc_graph0075.RData")
