import subprocess
import glob
import os

subprocess.run(['pyuic5', '-o', '../ui_mainwindow.py', '../forms/mainwindow.ui'])

subprocess.run(['pyrcc5', '-o', '../appresources_rc.py', '../appresources.qrc'])

# translations
# for tsfile in glob.glob('../translations/*.ts'):
#     basename = os.path.basename(tsfile)
#     subprocess.run(['lrelease', tsfile, '-qm', '../translations/' + os.path.splitext(basename)[0] + '.qm'])
