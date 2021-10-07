from __future__ import print_function
from pprint import pprint
import sys
import hail as hl
import pandas as pd

SAMPLE_QC_TABLE = "qc.kt"
kt = hl.read_table(SAMPLE_QC_TABLE)
n_samples = kt.count()
n_samples

PHESANT_FILE = "hwpheno.tsv"
cols = list(pd.read_csv(PHESANT_FILE, sep='\t').columns)[1:]

traits = hl.import_table(PHESANT_FILE,impute=True)
traits = traits.annotate(idx = hl.str(traits.idx))

# join kt and traits by idx and sample
table_joined = traits.key_by('idx').join(kt.key_by('sample'))
table_joined.write("pipeline.kt",overwrite=True)


