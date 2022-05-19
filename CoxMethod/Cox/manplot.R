library(qqman)

gwasResults = read.table(file = 'C:/Users/VukadinoviM/Documents/Beyond_Size/results/GWAS/si_final/exported_results.tsv', sep = '\t', header = TRUE)
gwasResults = na.omit(gwasResults)
manhattan(gwasResults, chr="chr", bp="pos",snp = 'rsid', p="p_value" )

#library(manhattanly)
#manhattanly(gwasResults, chr="chr", bp="pos",snp = 'rsid', p="p_value" )
