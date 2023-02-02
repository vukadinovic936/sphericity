import numpy as np
import pandas as pd 

exported_results = "/mnt/c/users/vukadinovim/Documents/Beyond_Size/results/GWAS/sphericity_index_normal/exported_results.tsv"
new_location = "lv_ef.txt"

df = pd.read_csv(exported_results, sep="\t")
df['snpid'] = df['rsid']
df['hg18chr'] = df['chr']
df['bp'] = df['pos']
df['a1'] = df['ref']
df['a2'] = df['alt']
df['beta'] = df['beta']
df['se'] = df['standard_error']
df['pval'] = df['p_value']
df['info'] = df['info']
df['OR'] = np.exp(df['beta'])

df = df[['snpid','hg18chr','bp','a1','a2','beta','se','pval','info','OR']]
df.to_csv(new_location, sep='\t')
