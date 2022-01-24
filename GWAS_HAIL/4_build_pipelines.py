from __future__ import print_function
from pprint import pprint
import sys
import hail as hl
import pandas as pd

pheno = str(sys.argv).split(',')[1].split("'")[1]
SAMPLE_QC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/qc.kt' 
kt = hl.read_table(SAMPLE_QC_TABLE)
n_samples = kt.count()
n_samples

PHESANT_FILE = f"/mnt/i/UKB_DATA/tsv_pheno/{pheno}.tsv"
cols = list(pd.read_csv(PHESANT_FILE, sep='\t').columns)[1:]

traits = hl.import_table(PHESANT_FILE,impute=True)
traits = traits.annotate(idx = hl.str(traits.idx))

# join kt and traits by idx and sample
table_joined = traits.key_by('idx').join(kt.key_by('eid'))
table_joined.write(f"/mnt/i/UKB_DATA/pipelines/{pheno}.kt",overwrite=True)


