#remove.packages(pkgs, lib) 
#library(devtools)
#install_github("vukadinovic936/fastman")


colors <-c("blue", "orange", "green", "red", "purple",
           "brown", "pink", "gray", "darkolivegreen", "cyan4", "black")

cols <- c("#41354d", "#78416d", "#b53b73","#d23d69", "#e67d62","#f7b795")

#cols <- c( rgb(0.20973515, 0.09747934, 0.24238489),
#            rgb(0.43860848, 0.12177004, 0.34119475),
#            rgb(0.67824099, 0.09192342, 0.3504148),
#            rgb(0.8833417, 0.19830556, 0.26014181),
#            rgb(0.95381595, 0.46373781, 0.31769923),
#            rgb(0.96516917, 0.70776351, 0.5606593))
## READ BAELINE
print(cols)
gwasResults = read.table(file = "I:/UKB_DATA/results/lv_ef_UKB/exported_results.tsv" ,
                         sep = '\t', 
                         header = TRUE)
gwasResults = na.omit(gwasResults)
myfastqq(gwasResults$p_value, col=cols[1], ylim=c(0,14),xlim=c(0,14),baseline=TRUE)
cnt=2
for (x in seq(2, 10, by=2)) {
  print(x)
  gwasResults = read.table(file = paste(paste("I:/UKB_DATA/results/lv_ef_n_sd",x,sep=""),"/exported_results.tsv",sep=""), 
                           sep = '\t', 
                           header = TRUE)
  gwasResults = na.omit(gwasResults)
  
  myfastqq(gwasResults$p_value, col=cols[cnt], ylim=c(0,14), xlim=c(0,14), baseline=FALSE)
  cnt <- cnt+1
}
legend( x="topleft", legend=c("Baseline", "SD 2", "SD 4", "SD 6", "SD 8", "SD 10"),
       col=cols, lty=c(1,1,1,1,1,1), cex=0.8)

