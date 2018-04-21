import cx_Freeze
import sys

if sys.platform =="win32":
    base = "Win32GUI"

executables =[cx_Freeze.Executable("webcralscraper.py",base = base, icon="icon.ico")]
cx_Freeze.setup(name ="WebCralScraper",options={"build_exe": {"packages" :["Tkinter","sys","selenium","re","xlsxwriter","PIL"],"include_files":["icon.ico","Webcralscraper.png","phantomjs.exe"]}},version="1.0",description="Developed by Chandan Chainani",executables=executables)
