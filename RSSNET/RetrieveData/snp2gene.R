library(postgwas)
vignette(postgwas)
#(file = "C:/Users/VukadinoviM/Documents/Beyond_Size/results/GWAS/hw_gwas/exported_results.tsv", 
#           sep = '\t',
#           header = TRUE)
snps <- data.frame(SNP = c("rs172154", "rs759704"))
annot.prox <- snp2gene.prox(snps)