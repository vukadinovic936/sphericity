library(fastman)


gwasResults = read.table(file = 'I:/UKB_DATA/results/my_ef_same/exported_results.tsv',
                         sep='\t',
                         header=TRUE)
gwasResults = na.omit(gwasResults)
p <- fastman (gwasResults,
              chr = "chr",
              bp = "pos",
              p = "p_value",
              snp="rsid",
              ylim=c(0,17),
              cex.axis = 0.8,
              suggestiveline=FALSE,
              col = "greys",
              cex=0.6)
#width=1167
#height=627
