import os
from distutils.dir_util import copy_tree
from shutil import copyfile
from rominfo import SRC_DISK_DEMO, SRC_DISK_SYSTEM, SRC_DISK_DATA_1, SRC_DISK_DATA_2
from rominfo import DEST_DISK_DEMO, DEST_DISK_SYSTEM, DEST_DISK_DATA_1, DEST_DISK_DATA_2

VERSION = 'v1.0.0'

CRW_DIR = os.getcwd()
PACHY98_DIR = '../romtools/'
PACHY98_PATCHES_DIR = os.path.join(PACHY98_DIR, 'patch')

# Begin with an original set of disk images
copyfile(SRC_DISK_DEMO, DEST_DISK_DEMO)
copyfile(SRC_DISK_SYSTEM, DEST_DISK_SYSTEM)
copyfile(SRC_DISK_DATA_1, DEST_DISK_DATA_1)
copyfile(SRC_DISK_DATA_2, DEST_DISK_DATA_2)

# Commands to generate the target disk and patches
os.system('python reinsert.py')
os.system('python formatting.py')
os.system('python ugd.py')
os.system('python generate_patches.py')

# Copy the new patches into the dist patch folder
copy_tree('patch', os.path.join('dist', 'patch'))
# dist should contain:
# X pachy98.exe
# static - readme.txt
# X version.txt
# X Pachy98-CRW.json
# X patch
	# all patches.xdelta3
# X bin
	# NDC.exe
	# xdelta3.exe
# full_disk_patches
	# CRWDemo.xdelta3
	# CRWSystem.xdelta3
	# CRWData1.xdelta3
	# CRWData2.xdelta3
# static - Manual.pdf
# static - Box art.pdf

with open(os.path.join('dist', 'version.txt'), 'w') as f:
	f.write(VERSION)


# need a zip utility or library.
# a zip file with all of the above minus version.txt
# a zip file with all of the above except manual+box art, version.txt
# a zip file with all of the above minus manual+box art, pachy98.exe, patch, bin, version.txt

# do something with Pachy98-cfg.json


os.chdir(PACHY98_DIR)
pyinstaller_command = 'pyinstaller pachy98.spec'
os.system(pyinstaller_command)

# signtool commnad: signtool sign /a /t http://timestamp.comodoca.com pachy98.exe

os.chdir(CRW_DIR)
copyfile(os.path.join(PACHY98_DIR, 'dist', 'pachy98.exe'), os.path.join('dist', 'pachy98.exe'))
copyfile(os.path.join(PACHY98_DIR, 'Pachy98-CRW.json'), os.path.join('dist', 'Pachy98-CRW.json'))
copyfile(os.path.join(PACHY98_DIR, 'bin', 'NDC.EXE'), os.path.join('dist', 'bin', 'NDC.EXE'))
copyfile(os.path.join(PACHY98_DIR, 'bin', 'xdelta3.exe'), os.path.join('dist', 'bin', 'xdelta3.exe'))

# FTP commands?