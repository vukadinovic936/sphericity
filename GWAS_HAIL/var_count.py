import hail as hl

BGEN_FILES = '/data/UKBB_data/imputed/ukb22828_c1_b0_v3.bgen/'
SAMPLE_FILE = "/data/UKBB_data/imputed/joined.sample"
MFI_TABLE ='mfi_joined.kt'

# Load bgen
bgen = hl.import_bgen(path = BGEN_FILES,
                      sample_file= SAMPLE_FILE, entry_fields=['GT', 'GP','dosage'])
print("LOADED BGEN FILES, NUM OF VARIANTS")
print(bgen.count())

# Q: Is this >0.8 info making a problem
mfi_table = hl.read_table(MFI_TABLE)
mfi_table = mfi_table.key_by('rsid')
mfi_table = mfi_table.select('v','info')
print(mfi_table.describe())
print("LOADED MFI JOINED, NUM OF VARS HERE")

print("AFTER FILTERING MFI")
print(mfi_table.filter(mfi_table.info> 0.8 ).count())
### FIGURE OUT HERE HOW TO FILTER BY INFO
data=bgen.annotate_rows(mfi=mfi_table[bgen.row.rsid])
data=data.filter_rows( data.mfi.info > 0.8 )  
#kdata=data.filter_rows( data.mfi.info > -1 | hl.is_nan(data.mfi.info))  
#data = data.annotate_rows(
#	mfi = hl.if_else()
#)

print("ANNOTATED AND FILTERED info > 0.8")
print(data.count())

#
#data=data.filter_rows(data.variant_qc.AF[1] > 0.001)
#print("FILTERED FOR AF > 0.001")
#print(data.count())
#
#data=data.filter_rows(data.variant_qc.AF[1] < 0.999)
#print("FILTERED FOR AF < 0.999")
#print(data.count())
#
#data=data.filter_rows(data.variant_qc.p_value_hwe > 1e-10)
#print("FILTERED FOR hew > 1e-10")
#print(data.count())
#
#data=data.filter_rows(data.variant_qc.call_rate > 0.95)
#print("FILTERED FOR call rate > 0.95")
#print(data.count())
#
