import hail as hl
from bokeh.io import output_file, save
from bokeh.layouts import gridplot

#BGEN_FILES = '/workspace/UKBB_data/imputed/ukb_imp_chr*_v3.bgen'
BGEN_FILES = '/data/UKBB_data/imputed/ukb22828_c*_b0_v3.bgen/'
SAMPLE_FILE = "/data/UKBB_data/imputed/joined.sample"

MFI_TABLE ='mfi_joined.kt'
QC_TABLE="qc.tsv"
PIPELINE_TABLE = 'pipeline.kt'
RESULTS_TABLE = 'results.kt' 

# get MFI
print("LOADING MFI")
mfi_table = hl.read_table(MFI_TABLE)
mfi_table = mfi_table.key_by('rsid')
mfi_table = mfi_table.select('v','info')

print("Preparing BGEN")
data = hl.import_bgen(path = BGEN_FILES,
                      sample_file= SAMPLE_FILE, entry_fields=['GT', 'GP','dosage'])
data= data.annotate_rows(mfi=mfi_table[data.row.rsid])
print("LOAD QC TABLE")

df_qc = hl.import_table(QC_TABLE)
df_qc = df_qc.annotate(PC1 = hl.float64(df_qc['PC1']),
                 PC2 = hl.float64(df_qc['PC2']),
                 PC3 = hl.float64(df_qc['PC3']),
                 PC4 = hl.float64(df_qc['PC4']),
                 PC5 = hl.float64(df_qc['PC5']),
                 PC6 = hl.float64(df_qc['PC6']),
                 PC7 = hl.float64(df_qc['PC7']),
                 PC8 = hl.float64(df_qc['PC8']),
                 PC9 = hl.float64(df_qc['PC9']),
                 PC10 = hl.float64(df_qc['PC10']),
                 eid = df_qc['eid'],
                 in_white_British_ancestry_subset = df_qc['ethnicity'] == "1",
                 used_in_pca_calculation = df_qc['used.in.pca.calculation'] == "1",
                 excess_relatives = df_qc['excess.relatives']=="1",
                 putative_sex_chromosome_aneuploidy = df_qc['putative.sex.chromosome.aneuploidy']=="1",
                 isFemale = df_qc['Inferred.Gender'] == '0')

df_qc = df_qc.filter(df_qc.sample!= "-1")
df_qc = df_qc.filter(df_qc.sample!= "-2")
df_qc = df_qc.filter(df_qc.sample!= "-3")
df_qc = df_qc.filter(df_qc.used_in_pca_calculation==True)
df_qc = df_qc.filter(df_qc.excess_relatives==False)

samples = df_qc.select('eid',
           'isFemale',
           'PC1',
           'PC2',
           'PC3',
           'PC4',
           'PC5',
           'PC6',
           'PC7',
           'PC8',
           'PC9',
           'PC10')['eid'].collect()
hl_samples = hl.str(samples)
data = data.filter_cols(hl_samples.contains(data.s))
data = hl.variant_qc(data)

print("FILTERING DATA")
data=data.filter_rows(data.mfi.info > 0.8) 
data=data.filter_rows(data.variant_qc.AF[1] > 0.001)
data=data.filter_rows(data.variant_qc.AF[1] < 0.999)
data=data.filter_rows(data.variant_qc.p_value_hwe > 1e-10)
data=data.filter_rows(data.variant_qc.call_rate > 0.95)
print("Starting GWAS")

pipeline_table = hl.read_table(PIPELINE_TABLE)

vds=data
pheno_table = hl.read_table(PIPELINE_TABLE)
vds=vds.annotate_cols(pheno = pheno_table[vds.col.s])
print("LINEAR REG")
gwas = hl.linear_regression_rows( y = vds.pheno.hw,
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
print("WRITTERN RESULTS")
