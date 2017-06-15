import os
from PIL import Image
from romtools.disk import Disk
from rominfo import DEST_DISK_DEMO, DEST_DISK_DATA_1, DEST_DISK_DATA_2, DEST_DISK_SYSTEM
from bitstring import BitArray
from shutil import copyfile

def rgb2hex(r, g, b):  
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)  

#SystemDisk = Disk(DEST_DISK_SYSTEM)
DemoDisk = Disk(DEST_DISK_DEMO)
Data1Disk = Disk(DEST_DISK_DATA_1)
Data2Disk = Disk(DEST_DISK_DATA_2)

"""
gameplay palette:
0000 black    #000000
0001 ltoran   #ff9933
0010 grngrey  #aaaa55
0011 orange   #ee8844
0100 blue     #5588dd
0101 brown    #663300
0110 dkgrey   #998899
0111 pale     #ffccaa
1000 purple   #4411aa
1001 red      #dd3311
1010 blugrey  #665577
1011 peach    #ffaa77
1100 green    #558800
1101 tan      #cc6611
1110 ltgrey   #ccccaa
1111 white    #ffffff
"""

gameplay_palette = {
    (0x00, 0x00, 0x00): BitArray([0, 0, 0, 0]),  # black
    (0xff, 0x99, 0x33): BitArray([0, 0, 0, 1]),  # light orange
    (0xaa, 0xaa, 0x55): BitArray([0, 0, 1, 0]),  # green-grey
    (0xee, 0x88, 0x44): BitArray([0, 0, 1, 1]),  # orange
    (0x55, 0x88, 0xdd): BitArray([0, 1, 0, 0]),  # blue
    (0x66, 0x33, 0x00): BitArray([0, 1, 0, 1]),  # brown
    (0x99, 0x88, 0x99): BitArray([0, 1, 1, 0]),  # dark grey
    (0xff, 0xcc, 0xaa): BitArray([0, 1, 1, 1]),  # pale
    (0x44, 0x11, 0xaa): BitArray([1, 0, 0, 0]),  # purple
    (0xdd, 0x33, 0x11): BitArray([1, 0, 0, 1]),  # red
    (0x66, 0x55, 0x77): BitArray([1, 0, 1, 0]),  # blue-grey
    (0xff, 0xaa, 0x77): BitArray([1, 0, 1, 1]),  # peach
    (0x55, 0x88, 0x00): BitArray([1, 1, 0, 0]),  # green
    (0xcc, 0x66, 0x11): BitArray([1, 1, 0, 1]),  # tan
    (0xcc, 0xcc, 0xaa): BitArray([1, 1, 1, 0]),  # light grey
    (0xff, 0xff, 0xff): BitArray([1, 1, 1, 1]),  # white

    (0xad, 0xad, 0x52): BitArray([0, 0, 1, 0]),  # green-grey
    (0xcc, 0xcc, 0xaa): BitArray([1, 1, 1, 0]),  # light grey
    (0x9c, 0x8c, 0x9c): BitArray([0, 1, 1, 0]),  # dark grey
    (0x52, 0x8c, 0xde): BitArray([0, 1, 0, 0]),  # blue
    (0xce, 0xce, 0xad): BitArray([1, 1, 1, 0]),  # light grey
    (0xff, 0xce, 0xad): BitArray([0, 1, 1, 1]),  # pale
    (0xff, 0xad, 0x73): BitArray([1, 0, 1, 1]),  # peach
    (0xde, 0x31, 0x10): BitArray([1, 0, 0, 1]),  # red
    (0x63, 0x52, 0x73): BitArray([1, 0, 1, 0]),  # blue-grey
    (0xff, 0x9c, 0x31): BitArray([0, 0, 0, 1]),  # light orange
    (0xce, 0x63, 0x10): BitArray([1, 1, 0, 1]),  # tan
    (0x63, 0x31, 0x00): BitArray([0, 1, 0, 1]),  # brown
    (0x42, 0x10, 0xad): BitArray([1, 0, 0, 0]),  # purple
    (0xef, 0x8c, 0x42): BitArray([0, 0, 1, 1]),  # orange
    (0x52, 0x8c, 0x00): BitArray([1, 1, 0, 0]),  # green

    (0xee, 0xee, 0xee): BitArray([1, 1, 1, 1]),  # white
    (0xbb, 0xbb, 0x99): BitArray([1, 1, 1, 0]),  # light grey
    (0x99, 0x99, 0x44): BitArray([0, 0, 1, 0]),  # green-grey
    (0x44, 0x77, 0xcc): BitArray([0, 1, 0, 0]),  # blue
}

