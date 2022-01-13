import hail as hl
from bokeh.io import output_file, save
from bokeh.layouts import gridplot

#read from files
PIPELINE_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/pipeline_mitral.kt'
GWAS_VARIANTS_VDS = '2_gwas_variants.vds'
#GWAS_VARIANTS_VDS = 'lead_snp.vds'

# write to files
RESULTS_TABLE = 'results_mitral.kt' 
pipeline_table = hl.read_table(PIPELINE_TABLE)

vds = hl.read_matrix_table(GWAS_VARIANTS_VDS)

for i in range(3,4):
    vds = vds.union_rows(hl.read_matrix_table(f"{i}_gwas_variants.vds"))

vds = vds.annotate_cols(pheno = pipeline_table[vds.s])
print("LINEAR REG")
gwas = hl.linear_regression_rows( y = vds.pheno.pheno,
                                  x = vds.GT.n_alt_alleles(),
                                  covariates = [1.0,
                                                vds.pheno.isFemale,
                                                vds.pheno.PC1,
                                                vds.pheno.PC2,
                                                vds.pheno.PC3,
                                                vds.pheno.PC4,
                                                vds.pheno.PC5,
                                                vds.pheno.PC6,
                                                vds.pheno.PC7,
                                                vds.pheno.PC8,
                                                vds.pheno.PC9,
                                                vds.pheno.PC10])
print("DONE LIN REG")
print("MAKING A PLOT")
p = hl.plot.manhattan(gwas.p_value)
output_file("man.html")
save(p)

print("MAKING QQ PLOT")
p = hl.plot.qq(gwas.p_value)
output_file("qq_plot.html")
save(p)

print("WRITE RESULTS")
gwas.write(RESULTS_TABLE, overwrite=True)
print("WRITTEN RESULTS")
