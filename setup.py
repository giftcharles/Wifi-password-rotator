from cx_Freeze import setup, Executable
import sys
import os

__APPPATH__ = os.getcwd() + '\\'

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

includefiles = [__APPPATH__ + "log/", __APPPATH__ + 'assets/']
executables = [Executable("WPR.py", base=None, icon=__APPPATH__ + 'assets/images/icon-normal.ico'),
                Executable("settings.py", base=base, icon=__APPPATH__ + 'assets/images/icon-cog.ico')]

packages = ["idna","selenium", "time", "smtplib", "codecs", "datetime", "pywifi", "gspread","oauth2client.service_account",
            "_pickle", "infi/systray", "pkg_resources._vendor", "wx", "subprocess", "logging", "secrets", "os"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files':includefiles,
        'build_exe': '\\executablex86'
    },

}

setup(
    name = "WPRsysTray",
    options = options,
    version = "1.2.0",
    description = 'Rotate router WIFI password',
    executables = executables
)