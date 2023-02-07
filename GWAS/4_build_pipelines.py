from __future__ import print_function
from pprint import pprint
import sys
import hail as hl
import pandas as pd

pheno = str(sys.argv).split(',')[1].split("'")[1]
SAMPLE_QC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/qc.kt'
kt = hl.read_table(SAMPLE_QC_TABLE)
n_samples = kt.count()

PHESANT_FILE = f"/mnt/i/UKB_DATA/tsv_pheno/{pheno}.tsv"

traits = hl.import_table(PHESANT_FILE,impute=True)
traits = traits.annotate(idx = hl.str(traits.idx), pheno=hl.float64(traits.pheno))


traits=traits.key_by('idx')
kt=kt.key_by('eid')
kt=kt.join(traits, how="inner")
kt.write(f"/mnt/i/UKB_DATA/pipelines/{pheno}.kt",overwrite=True)
print(kt.count())
