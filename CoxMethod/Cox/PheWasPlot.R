#!/usr/bin/env Rscript

# Usage : Type in the terminal Rscript PheWasPlot.R --vanilla {insert_phenotype_name}
# Example : Rscript PheWasPlot.R --vanilla sphericity_index

library(PheWAS)
library(readr)
library(tidyverse)

args = commandArgs(trailingOnly=TRUE)
#set a placeholder
phenotype_name="lvesv"
# test if there is at least one argument: if not, return an error
if (length(args)==0) {
	  stop("Exactly one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
	  # default output file
	  phenotype_name=args[1]
}else{
	stop("Exactly one argument must be supplied (input file).n", call.=FALSE)
}

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

out_path = paste("I:/UKB_DATA/results/PheWas_", phenotype_name, sep="")
print(out_path)
df <- read_csv(paste(out_path, "/results.csv", sep=""))
class(df$phecode)
names(df)[names(df) == 'phecode'] <- 'phenotype'
names(df)[names(df) == 'ccs'] <- 'beta'
names(df)[names(df) == 'p_vals'] <- 'p'
df['type']<-c(rep('logistic', nrow(df)))
df['bonferroni']<-c(rep(FALSE, nrow(df)))
df['OR'] <- exp(df['beta'])
dev.size("px")
png(file=paste(out_path, "/RplotPheWas.png", sep=""), width=1024, height=600)
phewas_plot <- phewasManhattan(df, OR.direction = T, title=paste(phenotype_name,"PheWAS"), annotate.size=3, significant.line = 2.6795e-5, suggestive.line=NA)
phewas_plot
dev.off()
pdf(file= paste(out_path,"/RplotPheWas.pdf", sep=""), width=16, height=9)
phewas_plot
dev.off()



