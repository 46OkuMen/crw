import re
import os
import openpyxl
from collections import OrderedDict
from romtools.dump import BorlandPointer, PointerExcel
from romtools.disk import Gamefile

from rominfo import POINTER_CONSTANT, FILES_WITH_POINTERS

# POINTER_CONSTANT is the line where "Borland Compiler" appears, rounded down to the nearest 0x10.

# TODO: This regex seems awfully broad.
# Maybe add a constraint that it's followed by 9a or ff? That seems to be common...
pointer_regex = r'\\x68\\x([0-f][0-f])\\x([0-f][0-f])'

def capture_pointers_from_function(hx): 
    return re.compile(pointer_regex).finditer(hx)

def location_from_pointer(pointer, constant):
    return '0x' + str(format((unpack(pointer[0], pointer[1]) + constant), '05x'))

def unpack(s, t=None):
    if t is None:
        t = str(s)[2:]
        s = str(s)[0:2]
    s = int(s, 16)
    t = int(t, 16)
    value = (t * 0x100) + s
    return value

pointer_count = 0

os.remove('crw_pointer_dump.xlsx')
PtrXl = PointerExcel('crw_pointer_dump.xlsx')

for gamefile in FILES_WITH_POINTERS:
    print(gamefile)
    pointer_locations = OrderedDict()
    gamefile_path = os.path.join('original', 'files', gamefile)
    GF = Gamefile(gamefile_path, pointer_constant=POINTER_CONSTANT[gamefile])
    with open(gamefile_path, 'rb') as f:
        bs = f.read()
        target_area = (GF.pointer_constant, len(bs))
        print(hex(target_area[0]), hex(target_area[1]))

        only_hex = u""
        for c in bs:
            only_hex += u'\\x%02x' % c

        #print(only_hex)
        pointers = capture_pointers_from_function(only_hex)

        for p in pointers:
            pointer_location = p.start()//4 + 1

            pointer_location = b'0x%05x' % pointer_location
            text_location = location_from_pointer((p.group(1), p.group(2)), GF.pointer_constant)

            if not target_area[0] <= int(text_location, 16) <= target_area[1]:
                continue

            all_locations = [pointer_location,]

            if (GF.filename, text_location) in pointer_locations:
                all_locations = pointer_locations[(GF.filename, text_location)]
                all_locations.append(pointer_location)

            pointer_locations[(GF, text_location)] = all_locations

    # Setup the worksheet for this file
    worksheet = PtrXl.add_worksheet(GF.filename)

    row = 1

    for (gamefile, text_location), pointer_locations in sorted((pointer_locations).items()):
        obj = BorlandPointer(gamefile, pointer_locations, text_location)
        #print(text_location)
        #print(pointer_locations)
        for pointer_loc in pointer_locations:
            worksheet.write(row, 0, text_location)
            worksheet.write(row, 1, str(pointer_loc).lstrip("b'").rstrip("'"))
            try:
                worksheet.write(row, 2, obj.text())
            except:
                worksheet.write(row, 2, u'')
            row += 1

PtrXl.close()