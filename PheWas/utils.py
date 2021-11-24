import pandas as pd
import numpy as np

def phe_to_tsv(phe_path,tsv_path):
	a = pd.read_csv(phe_path, sep=' ', names=['idx','b','pheno'])
	IDS = np.array(a['idx'])
	Pheno = np.array(a['pheno'])
	dic = {"idx":IDS, "pheno":Pheno}
	new_tsv = pd.DataFrame.from_dict(dic)
	new_tsv.to_csv(tsv_path, sep='\t')

def exclude_abnormal(tsv_path, new_tsv_path):
    df = pd.read_csv("/mnt/i/UKB_DATA/imputed_UKB/hw_normal.csv")
    tsv = pd.read_csv(tsv_path, sep='\t')
    mask = tsv['idx'].isin(np.array(df['idx']))
    tsv=tsv.loc[mask]
    tsv=tsv.drop(columns=['Unnamed: 0'])
    tsv.to_csv(new_tsv_path, sep='\t', index=False)