menu_palette = {
    (0x00, 0x00, 0x00): BitArray([0, 0, 0, 0]),   # black
    (0xff, 0x77, 0x11): BitArray([0, 0, 0, 1]),   # yet another orange
    (0x44, 0x33, 0x55): BitArray([0, 0, 1, 0]),   # purple grey
    (0xee, 0x88, 0x44): BitArray([0, 0, 1, 1]),   # orange
    (0x66, 0x77, 0xdd): BitArray([0, 1, 0, 0]),   # periwinkle
    (0x66, 0x33, 0x00): BitArray([0, 1, 0, 1]),   # brown
    (0x88, 0x99, 0xbb): BitArray([0, 1, 1, 0]),   # blue grey
    (0xff, 0xcc, 0x99): BitArray([0, 1, 1, 1]),   # less-pale
    (0xaa, 0xaa, 0xee): BitArray([1, 0, 0, 0]),   # lilac
    (0xee, 0x33, 0x11): BitArray([1, 0, 0, 1]),   # orange-ish red
    (0x55, 0x44, 0x88): BitArray([1, 0, 1, 0]),   # mid purple
    (0xff, 0xaa, 0x77): BitArray([1, 0, 1, 1]),   # peach
    (0x55, 0x44, 0xaa): BitArray([1, 1, 0, 0]),   # indigo
    (0xcc, 0x66, 0x11): BitArray([1, 1, 0, 1]),   # tan
    (0xdd, 0xdd, 0xdd): BitArray([1, 1, 1, 0]),   # light grey
    (0xff, 0xff, 0xff): BitArray([1, 1, 1, 1]),   # white

    (0x07, 0x07, 0x07): BitArray([0, 0, 0, 0]),   # almost black
    (0x66, 0x78, 0xdd): BitArray([0, 1, 0, 0]),   # almost periwinkle
    (0xff, 0x00, 0x00): BitArray([1, 0, 0, 1]),   # pure red
    
}

face06_palette = {
    (0x00, 0x01, 0x00): BitArray([0, 0, 0, 0]),   # almost black   # correct
    (0xff, 0x99, 0x34): BitArray([0, 0, 0, 1]),   # orange 3       # 0, 0, 0, 1
    #                             0, 0, 1, 0
    (0xee, 0x88, 0x43): BitArray([0, 0, 1, 1]),   # orange 2       # correct
    (0x56, 0x87, 0xe0): BitArray([0, 1, 0, 0]),   # periwinkle     # 0, 1, 0, 0
    (0x66, 0x34, 0x03): BitArray([0, 1, 0, 1]),   # brown          # 0, 1, 0, 1
    (0x9a, 0x88, 0x9c): BitArray([0, 1, 1, 0]),   # purple grey 2  # correct
    (0xfe, 0xcc, 0xa9): BitArray([0, 1, 1, 1]),   # orange 5
    (0x33, 0x0a, 0xbd): BitArray([1, 0, 0, 0]),   # purple 1       # 1, 0, 0, 0
    (0x3d, 0x09, 0xb3): BitArray([1, 0, 0, 0]),   # purple 2       # 1, 0, 0, 0
    (0x48, 0x0f, 0xa9): BitArray([1, 0, 0, 0]),   # purple 3       # 1, 0, 0, 0
    (0xdd, 0x34, 0x0a): BitArray([1, 0, 0, 1]),   # red            # correct
    (0x63, 0x55, 0x79): BitArray([1, 0, 1, 0]),   # purple grey 1  # correct
    (0xfe, 0xab, 0x75): BitArray([1, 0, 1, 1]),   # orange 4       # correct
    #                             1, 1, 0, 0
    (0xcd, 0x65, 0x1d): BitArray([1, 1, 0, 1]),   # orange 1       # correct
    (0xc9, 0xcd, 0xa9): BitArray([1, 1, 1, 0]),   # green grey     # correct
    (0xfe, 0xff, 0xfc): BitArray([1, 1, 1, 1]),   # almost white   # correct

    (0xcd, 0x65, 0x12): BitArray([1, 1, 0, 1]),   # orange 1       # correct

}

