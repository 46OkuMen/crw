import os

from rominfo import FILES, FILE_BLOCKS, CONTROL_CODES, POINTER_CONSTANT
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel

ORIGINAL_ROM_PATH = os.path.join('original', 'CRW_system.FDI')
TARGET_ROM_PATH = os.path.join('patched', 'CRW_system.FDI')
DUMP_XLS_PATH = 'CRW Dump.xlsx'
POINTER_XLS_PATH = 'crw_pointer_dump.xlsx'

Dump = DumpExcel(DUMP_XLS_PATH, CONTROL_CODES)
PtrDump = PointerExcel(POINTER_XLS_PATH)
OriginalCRW = Disk(ORIGINAL_ROM_PATH, dump_excel=Dump, pointer_excel=PtrDump)
TargetCRW = Disk(TARGET_ROM_PATH)

FILES_TO_REINSERT = ['CR1.EXE',]

for filename in FILES_TO_REINSERT:
    gamefile = Gamefile(filename, disk=OriginalCRW, dest_disk=TargetCRW, pointer_constant=POINTER_CONSTANT[filename])
    pointers = PtrDump.get_pointers(gamefile)
    for block in FILE_BLOCKS[filename]:
        block = Block(gamefile, block)
        previous_text_offset = block.start
        diff = 0
        print(repr(block.blockstring))
        #print gamefile.filestring[block.start:block.stop]
        # TODO: Get pointers.
        #for i, p in enumerate([ptr for ptr in pointers if block.start <= pointers[ptr][0].text_location < block.stop]):
        #    next_p = pointers[i]
        for t in Dump.get_translations(block):
            #if len(t.en_bytestring) == len(t.jp_bytestring) and t.en_bytestring != t.jp_bytestring:
            #if (0x11862 <= t.location <= 0x1195e) and len(t.en_bytestring) == len(t.jp_bytestring) and t.en_bytestring != t.jp_bytestring:
            if (0x11862 <= t.location <= 0x1195e) and t.en_bytestring != t.jp_bytestring:
                print(t)
                loc_in_block = t.location - block.start + diff

                i = block.blockstring.index(t.jp_bytestring)
                j = block.blockstring.count(t.jp_bytestring)

                index = 0
                while index < len(block.blockstring):
                    index = block.blockstring.find(t.jp_bytestring, index)
                    if index == -1:
                        break
                    print('jp bytestring found at', index)
                    index += len(t.jp_bytestring) # +2 because len('ll') == 2

                if j > 1:
                    print("%s multiples of this string found" % j)
                #print("Looking for:", repr(t.jp_bytestring))
                #print(repr(block.blockstring))
                assert loc_in_block == i, (hex(loc_in_block), hex(i))

                block.blockstring = block.blockstring.replace(t.jp_bytestring, t.en_bytestring, 1)

                #assert len(block.blockstring) == len(block.original_blockstring), "%s %s" % (len(block.blockstring), len(block.original_blockstring))
                #print diff

                gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                previous_text_offset = t.location

                this_diff = len(t.en_bytestring) - len(t.jp_bytestring)
                diff += this_diff


        block_diff = len(block.blockstring) - len(block.original_blockstring)
        print(block_diff)
        if block_diff < 0:
            block.blockstring += (-1)*block_diff*b'\x00'
        block_diff = len(block.blockstring) - len(block.original_blockstring)
        assert block_diff == 0, block_diff

        block.incorporate()
    gamefile.write()
