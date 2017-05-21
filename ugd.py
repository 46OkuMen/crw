import sys
from PIL import Image
from romtools.disk import Disk
from rominfo import DEST_DISK_DEMO, DEST_DISK_DATA_1, DEST_DISK_SYSTEM
from bitstring import BitArray

def rgb2hex(r, g, b):  
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)  

#SystemDisk = Disk(DEST_DISK_SYSTEM)
DemoDisk = Disk(DEST_DISK_DEMO)
Data1Disk = Disk(DEST_DISK_DATA_1)

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
}

# The text remains orange (0001) because it gets misaligned at the 4th plane?

def encode(filename, ugd_filename):
    im = Image.open(filename)
    print(im.size)


    im = im.convert()
    pix = im.load()
    #print(len(im.palette.tostring()))
    #for c in range(0, 64, 3):
    #    print(im.palette.tobytes()[c:c+3])

    blocks = im.size[0]//8
    print(blocks)
    
    with open(ugd_filename, 'wb') as f:
        f.write(b'\x01')
        f.write(blocks.to_bytes(2, byteorder='little'))
        f.write(im.size[1].to_bytes(1, byteorder='little'))


        for p in range(4):
            for b in range(blocks):
                for row in range(im.size[1]):
                    rowdata =[pix[col, row][0:3] for col in range(b*8, (b*8)+8)]

                    bool_array = [menu_palette[c][p] for c in rowdata]
                    #print(rowdata)
                    #print(bool_array)

                    ba = BitArray(bool_array)
                    val = ba.uint
                    if val:
                        f.write(b'\xe1') # escape character??
                        print('e1')
                    f.write(val.to_bytes(1, byteorder='little'))
                    print(p, b, row, ba)

if __name__ == '__main__':
    filename = sys.argv[1]
    ugd_filename = filename.replace('bmp', 'ugd').replace('png', 'ugd')
    encode(filename, ugd_filename)
    DemoDisk.insert(ugd_filename)
    #Data1Disk.insert(ugd_filename)