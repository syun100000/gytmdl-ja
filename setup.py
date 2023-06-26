from cx_Freeze import setup, Executable
import sys

# GUI=有効, CUI=無効 にする
if sys.platform == 'win32' : base = 'Win32GUI'
# exe にしたい python ファイルを指定
exe = Executable(script = 'gytmdl_gui.py',
                 base = base, icon='gytmdl_gui.ico')
 
# セットアップ
setup(name = 'Youtube Music Downloader',
      version = '1.0.0',
      description = 'Youtube Music Downloader',
      executables = [exe])

