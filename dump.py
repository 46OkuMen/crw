import os
import xlsxwriter
from rominfo import FILES, FILE_BLOCKS

dir = os.curdir

workbook = xlsxwriter.Workbook('crw_dump.xlsx')
header = workbook.add_format({'bold': True, 'align': 'center', 'bottom': True, 'bg_color': 'gray'})
block_division = workbook.add_format({'top': True, })

for filename in FILES:

    worksheet = workbook.add_worksheet(filename)
    worksheet.write(0, 0, 'Offset', header)
    worksheet.write(0, 1, 'Japanese', header)
    worksheet.write(0, 2, 'JP_Char', header)
    worksheet.write(0, 3, 'English', header)
    worksheet.write(0, 4, 'EN_Char', header)
    worksheet.write(0, 5, 'Comments', header)
    worksheet.set_column('A:A', 7)
    worksheet.set_column('B:B', 60)
    worksheet.set_column('C:C', 6)
    worksheet.set_column('D:D', 60)
    worksheet.set_column('E:E', 6)
    worksheet.set_column('F:F', 60)
    row = 1

    print("\n" + filename + "\n")
    with open(os.path.join('system', filename), 'rb') as f:
        for block in FILE_BLOCKS[filename]:
            block_length = block[1] - block[0]
            print("block:", hex(block[0]))
            print("block length:", block_length)
            f.seek(block[0], 0)
            contents = f.read(block_length+1)

            cursor = 0
            sjis_buffer = ""
            sjis_buffer_start = block[0]
            sjis_strings = []
            while cursor < len(contents):

                # ASCII text
                if 0x20 <= ord(contents[cursor]) & 0xf0 <= 0x7f:
                    sjis_buffer += contents[cursor]

                # First byte of SJIS text. Read the next one, too
                elif 0x80 <= ord(contents[cursor]) & 0Xf0 <= 0x9f:
                    sjis_buffer += contents[cursor]
                    cursor += 1
                    sjis_buffer += contents[cursor]

                # halfwidth kana
                elif 0xa1 <= ord(contents[cursor]) & 0xf0 <= 0xdf:
                    sjis_buffer += contents[cursor]


                # End of continuous SJIS string, so add the buffer to the strings and reset buffer
                else:
                    if sjis_buffer:
                        sjis_strings.append((sjis_buffer_start, sjis_buffer))
                    sjis_buffer = ""
                    sjis_buffer_start = block[0] + cursor+1
                cursor += 1

            # Catch anything left after exiting the loop
            if sjis_buffer:
                sjis_strings.append((sjis_buffer_start, sjis_buffer))


            if len(sjis_strings) == 0:
                continue

            for s in sjis_strings:
                loc = '0x' + hex(s[0]).lstrip('0x').zfill(5)
                print(loc)
                print(repr(s[1]))
                sjis_string = s[1].replace('\x87\x54', '[8754]')
                sjis_string = sjis_string.replace('\x87\x55', '[8755]')
                sjis_string = sjis_string.replace('\x87\x56', '[8756]')
                sjis_string = sjis_string.replace('\x86\xa5', '[86a5]')
                jp = sjis_string.decode('shift-jis')

                if len(jp.strip()) == 0:
                    continue

                worksheet.write(row, 0, loc)
                worksheet.write(row, 1, jp)
                row += 1

            worksheet.set_row(row, 15, block_division)

workbook.close()
