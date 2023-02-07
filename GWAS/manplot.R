library(qqman)

gwasResults = read.table(file='exported_results.tsv',
                         sep='\t',
                         header=TRUE)
gwasResults = na.omit(gwasResults)
p <- manhattan(gwasResults,
          chr='chr',
          bp='pos',
          snp='rsid',
          p='p_value',
          ylim=c(0,17),
          suggestiveline=F,
          cex.axis=0.8,
          col=c("#1f77b4","#ff7f03"))
