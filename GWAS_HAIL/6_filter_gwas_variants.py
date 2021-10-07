import hail as hl

VARIANT_VDS =  'all_variants.vds'
GWAS_VARIANTS_VDS = 'gwas_variants.vds'
GWAS_VARIANTS_TSV = 'gwas_variants.tsv'
data = hl.read(VARIANT_VDS)
data = data.filter_rows(data.mfi.info > 0.8) 
data = data.filter_rows(data.variant_qc.AF[1] > 0.001)
data = data.filter_rows(data.variant_qc.AF[1] < 0.999)
data = data.filter_rows(data.variant_qc.p_value_hwe > 1e-10)
data = data.filter_rows(data.variant_qc.call_rate > 0.95)
data = data.filter_rows(data.mfi.isHRC == True)
data.write(GWAS_VARIANTS_VDS, overwrite=True)