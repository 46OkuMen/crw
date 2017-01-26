import os

from rominfo import FILES, FILE_BLOCKS, CONTROL_CODES
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel

ORIGINAL_ROM_PATH = os.path.join('original_roms', 'CRW_system.FDI')
TARGET_ROM_PATH = os.path.join('patched_roms', 'CRW_system.FDI')
DUMP_XLS_PATH = 'CRW Dump.xlsx'

OriginalCRW = Disk(ORIGINAL_ROM_PATH)
TargetCRW = Disk(TARGET_ROM_PATH)
Dump = DumpExcel(DUMP_XLS_PATH, CONTROL_CODES)

FILES_TO_REINSERT = ['CR1.EXE',]

for filename in FILES_TO_REINSERT:
    gamefile = Gamefile(OriginalCRW, TargetCRW, filename)
    for block in FILE_BLOCKS[filename]:
        block = Block(gamefile, block)
        for t in Dump.get_translations(block):
            #if len(t.en_bytestring) == len(t.jp_bytestring) and t.en_bytestring != t.jp_bytestring:
            if (0x11862 <= t.location <= 0x1195e) and len(t.en_bytestring) == len(t.jp_bytestring) and t.en_bytestring != t.jp_bytestring:
                try:
                    print t
                    i = gamefile.filestring.index(t.jp_bytestring)
                    prefix = gamefile.filestring[:t.location]
                    suffix = gamefile.filestring[t.location+len(t.jp_bytestring):]
                    gamefile.filestring = prefix + t.en_bytestring + suffix
                    assert len(gamefile.filestring) == len(gamefile.original_filestring), "%s %s" % (len(gamefile.filestring), len(gamefile.original_filestring))
                    #gamefile.filestring = gamefile.filestring.replace(t.jp_bytestring, t.en_bytestring, 1)
                except UnicodeEncodeError:
                    print "something with weird chars in it"

    gamefile.write()
