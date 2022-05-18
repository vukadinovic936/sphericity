from __future__ import print_function
from pprint import pprint
import sys
import hail as hl
import pandas as pd

pheno = str(sys.argv).split(',')[1].split("'")[1]
SAMPLE_QC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/qc_sphericity_index.kt'
kt = hl.read_table(SAMPLE_QC_TABLE)
n_samples = kt.count()

PHESANT_FILE = f"/mnt/i/UKB_DATA/tsv_pheno/{pheno}.tsv"

traits = hl.import_table(PHESANT_FILE,impute=True)
traits = traits.annotate(idx = hl.str(traits.idx), pheno=hl.float64(traits.pheno))


traits=traits.key_by('idx')
kt=kt.key_by('eid')
kt=kt.annotate(pheno = traits[kt.eid].pheno)
kt.write(f"/mnt/i/UKB_DATA/pipelines/{pheno}.kt",overwrite=True)

#pheno = str(sys.argv).split(',')[1].split("'")[1]
#SAMPLE_QC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/qc.kt' 
#kt = hl.read_table(SAMPLE_QC_TABLE)
#n_samples = kt.count()
#print(n_samples)
#
#PHESANT_FILE = f"/mnt/i/UKB_DATA/tsv_pheno/{pheno}.tsv"
#
#traits = hl.import_table(PHESANT_FILE)
#traits = traits.annotate(idx = hl.str(traits.idx), pheno=hl.float64(traits.pheno))
#
## join kt and traits by idx and sample
##to and from pandas
#traits=traits.key_by('idx')
#kt=kt.key_by('eid')
#table_joined = traits.join(kt)
#temp=table_joined.to_pandas()
#temp2=hl.Table.from_pandas(temp)
#temp2.write(f"/mnt/i/UKB_DATA/pipelines/{pheno}.kt",overwrite=True)
