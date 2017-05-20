import sys
from PIL import Image
from romtools.disk import Disk
from rominfo import DEST_DISK_DEMO, DEST_DISK_DATA_1, DEST_DISK_SYSTEM
from bitstring import BitArray

#SystemDisk = Disk(DEST_DISK_SYSTEM)
DemoDisk = Disk(DEST_DISK_DEMO)
#Data1Disk = Disk(DEST_DISK_DATA_1)

bmp_palette = ['black',
               None,
               None,
               None,
               None,
               None,
               None,
               'dark grey',
               'light grey',
               None,
               None,
               None,
               None,
               None,
               None,
               'white',]

palette_planes = [
            BitArray([0, 0, 0, 0]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]), # dark grey
            BitArray([1, 1, 1, 1]), # light grey
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
            BitArray([1, 1, 1, 1]),
]

def encode(filename, ugd_filename):
    im = Image.open(filename)
    pix = im.load()
    print(im.size)

    blocks = im.size[0]//8
    print(blocks)
    
    with open(ugd_filename, 'wb') as f:
        f.write(b'\x01')
        f.write(blocks.to_bytes(2, byteorder='little'))
        f.write(im.size[1].to_bytes(1, byteorder='little'))


        for p in range(4):
            for b in range(blocks):
                for row in range(im.size[1]):
                    rowdata =[pix[col, row] for col in range(b*8, (b*8)+8)]
                    # Currently only handles black and white.
                    #bool_array = [c > 0 for c in rowdata]

                    bool_array = [palette_planes[c][p] for c in rowdata]
                    ba = BitArray(bool_array)
                    val = ba.uint
                    if 0x10 <= val <= 0x4f or 0x60 <= val <= 0x6f or 0x80 <= val <= 0x9f or 0xb0 <= val <= 0xef:
                        f.write(b'\xe1') # escape character??
                        print('e1')
                    f.write(val.to_bytes(1, byteorder='little'))
                    print(ba)

if __name__ == '__main__':
    filename = sys.argv[1]
    ugd_filename = filename.replace('bmp', 'ugd')
    encode(filename, ugd_filename)
    DemoDisk.insert(ugd_filename)