# periwinkle is mismapped to orange3.  Give orange3 periwinkle's bitstring.
# purple 3 is mismapped to periwinkle. Give periwinkle purple 3's bitstring.
# brown is mismapped to purple 3. Give purple 3 brown's bitstring.
# orange 3 is mismaped to green. That means orange 3's bitstring never needs to be used, but orange 3 should be given orange 4's bitstring maybe?
# purple 2 is mismapped to a weird green. Give it purple 3's bitstring, and retire its bitstring.
# purple 1 is mismapped to brown. Give purple 1's bitstring to brown and assign purple 1 to purple 3.

face19_palette = {
    (0x00, 0x00, 0x00): BitArray([0, 0, 0, 0]),   # black          # correct
    (0xff, 0x99, 0x33): BitArray([0, 0, 0, 1]),   # orange 1       # 0 0 0 1
    (0xff, 0x95, 0x2b): BitArray([0, 0, 0, 1]),   # orange 2       # correct
    (0x37, 0x00, 0xa4): BitArray([0, 0, 0, 1]),   # purple 2       # correct
    (0xee, 0x88, 0x44): BitArray([0, 0, 1, 1]),   # orange 5       # correct
    (0x55, 0x88, 0xdd): BitArray([0, 1, 0, 0]),   # blue           # correct
    (0x66, 0x33, 0x00): BitArray([0, 1, 0, 1]),   # brown          # correct
    (0x99, 0x88, 0x99): BitArray([0, 1, 1, 0]),   # light grey     # correct
    (0xff, 0xcc, 0xaa): BitArray([0, 1, 1, 1]),   # orange 4       # correct
    (0x44, 0x11, 0xaa): BitArray([1, 0, 0, 0]),   # purple 1       # correct
    (0xdd, 0x33, 0x11): BitArray([1, 0, 0, 1]),   # red 2          # correct
    (0xdd, 0x31, 0x0e): BitArray([1, 0, 0, 1]),   # red 1          # correct
    (0x66, 0x55, 0x77): BitArray([1, 0, 1, 0]),   # dark grey      # correct
    (0xff, 0xaa, 0x77): BitArray([1, 0, 1, 1]),   # orange 3       # correct
    (0xcc, 0x66, 0x11): BitArray([1, 1, 0, 1]),   # orange brown   # correct
    (0xcc, 0xcc, 0xaa): BitArray([1, 1, 1, 0]),   # green grey     # correct
    (0xff, 0xff, 0xff): BitArray([1, 1, 1, 1]),   # white          # correct
}

# orange 2 and 3 are probably the same color, so will get the same assignment later
# red 1 and 2 are even more similar

# green-grey is mismapped to orange brown. Give  green-grey's bitstring to orange brown.
# brown is mismapped to a medium green. Retire that bistring.
# dark grey is mismapped to brown. Give dark grey's bitstring to brown.
# light grey is mismapped to purple 1. Give light grey's bitstring to purple 1.
# blue is mismapped to orange 4. Give blue's bitstring to orange 4.
# orange 3 is mismapped to dark green. Retire that bitstring.
# orange 2 is mismapped to dark grey. Give orange 2's bitstring to dark grey.
# orange 1 is mismapped to red 2. Give orange 1's bitstring to red 2.
# purple 1 is mapped to orange 1. Give purple's bitstring to orange 1.
# red 2 is mismapped to blue. Give red 2's bitstring to blue.

# orange 2 is mismapped to dark grey (which is correct). Give orange 1 to orange 2.
# orange 3 is mismapped to dark green. Retire that bitstring.
# orange 1 is mismapped to red. Give it a new bitstring.

# orange 1 is mismapped to light grey. Give orange 1's bitstring to light grey.
# green grey is mismapped to dark green.
# purple grey 

