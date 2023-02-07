#!/usr/bin/Rscript
## fam_sqc_merge.R

## Arguments to read in:

# Rscript fam_sqc_merge.R \
# [UKBB qc file] \
# [UKBB header file] \
# [application specific .fam file] \
# [output file name]

## Example usage:

# Rscript fam_sqc_merge.R \
# ukb_sqc_v2.txt \
# ukb_sqc_v2_header.txt \
# ukb1859_cal_chr22_v2_s488374.fam \
# ukb1859_qc.txt
# args <- commandArgs(TRUE)
#hdr_file <- args[2]
#rm(list = ls())
# no need for fam files we have eid
sqc_file <- "/mnt/i/UKB_DATA/main_df/ukb47972.csv"
#fam_file <- "UK_Biobank_GWAS/imputed-v2-gwas/ukb22418_c5_b0_v2_s488221.fam"
out_file <- "/mnt/i/UKB_DATA/imputed_UKB/qc.tsv"

# join by ID and rename columns
library(data.table)
sqc <- fread(sqc_file,stringsAsFactors=F)
sqc <- data.frame(sqc)
colnames(sqc)

hd <- c("eid","batch",
"Inferred.Gender",
"heterozygosity",
"heterozygosity_pca",
"missingness",
"ethnicity",
"plate",
"well",
"PC1",
"PC2",
"PC3",
"PC4",
"PC5",
"PC6",
"PC7",
"PC8",
"PC9",
"PC10",
"PC11",
"PC12",
"PC13",
"PC14",
"PC15",
"PC16",
"PC17",
"PC18",
"PC19",
"PC20",
"PC21",
"PC22",
"PC23",
"PC24",
"PC25" ,
"PC26" ,
"PC27" ,
"PC28" ,
"PC29" ,
"PC30" ,
"PC31" ,
"PC32" ,
"PC33" ,
"PC34" ,
"PC35" ,
"PC36" ,
"PC37" ,
"PC38" ,
"PC39" ,
"PC40" ,
"putative.sex.chromosome.aneuploidy",
"used.in.pca.calculation"           ,
"excess.relatives"                  ,
"inference_x"                       ,
"inference_y"                       ,
"dna_con"                           ,
"qc_CR"                             ,
"qc_QD"                             ,
"outliers"                          ,
"used_in_phasing"                   ,
"used_in_phasing_x"                 ,
"using_in_phasing_xy"               ,
"some_field"                        )

names(sqc) <- hd
colnames(sqc)
write.table(sqc,out_file,col=T,row=F,quo=F,sep='\t')



#"eid" - "eid"
#"X22000.0.0" - batch
#"X22001.0.0" - Inferred.Gender
#"X22003.0.0" - heterozygosity
#"X22004.0.0" - heterozygosity_pca 
#"X22005.0.0" - missingness
#"X22006.0.0" - ethnicity
#"X22007.0.0" - plate
#"X22008.0.0" - well
#"X22009.0.1" - PC1
#"X22009.0.2" - PC2
#"X22009.0.3" - PC3
#"X22009.0.4" - PC4
#"X22009.0.5" - PC5
#"X22009.0.6" - PC6
#"X22009.0.7" - PC7
#"X22009.0.8" - PC8
#"X22009.0.9" - PC9
#"X22009.0.10" - PC10
#"X22009.0.11" - PC11
#"X22009.0.12" - PC12
#"X22009.0.13" - PC13
#"X22009.0.14" - PC14
#"X22009.0.15" - PC15
#"X22009.0.16" - PC16
#"X22009.0.17" - PC17
#"X22009.0.18" - PC18
#"X22009.0.19" - PC19
#"X22009.0.20" - PC20
#"X22009.0.21" - PC21
#"X22009.0.22" - PC22
#"X22009.0.23" - PC23
#"X22009.0.24" - PC24
#"X22009.0.25" - PC25
#"X22009.0.26" - PC26
#"X22009.0.27" - PC27
#"X22009.0.28" - PC28
#"X22009.0.29" - PC29
#"X22009.0.30" - PC30
#"X22009.0.31" - PC31
#"X22009.0.32" - PC32
#"X22009.0.33" - PC33
#"X22009.0.34" - PC34
#"X22009.0.35" - PC35
#"X22009.0.36" - PC36
#"X22009.0.37" - PC37
#"X22009.0.38" - PC38
#"X22009.0.39" - PC39
#"X22009.0.40" - PC40
#"X22019.0.0" - putative.sex.chromosome.aneuploidy
#"X22020.0.0" - used.in.pca.calculation
#"X22021.0.0" - excess.relatives 
#"X22022.0.0" - inference_x
#"X22023.0.0" - inference_y
#"X22024.0.0" - dna_con
#"X22025.0.0" - qc_CR
#"X22026.0.0" - qc_QD
#"X22027.0.0" - outliers
#"X22028.0.0" - used_in_phasing
#"X22029.0.0" - used_in_phasing_x
#"X22030.0.0" - using_in_phasing_xy
#"X22182.0.0" - some_field
