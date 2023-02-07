from __future__ import print_function
from pprint import pprint
import sys
import hail as hl
import pandas as pd
## NEW
## NOTE: WE DROPPED PCA COLUMNS WITH NANS in qc file


SAMPLE_QC_FILE = "/mnt/i/UKB_DATA/imputed_UKB/qc.tsv"
SAMPLE_QC_TABLE = "/mnt/i/UKB_DATA/imputed_UKB/qc.kt"

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
                 age_at_MRI = hl.float64(df['age_at_MRI']),
                 eid = df['eid'],
                 in_white_British_ancestry_subset = df['ethnicity'] == "1.0",
                 used_in_pca_calculation = df['used.in.pca.calculation'] == "1.0",
                 no_excess_relatives = df['excess.relatives']=="0.0",
                 putative_sex_chromosome_aneuploidy = df['putative.sex.chromosome.aneuploidy']=="1.0",
                 isFemale = df['Inferred.Gender'] == '0.0')



df = df.filter(df.in_white_British_ancestry_subset==True)


df = df.filter(df.no_excess_relatives==True)
df=df.select('eid',
           'isFemale',
           'age_at_MRI',
           'PC1',
           'PC2',
           'PC3',
           'PC4',
           'PC5',
           'PC6',
           'PC7',
           'PC8',
           'PC9',
           'PC10')
df.write(SAMPLE_QC_TABLE,overwrite=True)
print(df.count())