main_g_palette_values = [b'\x00\x00\x00',
                  b'\x04\x01\x0a',
                  b'\x05\x08\x0d',
                  b'\x05\x08\x00',
                  b'\x0a\x0a\x05',
                  b'\x06\x05\x07',
                  b'\x09\x08\x09',
                  b'\x0c\x0c\x0a',
                  b'\x0f\x09\x03',
                  b'\x0d\x03\x01',
                  b'\x06\x03\x00',
                  b'\x0c\x06\x01',
                  b'\x0e\x08\x04',
                  b'\x0f\x0a\x07',
                  b'\x0f\x0c\x0a',
                  b'\x0f\x0f\x0f'
                  ]

main_g_palette_string = b''.join(main_g_palette_values)

def encode(filename, ugd_filename, palette=menu_palette):
    im = Image.open(filename)
    print(im.size)


    im = im.convert()
    pix = im.load()
    #print(len(im.palette.tostring()))
    #for c in range(0, 64, 3):
    #    print(im.palette.tobytes()[c:c+3])

    blocks = im.size[0]//8
    #print(blocks)
    
    with open(ugd_filename, 'wb') as f:
        if 'MAIN_G' in ugd_filename:
            f.write(b'\x02')
            f.write(main_g_palette_string)
        elif 'WAKU_C' in ugd_filename:
            f.write(b'\x01\x33\x01\x80')
        elif im.size[1] > 255:
            f.write(b'\x00')
        else:
            f.write(b'\x01')
            f.write(blocks.to_bytes(2, byteorder='little'))
            f.write(im.size[1].to_bytes(1, byteorder='little'))

        for p in range(4):
            for b in range(blocks):
                for row in range(im.size[1]):
                    rowdata =[pix[col, row][0:3] for col in range(b*8, (b*8)+8)]

                    try:
                        bool_array = [palette[c][p] for c in rowdata]
                    except KeyError as e:
                        print([hex(p) for p in e.args[0]])
                    #print(rowdata)
                    #print(bool_array)

                    ba = BitArray(bool_array)
                    val = ba.uint
                    if val:
                        f.write(b'\xe1') # escape character??
                        #print('e1')
                    f.write(val.to_bytes(1, byteorder='little'))
                    #print(p, b, row, ba)

if __name__ == '__main__':
    demo_disk_filenames = ['WAKU_C.png', 'BAR_A.png', 'BAR_B.png', 'C_STAT.png', 'END_2.png', 'M_STAT.png', 'WEAPONX.png', 'BORNAS.png']
    data_disk_filenames = ['FACE04.png', 'FACE05.png', 'FACE06.png', 'FACE07.png', 'FACE17.png', 'FACE18.png', 'FACE19.png',
                           'FACE20.png', 'FACE21.png', 'SI100.png', 'MAIN_G.png']


    menu_palette_filenames = ['WAKU_C.png', 'BAR_A.png', 'BAR_B.png', 'C_STAT.png', 'END_2.png', 'M_STAT.png', 'WEAPONX.png', 'BORNAS.png']
    gameplay_palette_filenames = ['FACE04.png', 'FACE05.png', 'FACE07.png', 'FACE17.png', 'FACE18.png', 'SI100.png', 'MAIN_G.png']
    face06_palette_filenames = ['FACE06.png',]
    face19_palette_filenames = ['FACE19.png', 'FACE20.png', 'FACE21.png']

   # Face19-21 probably have their own palette too
    for filename in demo_disk_filenames + face06_palette_filenames + data_disk_filenames + face19_palette_filenames:

        filepath = os.path.join('edited_img', filename)
        ugd_filepath = filepath.replace('bmp', 'ugd').replace('png', 'ugd')
        print(ugd_filepath)

        if filename in menu_palette_filenames:
            palette  = menu_palette
        elif filename in gameplay_palette_filenames:
            palette = gameplay_palette
        elif filename in face06_palette_filenames:
            palette = face06_palette
        elif filename in face19_palette_filenames:
            palette = face19_palette

        encode(filepath, ugd_filepath, palette)

        if filename in demo_disk_filenames:
            DemoDisk.insert(ugd_filepath)
        else:
            Data1Disk.insert(ugd_filepath)
            Data2Disk.insert(ugd_filepath)
        #Data1Disk.insert(ugd_filename)
