import hail as hl

#hl.init(default_reference='GRCh38')

BGEN_FILES = '/workspace/UKBB_data/imputed/ukb22828_c*_b0_v3.bgen/'
SAMPLE_FILE = "/workspace/UKBB_data/imputed/joined.sample"

hl.index_bgen(BGEN_FILES,
              contig_recoding={'01':'1',
                               '02':'2',
                               '03':'3',
                               '04':'4',
                               '05':'5',
                               '06':'6',
                               '07':'7',
                               '08':'8',
                               '09':'9'})