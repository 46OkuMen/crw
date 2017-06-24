import os

SRC_DISK_DEMO = os.path.join('original', 'CRW_demo.FDI')
SRC_DISK_SYSTEM = os.path.join('original', 'CRW_system.FDI')
SRC_DISK_DATA_1 = os.path.join('original', 'CRW_data1.FDI')
SRC_DISK_DATA_2 = os.path.join('original', 'CRW_data2.FDI')

DEST_DISK_DEMO = os.path.join('patched', 'CRW_demo.FDI')
DEST_DISK_SYSTEM = os.path.join('patched', 'CRW_system.FDI')
DEST_DISK_DATA_1 = os.path.join('patched', 'CRW_data1.FDI')
DEST_DISK_DATA_2 = os.path.join('patched', 'CRW_data2.FDI')

# TALK.TXT, IV1-8.TXT, TITOL.TXT, NINMU1-8.TXT
# CRWUNI.TXT
FILES = ['OPEN.EXE', 'CR1.EXE', 'CR2.EXE', 'CR3.EXE', 'CR4.EXE', 'CR5.EXE',
         'CR6.EXE', 'CR7.EXE', 'CR8.EXE']


SYS_FILES = ['OPEN.EXE', 'CR1.EXE', 'CR2.EXE', 'CR3.EXE', 'CR4.EXE', 'CR5.EXE',
             'CR6.EXE', 'CR7.EXE', 'CR8.EXE', 'CRWUNI.TXT', 'TALK.TXT']

DEMO_FILES = ['NINMU1.TXT', 'NINMU2.TXT', 'NINMU3.TXT', 'NINMU4.TXT',
              'NINMU5.TXT', 'NINMU6.TXT', 'NINMU7.TXT', 'NINMU8.TXT',
              'TITOL.TXT', 'IV9.TXT', 'WAKU_C.UGD', 'BAR_A.UGD', 'BAR_B.UGD',
              'C_STAT.UGD', 'END_2.UGD', 'M_STAT.UGD', 'WEAPONX.UGD',
              'BORNAS.UGD', 'T_MOJI.UGD']

DATA_1_FILES = ['IV1.TXT', 'IV2.TXT', 'IV3.TXT', 'IV4.TXT', 'FACE04.UGD',
                'FACE05.UGD', 'FACE06.UGD', 'FACE07.UGD', 'FACE17.UGD',
                'FACE18.UGD', 'FACE19.UGD', 'FACE20.UGD', 'FACE21.UGD',
                'SI100.UGD', 'MAIN_G.UGD']

DATA_2_FILES = ['IV5.TXT', 'IV6.TXT', 'IV7.TXT', 'IV8.TXT', 'FACE04.UGD',
                'FACE05.UGD', 'FACE06.UGD', 'FACE07.UGD', 'FACE17.UGD',
                'FACE18.UGD', 'FACE19.UGD', 'FACE20.UGD', 'FACE21.UGD',
                'SI100.UGD', 'MAIN_G.UGD']

