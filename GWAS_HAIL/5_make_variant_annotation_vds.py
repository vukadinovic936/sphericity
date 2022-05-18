from __future__ import print_function
from pprint import pprint
import hail as hl
import sys
chr = str(sys.argv[1])
#reading files
BGEN_FILES = f'/mnt/i/UKB_DATA/imputed_UKB/imputed/ukb22828_c{chr}_b0_v3.bgen/'
SAMPLE_FILE = "/mnt/i/UKB_DATA/imputed_UKB/imputed/joined.sample"
MFI_FILE =  '/mnt/i/UKB_DATA/imputed_UKB/ukb_mfi_v3.tsv.bgz'
QC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/qc.kt'
#HRC_FILE = "HRC.vcf.bgz"
HRC_FILE = '/mnt/i/UKB_DATA/imputed_UKB/HRC.r1-1.GRCh37.wgs.mac5.sites.tab'

#writing to files
MFI_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/mfi.kt'
HRC_TABLE = '/mnt/i/UKB_DATA/imputed_UKB/hrc.kt'
MFI_JOINED = "/mnt/i/UKB_DATA/imputed_UKB/mfi_joined.kt"
VARIANT_VDS = f'{chr}_all_variants.vds'
GWAS_VARIANTS_VDS = f'{chr}_gwas_variants.vds'
#mfi_table = (
#    hl.import_table(
#        MFI_FILE,
#        no_header=True,
#        impute=True,
#    )
#    .rename({
#        'f0': 'chr',
#        'f1': 'v',
#        'f2': 'rsid',
#        'f3': 'pos',
#        'f4': 'ref',
#        'f5': 'alt',
#        'f6': 'maf',
#        'f7': "whoknows",
#        'f8': 'info'
#    })
#)
#mfi_table = mfi_table.key_by('v')
#mfi_table.write(MFI_TABLE,overwrite=True)
#hrc_table=(
#    hl
#    .import_table(
#        HRC_FILE,
#        impute=True
#    )
#)
#hrc_table = hrc_table.filter(hrc_table['#CHROM'] != "X")
#hrc_table=hrc_table.annotate(v=
#                             hrc_table['#CHROM']+":"+hl.str(hrc_table['POS'])+"_"+hl.str(hrc_table.REF)+"_"+hl.str(hrc_table.ALT))
#
#hrc_table=hrc_table.select('v')
#hrc_table.key_by('v')
#hrc_table.write(HRC_TABLE, overwrite=True)
#
#print("WRITTERN MFI AND HRC")
#mfi_table = hl.read_table(MFI_TABLE)
#hrc_table = hl.read_table(HRC_TABLE)
#table_joined = mfi_table.key_by('v').join(hrc_table.key_by('v'),how='inner')
#print("DONE Merging MFI and HRE!")
#table_joined.write(MFI_JOINED, overwrite=True)
#print("DONE Writing MFI_JOINED!")
## there is no isHRC we remove it here in this step.

#
### Process BGEN
# no hrc
mfi_joined = hl.read_table(MFI_TABLE)
mfi_joined = mfi_joined.key_by('rsid')
bgen = hl.import_bgen(path = BGEN_FILES,
                      sample_file= SAMPLE_FILE, entry_fields=['GT', 'GP','dosage'])
data=bgen.annotate_rows(mfi=mfi_joined[bgen.row.rsid])
# qc file
samples=hl.read_table(QC_TABLE)['eid'].collect()
hl_samples = hl.str(samples)
data = data.filter_cols(hl_samples.contains(data.s))
data = hl.variant_qc(data)

data = data.filter_rows(data.mfi.info >= 0.3)
data = data.filter_rows(data.mfi.maf >= 0.01)
data = data.filter_rows(data.variant_qc.AF[1] > 0.001)
data = data.filter_rows(data.variant_qc.AF[1] < 0.999)
data = data.filter_rows(data.variant_qc.p_value_hwe >= 1e-20)
data = data.filter_rows(data.variant_qc.call_rate >= 0.95)
data = hl.sample_qc(data)
data = data.filter_cols( (data.sample_qc.call_rate >= 0.98 ))
data.write(GWAS_VARIANTS_VDS, overwrite=True)
print("DONE WRITING PROCESSED VARIANTS")

