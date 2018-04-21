
import sys
from cx_Freeze import setup, Executable

if sys.platform =="win32":
    base = "Win32GUI"
    
options = {
    'build_exe': {
        'compressed': True,
        'includes_files': [
            "icon.ico",
            "phantomjs.exe"
        ],
        'path': sys.path + ['modules']
    }
}


executables = [
	Executable("webcralscraper6.py",
	base = base,
	icon="icon.ico")
]

setup(name='advanced_cx_Freeze_sample',
      version='1.0',
      description='Developed by Chandan Chainani',
      options=options,
      executables=executables
      )
