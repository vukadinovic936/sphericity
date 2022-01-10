# code obtained from https://support.bioconductor.org/p/124462/#124464 
library(ensembldb)
library(AnnotationHub)
library(dplyr)


hub = AnnotationHub()
query(hub, c("EnsDb", "Homo sapiens", "97"))
edb = hub[["AH73881"]]
keytypes(edb)
columns(edb)
keys = keys(edb, "GENENAME")
columns =  c("GENEID", "ENTREZID", "GENEBIOTYPE", "GENESEQSTART", "GENESEQEND")
tbl =
  ensembldb::select(edb, keys, columns, keytype = "GENENAME") %>%
  as_tibble()
tbl
supportedFilters()
filter = ~ gene_name %in% keys & gene_biotype == "protein_coding"
tbl =
  ensembldb::select(edb, filter, columns) %>%
  as_tibble()
tbl
write.csv(tbl,"gene_names.csv", row.names=FALSE)

ensembldb::listColumns(edb)