FILE_BLOCKS = {'OPEN.EXE': [(0x9afd, 0x9cd5),  # characters & guns
                            (0x9cd5, 0xa32c),  # credits
                            (0xa59b, 0xa6fc),  # main menu text
                            (0xa78e, 0xa826),  # disk switch
                            (0xa893, 0xa903),  # demo disk switch
                            (0xa976, 0xa9db),  # disk switch
                            (0xaa4b, 0xaab0),  # disk switch
                            (0xaaee, 0xab15),  # unit types
                            (0xaba0, 0xabbe),  # confirm/cancel
                            (0xadb4, 0xadd1),  # more confirm/cancel
                            (0xae3e, 0xae6b),  # unit types & filenames
                            (0xaea5, 0xaeda),  # selection
                            (0xaf04, 0xaf2c)],  # dialog"]
                'CR1.EXE': [(0x11107, 0x111e3), # english names/movements
                            (0x11296, 0x114a2), # general ui
                            (0x1163b, 0x116b0), # save msgs
                            (0x116ed, 0x117b0), # general ui
                            (0x11862, 0x11966), # general ui
                            (0x11970, 0x1198f), # memory errors
                            (0x119f8, 0x11a90), # disk switch
                            (0x11b09, 0x11bca)],  # error msgs"
                'CR2.EXE': [(0x11f37, 0x12014), # english names/movements
                            (0x120c6, 0x122d2), # general ui
                            (0x1246b, 0x124e0), # save msgs
                            (0x1251d, 0x125e0), # general ui
                            (0x1269d, 0x127a1), # general ui
                            (0x127aa, 0x127c9), # memory errors
                            (0x12832, 0x128ca), # disk switch
                            (0x12943, 0x12a04), # error msgs
                            (0x12a2a, 0x12a78)],  # unit placement msgs"]
                'CR3.EXE': [(0x11cf7, 0x11dd3), # english names/movements
                            (0x11e86, 0x12092), # general ui
                            (0x1222b, 0x122a0), # save msgs
                            (0x122dd, 0x123a0), # general ui
                            (0x1245d, 0x12561), # general ui
                            (0x1256a, 0x12589), # memory errors
                            (0x125f2, 0x1268a), # disk switch
                            (0x12703, 0x127c4), # error msgs
                            (0x127ea, 0x12838)],  # unit placement msgs"]
                'CR4.EXE': [(0x11ea7, 0x11f83), # english names/movements
                            (0x12036, 0x12242), # general ui
                            (0x123db, 0x12450), # save msgs
                            (0x1248d, 0x12550), # general ui
                            (0x1260d, 0x12711), # general ui
                            (0x1271a, 0x12739), # memory errors
                            (0x127a2, 0x1283a), # disk switch
                            (0x128b3, 0x12974), # error msgs
                            (0x1299a, 0x129e8)],  # unit placement msgs"]
                'CR5.EXE': [(0x11d97, 0x11e73), # english names/movements
                            (0x11f26, 0x12132), # general ui
                            (0x122cb, 0x12340), # save msgs
                            (0x1237d, 0x12440), # general ui
                            (0x124fd, 0x12601), # general ui
                            (0x1260a, 0x12629), # memory errors
                            (0x12692, 0x1272a), # disk switch
                            (0x127a3, 0x12864), # error msgs
                            (0x1288a, 0x128d8)],  # unit placement msgs"]
                'CR6.EXE': [(0x11c77, 0x11d53), # english names/movements
                            (0x11e06, 0x12012), # general ui
                            (0x121ab, 0x12220), # save msgs
                            (0x1225d, 0x12320), # general ui
                            (0x123dd, 0x124e1), # general ui
                            (0x124ea, 0x12509), # memory errors
                            (0x12572, 0x1260a), # disk switch
                            (0x12683, 0x12744), # error msgs
                            (0x1276a, 0x127b8)],  # unit placement msgs"]
                'CR7.EXE': [(0x11ed7, 0x11fb3), # english names/movements
                            (0x12066, 0x12272), # general ui
                            (0x1240b, 0x12480), # save msgs
                            (0x124bd, 0x12580), # general ui
                            (0x1263d, 0x12741), # general ui
                            (0x1274a, 0x12769), # memory errors
                            (0x127d2, 0x1286a), # disk switch
                            (0x128e3, 0x129a4), # error msgs
                            (0x129ca, 0x12a18)],  # unit placement msgs"
                'CR8.EXE': [(0x11cf7, 0x11dd3), # english names/movements
                            (0x11e86, 0x12092), # general ui
                            (0x1222b, 0x122a0), # save msgs
                            (0x122dd, 0x123a0), # general ui
                            (0x1245d, 0x12561), # general ui
                            (0x1256a, 0x12589), # memory errors
                            (0x125f2, 0x1268a), # disk switch
                            (0x12703, 0x127c4), # error msgs
                            (0x127f2, 0x12840)],  # unit placement msgs"]
}

FILES_WITH_POINTERS = ['OPEN.EXE', 'CR1.EXE', 'CR2.EXE', 'CR3.EXE', 'CR4.EXE',
                       'CR5.EXE', 'CR6.EXE', 'CR7.EXE', 'CR8.EXE']

POINTER_CONSTANT = {
    'OPEN.EXE': 0x9a70,
    'CR1.EXE': 0x11020,
    'CR2.EXE': 0x11e50,
    'CR3.EXE': 0x11c10,
    'CR4.EXE': 0x11dc0,
    'CR5.EXE': 0x11cb0,
    'CR6.EXE': 0x11b90,
    'CR7.EXE': 0x11df0,
    'CR8.EXE': 0x11c10,
}

CONTROL_CODES = {b'[86a5]': b'\x86\x85',
                 b'[8754]': b'\x87\x54',
                 b'[8755]': b'\x87\x55',
                 b'[8756]': b'\x87\x56',
                 b'[00]':   b'\x00'}

EOF_CHAR = b'\x10'
