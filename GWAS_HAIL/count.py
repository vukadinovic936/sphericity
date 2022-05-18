import numpy as np
import pandas as pd
import hail as hl

SAMPLE_QC_FILE="/mnt/i/UKB_DATA/imputed_UKB/qc.tsv"
df = hl.import_table(SAMPLE_QC_FILE)
df = df.annotate(PC1 = hl.float64(df['PC1']),
                 PC2 = hl.float64(df['PC2']),
                 PC3 = hl.float64(df['PC3']),
                 PC4 = hl.float64(df['PC4']),
                 PC5 = hl.float64(df['PC5']),
                 PC6 = hl.float64(df['PC6']),
                 PC7 = hl.float64(df['PC7']),
                 PC8 = hl.float64(df['PC8']),
                 PC9 = hl.float64(df['PC9']),
                 PC10 = hl.float64(df['PC10']),
                 eid = df['eid'],
                 in_white_British_ancestry_subset = df['ethnicity'] == "1",
                 used_in_pca_calculation = df['used.in.pca.calculation'] == "1",
                 excess_relatives = df['excess.relatives']=="1",
                 putative_sex_chromosome_aneuploidy = df['putative.sex.chromosome.aneuploidy']=="1",
                 isFemale = df['Inferred.Gender'] == '0')
df=df.to_pandas()
df['eid']=np.array(df['eid']).astype('float')
imaging=pd.read_csv("/mnt/i/UKB_DATA/tsv_pheno/si_final.tsv",sep='\t')
imaging=imaging.merge(df, left_on='idx',right_on='eid')
print(len(imaging))
imaging=imaging[imaging['in_white_British_ancestry_subset']==True]
print(len(imaging))
imaging=imaging[imaging['excess_relatives']==False]
print(len(imaging))

