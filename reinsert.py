import os

from rominfo import FILES, FILE_BLOCKS, CONTROL_CODES, POINTER_CONSTANT, EOF_CHAR
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

FILES_TO_REINSERT = ['OPEN.EXE', 'CR1.EXE', 'CR2.EXE', 'CR3.EXE', 'CR4.EXE', 'CR5.EXE',
                     'CR6.EXE', 'CR7.EXE', 'CR8.EXE',]

def mission_ASM_hacks(gamefile):
    first_open_index = gamefile.filestring.index(b'\xc7\x46\xfc\x06\x00') + 3
    gamefile.edit(first_open_index, b'\x0d')

    first_close_index = gamefile.filestring.find(b'\xc7\x46\xfc\x06\x00', first_open_index) + 3
    gamefile.edit(first_close_index, b'\x0d')

    first_highlight_index = gamefile.filestring.find(b'\xc7\x46\xfa\x04\x00') + 3
    gamefile.edit(first_highlight_index, b'\x0b')
    # TODO: What about the duplicate much later?

    EOF_control_code_index = gamefile.filestring.find(b'\x80\x7e\xfc\x20') + 3
    gamefile.edit(EOF_control_code_index, EOF_CHAR)

for filename in FILES_TO_REINSERT:
    gamefile_path = os.path.join('original', 'files', filename)
    gamefile = Gamefile(gamefile_path, disk=OriginalCRW, dest_disk=TargetCRW, pointer_constant=POINTER_CONSTANT[filename])
    pointers = PtrDump.get_pointers(gamefile)

    if filename == 'OPEN.EXE':
        gamefile.edit(0x2e90, b'\x50\x01')   # intro timer
        gamefile.edit(0x582a, EOF_CHAR)
        gamefile.edit(0x8213, EOF_CHAR)
        gamefile.edit(0x84c1, EOF_CHAR)
        gamefile.edit(0x6042, b'\x0c')       # "ZOU" bug fix, STATUS
        gamefile.edit(0x6ade, b'\x0c')       # "ZOU" bug fix, MECH

    if filename.startswith("CR"):
        mission_ASM_hacks(gamefile)

    for block in FILE_BLOCKS[filename]:
        block = Block(gamefile, block)
        previous_text_offset = block.start
        diff = 0
        print(repr(block.blockstring))
        for t in Dump.get_translations(block):
            if t.en_bytestring != t.jp_bytestring:
                print(t)
                loc_in_block = t.location - block.start + diff

                print(t.jp_bytestring)
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
                assert loc_in_block == i, (hex(loc_in_block), hex(i))

                block.blockstring = block.blockstring.replace(t.jp_bytestring, t.en_bytestring, 1)

                gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                previous_text_offset = t.location

                this_diff = len(t.en_bytestring) - len(t.jp_bytestring)
                diff += this_diff


        block_diff = len(block.blockstring) - len(block.original_blockstring)
        if block_diff < 0:
            block.blockstring += (-1)*block_diff*b'\x00'
        block_diff = len(block.blockstring) - len(block.original_blockstring)
        assert block_diff == 0, block_diff

        block.incorporate()

    gamefile.write()
