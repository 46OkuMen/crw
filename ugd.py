from romtools.disk import Disk
from rominfo import DEST_DISK_DEMO, DEST_DISK_DATA_1, DEST_DISK_SYSTEM

#SystemDisk = Disk(DEST_DISK_SYSTEM)
#DemoDisk = Disk(DEST_DISK_DEMO)
Data1Disk = Disk(DEST_DISK_DATA_1)

Data1Disk.insert('patched\\' + 'FACE00.UGD')