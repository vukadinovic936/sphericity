import hail as hl

hl.init()
mt = hl.read_matrix_table('data/1kg.mt')
table = (hl.import_table('data/1kg_annotations.txt', impute=True)
                 .key_by('Sample'))

mt = mt.annotate_cols(pheno = table[mt.s])
mt = hl.sample_qc(mt)
mt = mt.filter_cols((mt.sample_qc.dp_stats.mean >= 4) & (mt.sample_qc.call_rate >= 0.97))
ab = mt.AD[1] / hl.sum(mt.AD)
filter_condition_ab = ((mt.GT.is_hom_ref() & (ab <= 0.1)) |
                        (mt.GT.is_het() & (ab >= 0.25) & (ab <= 0.75)) |
                        (mt.GT.is_hom_var() & (ab >= 0.9)))
mt = mt.filter_entries(filter_condition_ab)
mt = hl.variant_qc(mt)
mt = mt.filter_rows(mt.variant_qc.AF[1] > 0.01)

#eigenvalues, pcs, _ = hl.hwe_normalized_pca(mt.GT)

#mt = mt.annotate_cols(scores = pcs[mt.s].scores)
gwas = hl.linear_regression_rows(
    y=mt.pheno.CaffeineConsumption,
    x=mt.GT.n_alt_alleles(),
    covariates=[1.0])

gwas.write("results.kt", overwrite=True)
