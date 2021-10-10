import pandas as pd
import numpy as np
from phemap import Phemap
from tqdm import tqdm
import pickle

df_icd9=pd.read_csv("icd9.csv")
source_file = 'data/phecode_definitions1.2.csv'
mapping_file = 'data/phecode_map.csv'
phemap = Phemap(source_file=source_file, mapping_file=mapping_file)
patient_diag = {}
for index, row in tqdm(df_icd9.iterrows()):
    pheno_codes = []
    for i in range(1,224):
        icd10 = row[f'ICD10_{i}']
        try:
            phecode = phemap.get_phecode_for_icd10(icd10)
            pheno_codes +=phecode
        except:
            1+2
	patient_diag[row['eid']] = pheno_codes

filehandler = open("patient_diag", 'wb')
pickle.dump(patient_diag, filehandler)