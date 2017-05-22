from romtools.disk import Disk
from rominfo import DEST_DISK_DEMO, DEST_DISK_DATA_1, DEST_DISK_DATA_2, DEST_DISK_SYSTEM, EOF_CHAR

SystemDisk = Disk(DEST_DISK_SYSTEM)
DemoDisk = Disk(DEST_DISK_DEMO)
Data1Disk = Disk(DEST_DISK_DATA_1)
Data2Disk = Disk(DEST_DISK_DATA_2)

titols =['TITOL.TXT',]
ninmus = ['NINMU1.TXT', 'NINMU2.TXT', 'NINMU3.TXT', 'NINMU4.TXT', 'NINMU5.TXT', 'NINMU6.TXT',
          'NINMU7.TXT', 'NINMU8.TXT']
ivs = ['IV1.TXT', 'IV2.TXT', 'IV3.TXT', 'IV4.TXT', 'IV5.TXT', 'IV6.TXT',
       'IV7.TXT', 'IV8.TXT', 'IV9.TXT', 'TALK.TXT']

#ninmus = ['NINMU1.TXT', 'TITOL.TXT']
#ivs = ['IV1.TXT', 'TALK.TXT']

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

def pad_iv9(l):
    """Pad an IV*.TXT line with spaces to 80 characters.
       Need to overwrite previous dialogue rather than end early.
    """
    if len(l) > 80:
        l = l[:78]
        l += b'\r\n'
    elif len(l) < 80:
        l.rstrip(b'\r\n')
        l = l + b' '*(78 - len(l))
        l += b'\r\n'
    assert len(l) == 80
    return l

# For the NINMU*.TXT files, each line must be an even number of characters.
for n in titols:
    with open('patched\original_' + n, 'rb') as f:
        lines = f.readlines()

    with open('patched\\' + n, 'wb') as f:
        print(lines)
        for l in lines:
            print(repr(l))
            print(len(l))
            if len(l) != 50:
                words = l.split(b' ')
                formatted_lines = []
                print(words)
                while words:
                    thisline = []
                    while len(b' '.join(thisline)) < 50 and words:
                        if len(b' '.join(thisline) + words[0]) + 1 <= 50:
                            thisline.append(words.pop(0))
                        else:
                            break
                    formatted_line = b' '.join(thisline)
                    deficit = 50 - len(formatted_line)
                    formatted_line += b' '*deficit
                    assert len(formatted_line) == 50
                    formatted_lines.append(formatted_line)
                #print(formatted_lines)


        for l in formatted_lines:
            print(l)
            f.write(l)
        if n == 'TITOL.TXT':
            f.write(b'\x1a')
            #f.truncate(0x3b1)
    DemoDisk.insert('patched\\' + n)

for n in ninmus:
    with open('patched\original_' + n, 'rb') as f:
        lines = f.readlines()

    with open('patched\\' + n, 'wb') as f:
        print(lines)
        for l in lines:
            if len(l) > 50:
                l = l.strip(b'\r\n')
                words = l.split(b' ')
                formatted_lines = []
                while words:
                    thisline = []
                    while len(b' '.join(thisline)) <= 50 and words:
                        if len(b' '.join(thisline) + words[0]) + 1 <= 50:
                            thisline.append(words.pop(0))
                        else:
                            break
                    formatted_line = b' '.join(thisline)
                    if len(formatted_line) <= 48:
                        deficit = 48 - len(formatted_line)
                        formatted_line += b' '*deficit
                        formatted_line += b'\r\n'
                    elif len(formatted_line) == 49:
                        formatted_line += b' '
                    else:
                        pass
                    print(formatted_line)
                    assert len(formatted_line) == 50, len(formatted_line)
                    formatted_lines.append(formatted_line)

            else:
                formatted_lines = [l, ]

            for l in formatted_lines:
                if len(l) % 2 == 1:
                    just_the_line = l.split(b'\r\n')[0]
                    l = just_the_line + b" " + b'\r\n'
                print(l)
                f.write(l)

        f.write(EOF_CHAR)
    DemoDisk.insert('patched\\' + n)

# For IV*.TXT files, each window must be 80 characters long, with 32-character lines.
# Pad with the EOF char after text is done.
for i in ivs:
    with open('patched\original_' + i, 'rb') as f:
        lines = f.readlines()

    with open('patched\\' + i, 'wb') as f:
        if i[2] == '9':
            LINE_LENGTH = 34
        else:
            LINE_LENGTH = 32
        for l in lines:
            l = l.replace(b'\x81\x40', b'  ')
            l = l.replace(b'\xe3\x80\x80', b'   ')
            l = l.replace(b'\xe3\x80', b'  ')
            l = l.replace(b'\x1a', b' ')
            l = l.replace(b'\xef\xbb\xbf', b' ')
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
                    while words and len(window[j] + b' ' + words[0]) <= LINE_LENGTH:
                        window[j] += b' ' + words.pop(0)
                    if len(window[j]) < LINE_LENGTH:
                        if j == 2:
                            window[j] += EOF_CHAR*(LINE_LENGTH-len(window[j]))
                        else:
                            window[j] += b' '*(LINE_LENGTH-len(window[j]))

            if words:
                print("Not all words made it into this window")

            joined_lines = b''.join(window)
            joined_lines = pad_iv(joined_lines)
            print(joined_lines)
            f.write(joined_lines)
    if i.startswith("IV") and int(i[2]) < 5:
        Data1Disk.insert('patched\\' + i)
    elif i.startswith("IV") and 5 <= int(i[2]) < 9:
        Data2Disk.insert('patched\\' + i)
    elif i.startswith("IV") and 9 == int(i[2]):
        DemoDisk.insert('patched\\' + i)
    else:
        SystemDisk.insert('patched\\' + i)

# END.TXT needs to be padded to 38 chars per line. And needs the right EOF char.

"""
with open('patched\\original_TALK.TXT', 'rb') as f:
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
    SystemDisk.insert('patched\\TALK.TXT')
"""

#SystemDisk.insert('patched\CR1.EXE')
