import hail as hl
import os
import sys
import shutil
import pandas as pd
import numpy as np

pheno = str(sys.argv).split(',')[1].split("'")[1]

MFI_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/mfi.kt'
RESULTS_TABLE = f'results_{pheno}.kt'
os.mkdir(f"/mnt/i/UKB_DATA/results/{pheno}")
shutil.move("man.html", f"/mnt/i/UKB_DATA/results/{pheno}/man.html")
shutil.move("qq_plot.html", f"/mnt/i/UKB_DATA/results/{pheno}/qq.html")
EXPORTED_RESULTS = f"/mnt/i/UKB_DATA/results/{pheno}/exported_results.tsv"
results = hl.read_table(RESULTS_TABLE)

mfi_table = hl.read_table(MFI_TABLE)
mfi_table = mfi_table.key_by('v')
results=results.annotate(v=hl.str(results.locus) + "_" + results.alleles[0] + "_" + results.alleles[1] )
mfi_table = mfi_table[results.v]

results=results.annotate(chr = mfi_table.chr,
                         rsid = mfi_table.rsid,
                         pos = mfi_table.pos, 
                         ref = mfi_table.ref, 
                         alt = mfi_table.alt,
                         maf = mfi_table.maf,
                         info = mfi_table.info)

results.export(EXPORTED_RESULTS)

## .mfi has some pos and chr missing, fix that by extracting it from locus
#df = pd.read_csv(EXPORTED_RESULTS, sep='\t')
#CHR = np.array([df['locus'][i].split(":")[0] for i in range(len(df))]).astype('uint8')
#POS = np.array([df['locus'][i].split(":")[1] for i in range(len(df))]).astype('uint')
#df['chr'] = CHR
#df['pos'] = POS
#df.to_csv(EXPORTED_RESULTS, sep='\t', index=0)
