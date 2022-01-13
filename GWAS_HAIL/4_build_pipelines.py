from __future__ import print_function
from pprint import pprint
import sys
import hail as hl
import pandas as pd

SAMPLE_QC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/qc.kt' 
kt = hl.read_table(SAMPLE_QC_TABLE)
n_samples = kt.count()
n_samples

PHESANT_FILE = "/mnt/i/UKB_DATA/non_imputed_UKB/phe_files/mitral_distance.tsv"
cols = list(pd.read_csv(PHESANT_FILE, sep='\t').columns)[1:]

traits = hl.import_table(PHESANT_FILE,impute=True)
traits = traits.annotate(idx = hl.str(traits.idx))

# join kt and traits by idx and sample
table_joined = traits.key_by('idx').join(kt.key_by('eid'))
table_joined.write("/mnt/i/UKB_DATA/imputed_UKB/pipeline_mitral.kt",overwrite=True)


