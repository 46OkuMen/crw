import os
import shutil
from rominfo import SRC_DISK_DEMO, SRC_DISK_SYSTEM, SRC_DISK_DATA_1, SRC_DISK_DATA_2
from rominfo import DEST_DISK_DEMO, DEST_DISK_SYSTEM, DEST_DISK_DATA_1, DEST_DISK_DATA_2
from rominfo import DEMO_FILES, SYS_FILES, DATA_1_FILES, DATA_2_FILES
from romtools.disk import Disk
from romtools.patch import Patch

DemoSrc = Disk(SRC_DISK_DEMO)
SysSrc = Disk(SRC_DISK_SYSTEM)
Data1Src = Disk(SRC_DISK_DATA_1)
Data2Src = Disk(SRC_DISK_DATA_2)

DemoDest = Disk(DEST_DISK_DEMO)
SysDest = Disk(DEST_DISK_SYSTEM)
Data1Dest = Disk(DEST_DISK_DATA_1)
Data2Dest = Disk(DEST_DISK_DATA_2)

for src, dest, files in ((DemoSrc, DemoDest, DEMO_FILES), (SysSrc, SysDest, SYS_FILES), (Data1Src, Data1Dest, DATA_1_FILES), (Data2Src, Data2Dest, DATA_2_FILES)):
    for f in files:
        dest.extract(f, dest_path=os.curdir)
        shutil.copyfile(f, 'edited_' + f)
        src.extract(f, dest_path=os.curdir)

        patch_filename = f + '.xdelta'
        patch_destination = os.path.join('patch', patch_filename)
        filepatch = Patch(f, patch_destination, edited='edited_' + f)
        filepatch.create()
        print(patch_filename)

        os.remove(f)
        os.remove('edited_' + f)
