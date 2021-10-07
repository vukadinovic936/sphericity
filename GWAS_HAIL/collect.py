import hail as hl

MFI_TABLE ='mfi.kt'
HRC_FILE = 'HRC.r1-1.GRCh37.wgs.mac5.sites.tab'

mfi_table = hl.read_table(MFI_TABLE)
hrc_table = hl.import_table(HRC_FILE,impute=True)
mfi_table=mfi_table.key_by('v')
hrc_table = hrc_table.annotate(chr = mfi_table[hrc_table.v].chr,
                               rsid = mfi_table[hrc_table.v].rsid,
                               pos = mfi_table[hrc_table.v].pos,
                               ref = mfi_table[hrc_table.v].ref,
                               alt = mfi_table[hrc_table.v].alt,
                               maf = mfi_table[hrc_table.v].maf,
                               wkoknows = mfi_table[hrc_table.v].whoknows,
                               info = mfi_table[hrc_table.v].info)
print(":DONE")
hrc_table.write("joinedHRC.qt", overwrite = True)
