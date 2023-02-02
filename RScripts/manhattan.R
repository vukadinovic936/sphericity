library(qqman)

gwasResults = read.table(file=
                           'C:/Users/remote/Desktop/BOLT-LMM_v2.4/lvef_chr18_test/bolt_chr10_lvef_ukb.bgen.gz',
                         sep='\t',header=TRUE)
gwasResults = na.omit(gwasResults)
p <- manhattan(gwasResults,
          chr='CHR',
          bp='BP',
          snp='SNP',
          p='P_BOLT_LMM_INF',
          ylim=c(0,17),
          suggestiveline=F,
          cex.axis=0.8,
          col=c("#1f77b4","#ff7f03")
          )


