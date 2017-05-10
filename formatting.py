from romtools.disk import Disk
from rominfo import DEST_DISK_DEMO, DEST_DISK_DATA_1, DEST_DISK_SYSTEM, EOF_CHAR

SystemDisk = Disk(DEST_DISK_SYSTEM)
DemoDisk = Disk(DEST_DISK_DEMO)
Data1Disk = Disk(DEST_DISK_DATA_1)

ninmus = ['NINMU1.TXT']
ivs = ['IV1.TXT', 'TALK.TXT']

def pad_iv(l):
    """Pad an IV*.TXT line to 80 characters.
    """
    if len(l) > 80:
        l = l[:78]
        l += b'\r\n'
    elif len(l) < 80:
        l.rstrip(b'\r\n')
        l = l + EOF_CHAR*(78 - len(l))
        l += b'\r\n'
    assert len(l) == 80
    return l


# For the NINMU*.TXT files, each line must be an even number of characters.
for n in ninmus:
    with open('patched\original_' + n, 'rb') as f:
        lines = f.readlines()

    with open('patched\\' + n, 'wb') as f:
        print(lines)
        for l in lines:
            print(repr(l))
            print(len(l))
            if len(l) % 2 == 1:
                just_the_line = l.split(b'\r\n')[0]
                l = just_the_line + b" " + b'\r\n'

            #if len(l) > 50:
            #    words = l.split(' ')
            #    firstline = ''
            #    while words and len(firstline + " " + words[0] + '\r\n') <= 50:
            #        firstline += ' ' + words.pop(0)
            #    firstline += '\r\n'
            #    if words:
            #        secondline = ''
            #        while words and len(secondline + " " + words[0] + '\r\n') <= 50:
            #            secondline += ' ' + words.pop(0)
            #        secondline += '\r\n'
            #    f.write(firstline)
            #    f.write(secondline)

            f.write(l)
    DemoDisk.insert('patched\\' + n)

# For IV*.TXT files, each window must be 80 characters long, with 32-character lines.
# Pad with the EOF char after text is done.
for i in ivs:
    with open('patched\original_' + i, 'rb') as f:
        lines = f.readlines()

    with open('patched\\' + i, 'wb') as f:
        # TODO: Split lines; 32 chars each.
        for l in lines:
            l = l.replace(b'\x81\x40', b'  ')
            l = l.replace(b'\xe3\x80\x80', b'   ')
            l = l.replace(b'\xe3\x80', b'  ')
            l = l.replace(b'\x1a', b' ')
            if i.startswith("IV") and len(l.strip()) == 0:
                continue
            l = l.rstrip(b'\r\n')
            l = l.lstrip()
            l = l.rstrip()

            words = l.split(b' ')
            firstline, secondline, thirdline = b'', b'', b''
            window = [firstline, secondline, thirdline]
            for j, _ in enumerate((firstline, secondline, thirdline)):
                if words:
                    window[j] = words.pop(0)
                    while words and len(window[j] + b' ' + words[0]) <= 32:
                        window[j] += b' ' + words.pop(0)
                    if len(window[j]) < 32:
                        if j == 2:
                            window[j] += EOF_CHAR*(32-len(window[j]))
                        else:
                            window[j] += b' '*(32-len(window[j]))

            if words:
                print("Not all words made it into this window")

            joined_lines = b''.join(window)
            joined_lines = pad_iv(joined_lines)
            print(joined_lines)
            f.write(joined_lines)
    if i.startswith("IV"):
        Data1Disk.insert('patched\\' + i)
    else:
        SystemDisk.insert('patched\\' + i)

"""with open('patched\\original_TALK.TXT', 'rb') as f:
    lines = f.readlines()
with open('patched\\TALK.TXT', 'wb') as f:
    for l in lines:
            l = l.replace(b'\x81\x40', b'  ')
            l = l.replace(b'\xe3\x80\x80', b'   ')
            l = l.replace(b'\xe3\x80', b'  ')
            l = l.replace(b'\x1a', b' ')
            if len(l.strip()) == 0:
                continue
            l = l.rstrip(b'\r\n')
            l = l.rstrip()
            print(l)
"""

SystemDisk.insert('patched\CR1.EXE')
