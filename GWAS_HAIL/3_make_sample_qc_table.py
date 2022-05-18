from __future__ import print_function
from pprint import pprint
import sys
import hail as hl
import pandas as pd
## NEW
## NOTE: WE DROPPED PCA COLUMNS WITH NANS in qc file


SAMPLE_QC_FILE = "/mnt/i/UKB_DATA/imputed_UKB/qc_sphericity_index.tsv"
SAMPLE_QC_TABLE = "/mnt/i/UKB_DATA/imputed_UKB/qc_sphericity_index.kt"

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


## END
#SAMPLE_QC_FILE = "/mnt/i/UKB_DATA/imputed_UKB/qc_si.tsv"
#SAMPLE_QC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/qc.kt' 
#main = pd.read_csv(SAMPLE_QC_FILE,sep='\t')
#print(main)
#main=main[main['ethnicity']==1.0]
#main=main[main['excess.relatives']==0.0]
#main=main[['eid',
#          'Inferred.Gender',
#          'age_at_MRI',
#          'PC1',
#          'PC2',
#          'PC3',
#          'PC4',
#          'PC5',
#          'PC6',
#          'PC7',
#          'PC8',
#          'PC9',
#          'PC10']]
#main=main.astype({"eid":str},errors='raise')
#main=main.rename(columns={"Inferred.Gender":"isFemale"})
#main=main.astype({"eid":str,
#                  "isFemale":bool,
#                  "age_at_MRI":float,
#                  "PC1":float,
#                  "PC2":float,
#                  "PC3":float,
#                  "PC4":float,
#                  "PC5":float,
#                  "PC6":float,
#                  "PC7":float,
#                  "PC8":float,
#                  "PC9":float,
#                  "PC10":float}, errors='raise')
##print(main)
#main.to_csv("temp.tsv", sep='\t')
#df=hl.import_table("temp.tsv",impute=True)
#df=df.annotate(eid=hl.str(df.eid))
#print(df.show(10))
#df.write(SAMPLE_QC_TABLE,overwrite=True)
# c
#hc = hail.HailContext()
# sampddd
## see Untiled.ipybn
#SAMPLE_QC_FILE = "/mnt/i/UKB_DATA/imputed_UKB/qc_si.tsv"
#SAMPLE_QC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/qc.kt' 
#df = hl.import_table(SAMPLE_QC_FILE,impute=True)
#df = df.annotate(PC1 = df['PC1'],
#                 PC2 = df['PC2'],
#                 PC3 = df['PC3'],
#                 PC4 = df['PC4'],
#                 PC5 = df['PC5'],
#                 PC6 = df['PC6'],
#                 PC7 = df['PC7'],
#                 PC8 = df['PC8'],
#                 PC9 = df['PC9'],
#                 PC10 = df['PC10'],
#                 eid = df['eid'],
#                 in_white_British_ancestry_subset = df['ethnicity'] == "1.0",
#                 used_in_pca_calculation = df['used.in.pca.calculation'] == "1.0",
#                 no_excess_relatives = df['excess.relatives']=="0.0",
#                 putative_sex_chromosome_aneuploidy = df['putative.sex.chromosome.aneuploidy']=="1.0",
#                 isFemale = df['Inferred.Gender'] == '0.0',
#                 age_at_MRI = df['age_at_MRI'])
#
##df = df.key_by('sample')
##df = df.filter(df.eid!= "-1")
##df = df.filter(df.eid!= "-2")
##df = df.filter(df.eid!= "-3")
##df = df.filter(df.used_in_pca_calculation==True)
##df = df.filter(hl.is_missing(df.putative_sex_chromosome_aneuploidy))
#df = df.filter(df.no_excess_relatives==True)
#df = df.filter(df.in_white_British_ancestry_subset==True)
#print(df.count())
#df.select('eid',
#           'isFemale',
#           'age_at_MRI',
#           'PC1',
#           'PC2',
#           'PC3',
#           'PC4',
#           'PC5',
#           'PC6',
#           'PC7',
#           'PC8',
#           'PC9',
#           'PC10').write(SAMPLE_QC_TABLE,overwrite=True)

#kt = hl.read_table(SAMPLE_QC_TABLE)
#n_samples = kt.count()
#n_samples
#print(n_samples)
#kt.show()
