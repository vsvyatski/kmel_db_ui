import subprocess

subprocess.run(
    ['pylupdate5', '-translate-function', '_translate', '../driveutils.py', '../mainwindow.py',
     '../preferencesdialog.py', '../ui_aboutdialog.py', '../ui_mainwindow.py', '../ui_preferencesdialog.py', '-ts',
     '../translations/kenwood_db_gen_en.ts', '../translations/kenwood_db_gen_es.ts',
     '../translations/kenwood_db_gen_ru.ts'])
