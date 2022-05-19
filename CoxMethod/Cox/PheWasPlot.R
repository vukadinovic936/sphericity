library(PheWAS)
library(readr)
library(tidyverse)


#icd10cm_codes=read_csv("id_icd10_count.csv", col_types="ifci")
#load(file="phecode_map_icd10.rda")
#genotypes <- read.csv('genotypes.csv',sep=',',colClasses=c("integer","integer"))
#phenotypes=createPhenotypes(icd10cm_codes)
#results=phewas(phenotypes,genotypes,cores=1,significance.threshold=c("bonferroni"))
#results_d=addPhecodeInfo(results)
#List the significant results
#sig_results <- results_d[results_d$bonferroni&!is.na(results_d$p),]
#DT::datatable(sig_results)
#phewas_plot <- phewasManhattan(results, OR.direction = T, title="My Example PheWAS Manhattan Plot", annotate.size=3)
#phewas_plot
#results <- subset(results, selec=-c(adjustment, n_no_snp))
#results


df <- read_csv("C:/Users/VukadinoviM/Documents/Beyond_Size/G_results/PheWas/BSA_lv_width/results.csv")
class(df$phecode)
names(df)[names(df) == 'phecode'] <- 'phenotype'
names(df)[names(df) == 'ccs'] <- 'beta'
names(df)[names(df) == 'p_vals'] <- 'p'
df['type']<-c(rep('logistic', nrow(df)))
df['bonferroni']<-c(rep(FALSE, nrow(df)))
df['OR'] <- exp(df['beta'])
phewas_plot <- phewasManhattan(df, OR.direction = T, title="LV Length PheWAS", annotate.size=3, significant.line = 2.6795e-5, suggestive.line=NA)
phewas_plot



