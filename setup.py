from cx_Freeze import setup, Executable
import sys


base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

includefiles = ["./log/", './GUI/bitmaps/icon-cog.png', './GUI/bitmaps/save-32.png', './GUI/bitmaps/start-green-play-icon-1.png', './GUI/bitmaps/iconfinder_lowercase_letter_x_red_3052270.png', 'icon-green.ico', 'icon-yellow.ico', 'icon-normal.ico', 'icon-normal.png', 'Registry-f2600ffbcc35.json', 'Profile_settings.pkl', 'Last Change Date.dat', 'chromedriver.exe', 'credentials.json']
executables = [Executable("WPR.py", base=None, icon='icon-normal.ico'), Executable("settings.py", base=None, icon='icon-cog.ico')]

packages = ["idna","selenium","random", "time", "smtplib", "codecs", "datetime", "pywifi", "gspread","oauth2client.service_account",
            "_pickle", "infi/systray", "pkg_resources._vendor", "wx", "subprocess", "logging" ]
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
    version = "0.1",
    description = 'Rotate router WIFI password',
    executables = executables
)