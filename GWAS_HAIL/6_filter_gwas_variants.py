import hail as hl

"""

ID list:
	- cMRI cohort (you provide)
	- no kinship (Data-Field 22021)
	- European (Data-Field 22006)
	- not outlier (Data-Field 22027)

plink \
	--bgen <imputation .bgen file> \
	--sampel <imputation .sample file>  \
    --keep <ID list from above> \
    --maf 0.001 \
    --hwe 1e-6 \
    --geno 0.02 \
    --mind 0.02 \
	--mach-r2-filter 0.4 2 \
    --write-snplist \
    --make-just-fam \
    --out <prefix>

"""
VARIANT_VDS =  'all_variants.vds'
GWAS_VARIANTS_VDS = 'gwas_variants.vds'
GWAS_VARIANTS_TSV = 'gwas_variants.tsv'
data = hl.read_matrix_table(VARIANT_VDS)
data = data.filter_rows(data.mfi.info > 0.8) 
data = data.filter_rows(data.mfi.maf > 0.001) 
data = data.filter_rows(data.variant_qc.AF[1] > 0.001)
data = data.filter_rows(data.variant_qc.AF[1] < 0.999)
data = data.filter_rows(data.variant_qc.p_value_hwe > 1e-10)
data = data.filter_rows(data.variant_qc.call_rate > 0.95)
#data = data.filter_rows(data.mfi.isHRC == True)
data.write(GWAS_VARIANTS_VDS, overwrite=True)
