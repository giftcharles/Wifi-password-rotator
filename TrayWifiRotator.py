from infi.systray import SysTrayIcon
import time
def say_hello(systray):
    print("Hello, Gift")

def do_meth(systray):
    print('doing meth')

def on_quit_callback(systray):
    print('the program just quit on you, what a shame!')    
menu_options = (("Say Hello", None, say_hello),("Do Meth", None, do_meth),)
systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options, on_quit=on_quit_callback)
systray.start()