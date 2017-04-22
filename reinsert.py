import os

from rominfo import FILES, FILE_BLOCKS, CONTROL_CODES
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel

ORIGINAL_ROM_PATH = os.path.join('original', 'CRW_system.FDI')
TARGET_ROM_PATH = os.path.join('patched', 'CRW_system.FDI')
DUMP_XLS_PATH = 'CRW Dump.xlsx'
POINTER_XLS_PATH = 'crw_pointer_dump.xlsx'

OriginalCRW = Disk(ORIGINAL_ROM_PATH)
TargetCRW = Disk(TARGET_ROM_PATH)
Dump = DumpExcel(DUMP_XLS_PATH, CONTROL_CODES)
PtrDump = PointerExcel(POINTER_XLS_PATH)

FILES_TO_REINSERT = ['CR1.EXE',]

for filename in FILES_TO_REINSERT:
    gamefile = Gamefile(filename, OriginalCRW, TargetCRW)
    for block in FILE_BLOCKS[filename]:
        block = Block(gamefile, block)
        diff = 0
        print block
        #print gamefile.filestring[block.start:block.stop]
        # TODO: Get pointers.
        # for p in PtrDump.get_translations(block):
        for t in Dump.get_translations(block):
            #if len(t.en_bytestring) == len(t.jp_bytestring) and t.en_bytestring != t.jp_bytestring:
            #if (0x11862 <= t.location <= 0x1195e) and len(t.en_bytestring) == len(t.jp_bytestring) and t.en_bytestring != t.jp_bytestring:
            if (0x1163b <= t.location <= 0x116b0) and t.en_bytestring != t.jp_bytestring:
                print t
                loc_in_block = t.location - block.start
                
                i = block.blockstring.index(t.jp_bytestring)
                prefix = block.blockstring[:loc_in_block+diff]
                suffix = block.blockstring[loc_in_block+diff+len(t.jp_bytestring):]
                block.blockstring = prefix + t.en_bytestring + suffix
                #assert len(block.blockstring) == len(block.original_blockstring), "%s %s" % (len(block.blockstring), len(block.original_blockstring))
                this_diff = len(t.en_bytestring) - len(t.jp_bytestring)
                diff += this_diff
                #print diff

        block_diff = len(block.blockstring) - len(block.original_blockstring)
        print block_diff
        if block_diff < 0:
            block.blockstring += (-1)*block_diff*'\x00'
        block_diff = len(block.blockstring) - len(block.original_blockstring)
        assert block_diff == 0, block_diff

        block.incorporate()
    gamefile.write()
