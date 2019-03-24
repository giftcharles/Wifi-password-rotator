# C:/Users/gift/AppData/Local/Programs/Python/Python36-32x86/python.exe setup.py build


import secrets
import time
import smtplib
import selenium
from selenium import webdriver
import codecs
import datetime
from datetime import timedelta
import pywifi
from pywifi import const
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import _pickle as cPickle
import requests
from infi.systray import SysTrayIcon
from selenium.webdriver.chrome.options import Options
import logging
import logging.handlers


def __setVariables():

    # global variables 
    global PIK 
    global EXTRA_EMAILS
    global REGISTRY
    global _PASSWORD_PREFIX
    global _GMAIL_USER
    global _GMAIL_USER_PASS
    global SSID
    global WaitAfterEmail
    global CARRIER
    global HOST_ADDRESS
    global HOST_USERNAME
    global HOST_PASSWORD
    global SERVICE_ACCOUNT_CREDENTIALS
    global HOUR_MINUTE
    global DAY_NIGHT
    global LOGGER
    global timeToClose 
    global environment
    global specifiedTimeToRunAfter

    environment = 'production'

    if environment == 'production':
        timeToClose = 60
    elif environment == 'development':
        timeToClose = 5

    # file logging configurations
    LOG_FILENAME = './log/logs.log'

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    LOGGER = logging.getLogger("LOGGER")
    LOGGER.setLevel(logging.DEBUG)

    Rotation_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=(1048576*5), backupCount=7
    )

    Rotation_handler.setFormatter(formatter)
    LOGGER.addHandler(Rotation_handler)

    #consoleHandler = logging.StreamHandler()
    #consoleHandler.setFormatter(formatter)
    #LOGGER.addHandler(consoleHandler)

    LOGGER.debug('#### %s: WPR LOGS START' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),) )


    try:
        PIK = './Profile_settings.pkl'

        with open(PIK, "rb") as f: 
            pickleData =  cPickle.load(f)
        
        LOGGER.debug('Unpickled profile settings file and loaded to pickleData')
        LOGGER.debug(pickleData)
    except Exception as e:
        LOGGER.debug('something went wrong! could not unpickle')
        LOGGER.debug('Exiting out of the run immidiately!')
        LOGGER.debug(e)
        raise SystemExit


    if pickleData != []:
        EXTRA_EMAILS = pickleData[0]['EXTRA_EMAILS']
        REGISTRY = pickleData[1]['REGISTRY']
        _PASSWORD_PREFIX = pickleData[2]['_PASSWORD_PREFIX']
        _GMAIL_USER = pickleData[3]['_GMAIL_USER']
        _GMAIL_USER_PASS = pickleData[4]['_GMAIL_USER_PASS']
        SSID = pickleData[5]['SSID']
        WaitAfterEmail = pickleData[6]['WaitAfterEmail']
        CARRIER = pickleData[7]['CARRIER']
        HOST_ADDRESS = pickleData[8]['HOST_ADDRESS']
        HOST_USERNAME = pickleData[9]['HOST_USERNAME']
        HOST_PASSWORD = pickleData[10]['HOST_PASSWORD']
        SERVICE_ACCOUNT_CREDENTIALS = pickleData[11]['SERVICE_ACCOUNT_CREDENTIALS']
        HOUR_MINUTE = pickleData[12]['HourMinute']
        DAY_NIGHT = pickleData[12]['DayNight']
        specifiedTimeToRunAfter = pickleData[13]['_USE_RUN_AFTER_BOOLEAN']

        LOGGER.debug('Global variables have been set')

 
def __get_checked_in_customer_emails():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_CREDENTIALS, scope)

    try:
        gc = gspread.authorize(credentials)

        wks = gc.open(REGISTRY).sheet1

        list_of_regestries = wks.get_all_values()

        i=0
        customers = list()
        email_list = list()
        for row in list_of_regestries:
            if i > 3:
                customers.append(row)    
            i+=1

        for customer in customers:
            if customer[2] == '':
                if customer[5] != '':
                    email_list.append(customer[5])

        email_list += EXTRA_EMAILS

        LOGGER.debug('Guest Email list downloaded from the guest registry')        
        LOGGER.debug(email_list)


        return email_list

    except Exception as e:
        LOGGER.debug(e)
        LOGGER.debug('retrying in 5...')
        time.sleep(5)
        return __get_checked_in_customer_emails()



def __GeneratePassword():

    today = datetime.datetime.now().strftime('%d-%m-%Y')

    letters = list('abcdefghijklmnopqrstuvwxyz')

    secretObject = secrets.SystemRandom()

    number = secretObject.randrange(100,1000)

    randomLetter = secrets.choice(letters)

    randomPass = _PASSWORD_PREFIX + randomLetter + str(number)

    LOGGER.debug("randomly generated password => %s" % (randomPass,))

    return [randomPass, today]


# Email the password to the admin
def send_password_via_email(genPassAndTime):

    if environment == 'development':
        return []

    sent_from = _GMAIL_USER  
    to = __get_checked_in_customer_emails()  
    subject = '(Kifumbu) NEW WIFI PASSWORD'  
    body = 'The new WIFI password is:\n %s \nIt will start being used %s seconds from now.\n\nYou will be notified if the password fails to change' % (genPassAndTime[0], int(WaitAfterEmail))

    email_text = 'From: %s \nTo: %s\nSubject: %s\n\n %s' % (sent_from, ", ".join(to), subject, body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(_GMAIL_USER, _GMAIL_USER_PASS)
        server.sendmail(sent_from, to, email_text)
        server.close()

        LOGGER.debug('Email(s) sent')

        return to

    except Exception as e:  
        LOGGER.debug('Something went wrong while sending emails')
        LOGGER.debug(e)
        LOGGER.debug('retrying in 5...')
        time.sleep(5)
        LOGGER.debug('retrying...')
        return send_password_via_email(genPassAndTime)

def __Email_guests_password_didnt_change(emailsList, FailedPassword):
    sent_from = _GMAIL_USER  
    to = emailsList  
    subject = '(Kifumbu)[ERROR] PASSWORD WAS NOT CHANGED'  
    body = 'The password %s from the last email, will not be in use due to a technical error, Keep using the last password unless we notify you otherwise.\n\n Sorry for any inconviniences' % (FailedPassword,)

    email_text = 'From: %s \nTo: %s\nSubject: %s\n\n %s' % (sent_from, ", ".join(to), subject, body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(_GMAIL_USER, _GMAIL_USER_PASS)
        server.sendmail(sent_from, to, email_text)
        server.close()

        LOGGER.debug('Email(s) sent')        
        
        return True

    except Exception as e:  
        LOGGER.debug('Something went wrong while sending emails')
        LOGGER.debug(e)
        LOGGER.debug('retrying in 5...')
        time.sleep(5)
        LOGGER.debug('retrying...')
        if __Email_guests_password_didnt_change(emailsList, FailedPassword):
            LOGGER.debug('Password change retraction emails sent')


def __connect_to_WIFI_connection_new_pass(NewPassword):
    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    try:
        iface.disconnect()
        LOGGER.debug('disconnected computer from the wifi')
    except Exception as e:
        LOGGER.debug('could not disconnect from the wifi connection')
        LOGGER.debug(e)
    time.sleep(1)
    try:
        assert iface.status() in\
            [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
    except Exception as e:
        LOGGER.debug('assert iface.status() failed')

    profile = pywifi.Profile()
    profile.ssid = SSID
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = NewPassword

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    try:
        assert iface.status() == const.IFACE_CONNECTED
    except Exception as e:
        LOGGER.debug('assert iface.status() failed')

def __log_todays_date():

    if environment == 'development':
        LOGGER.debug('no need to log the day in development mode')
        return False

    if specifiedTimeToRunAfter == False:
        LOGGER.debug('We are not runnnig the software after a specified time')
        return False
    
    today = datetime.datetime.now().strftime('%d-%m-%Y')

    try:
        saveFile = open('Last Change Date.dat', 'wb')

        cPickle.dump(today, saveFile)

        saveFile.close()

        LOGGER.debug('Todays randomly generated password has been logged')

        return True
    except Exception as e:
        LOGGER.debug(e)
        return False

def __has_changed_today():
    today = datetime.datetime.now().strftime('%d-%m-%Y')

    openFile = open('Last Change Date.dat', 'rb')

    LOGGER.debug('Checking the last save date')

    try:
        saveDate = cPickle.load(openFile)
    except:
        LOGGER.debug('Could not load the last save date, returning False')

        return False

    openFile.close()

    if saveDate == today:
        LOGGER.debug('The save date is today, cancelling...')
        return True

    elif saveDate != today:
        LOGGER.debug('The save date is not today, thus, stop the application')
        return False

def __is_in_hour_minute():
    now = datetime.datetime.now().strftime('%H:%M %p')
    passwordUpdateHour = datetime.datetime.strptime(HOUR_MINUTE + DAY_NIGHT.lower(), '%H:%M%p').strftime('%H:%M %p')  
    passwordUpdateHourplusOne = datetime.datetime.strptime(HOUR_MINUTE + DAY_NIGHT.lower(), '%H:%M%p') + timedelta(hours=1)
    passwordUpdateHourplusOne = passwordUpdateHourplusOne.strftime('%H:%M %p')  

    #if now > passwordUpdateHour and now < passwordUpdateHourplusOne:
    if now > passwordUpdateHour:
        LOGGER.debug('Its after the specified time, return true')
        return True
    else:
        LOGGER.debug('Its before the specified time, return false')
        return True


def __internet_connection():
    try:
        requests.get('http://216.58.192.142')
        LOGGER.debug('we do have an internet connection, return true')
        return True

    except Exception as e:
        LOGGER.debug('Its after the specified time, return true')
        LOGGER.debug(e)        
        return False

def __Connected_to_router():
    try:
        requests.get(HOST_ADDRESS)
        LOGGER.debug('Connected to HOST_ADDRESS: %s' % (HOST_ADDRESS,))
        return True

    except Exception as e:
        LOGGER.debug('Failed to connect to HOST_ADDRESS: %s' % (HOST_ADDRESS,))
        LOGGER.debug(e)
        return False

def TTCL_HostNav():
    
    NewPasswordAndTime = __GeneratePassword()

    emails = send_password_via_email(NewPasswordAndTime)
    LOGGER.debug('waiting for like %s seconds for Emails to be delivered' % (WaitAfterEmail,))
    time.sleep(WaitAfterEmail)

    options = Options()
    options.headless = True

    driver = webdriver.Chrome(chrome_options=options)
    
    driver.get(HOST_ADDRESS)

    user_box = driver.find_element_by_name('router_username')
    pass_box = driver.find_element_by_id('tbarouter_password')

    time.sleep(2)

    user_box.send_keys(HOST_USERNAME)
    time.sleep(1)
    pass_box.send_keys(HOST_PASSWORD)

    time.sleep(2)

    login_button = driver.find_element_by_id('btnSignIn')
    login_button.click()

    time.sleep(2)

    try:
        skip_setup_button = driver.find_element_by_id('lt_btnSkip')
        skip_setup_button.click()
        time.sleep(2)
    except Exception as e:
        LOGGER.debug('No introduction helper Dialogue box')                
        LOGGER.debug(e)        
        
    wireless_tab_button = driver.find_element_by_id('7')
    wireless_tab_button.click()

    time.sleep(2)

    WIFI_pass_box = driver.find_element_by_id('txtPasswd_0')
    WIFI_pass_box.clear()
    time.sleep(1)
    WIFI_pass_box.send_keys(NewPasswordAndTime[0])
    time.sleep(2)

    try:
        save_pass_button = driver.find_element_by_css_selector('.ssids #lt_btnApply')
        save_pass_button.click()
        LOGGER.debug('Apply button has been clicked and password has been saved')
        __log_todays_date()

    except Exception as e:
        LOGGER.debug('could not apply the new password')
        LOGGER.debug(e)
        LOGGER.debug('emailing guests about the issue in 5...')
        time.sleep(5)
        __Email_guests_password_didnt_change(emails, NewPasswordAndTime[0])
        return

    time.sleep(5)

    LOGGER.debug('Disconnect and try reconnecting to the router using the new password')
    __connect_to_WIFI_connection_new_pass(NewPasswordAndTime[0])

def __open_settings(systray):
    
    import subprocess
    
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen("settings.exe", startupinfo=startupinfo)    
        LOGGER.debug('settings.exe Opened')
    except Exception as e:
        LOGGER.debug('could not open "settings.exe"')
        LOGGER.debug(e)

def state_manage_trayIcon(systrayObj, navFunction):
    try:
        systrayObj.update(hover_text="Running... WPR", icon="icon-green.ico")
        navFunction()
        systrayObj.update(icon="icon-normal.ico")
        LOGGER.debug('waiting for %s seconds before closing...' % (timeToClose,))
        for i in range(timeToClose):
            systrayObj.update(hover_text="Completed the run, exiting in %s seconds" % (timeToClose - (i+1),))
            time.sleep(1)
    except Exception as err:
        systrayObj.update(hover_text="Failed to run", icon="icon-yellow.ico")
        LOGGER.debug(err)
        LOGGER.debug('something went wrong! while running TTCL Host Navigator')
        for i in range(timeToClose):
            systrayObj.update(hover_text="Failed the run, exiting in %s seconds" % (timeToClose - (i+1),))
            time.sleep(1)

def __end_log_runtime():
    LOGGER.debug('#### %s: WPR LOGS END' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),) )
    

def run():

    __setVariables()

    if not __Connected_to_router():
        __end_log_runtime()
        return

    if not __internet_connection():
        __end_log_runtime()
        return

    if __has_changed_today():
        __end_log_runtime()
        return
    
    if not __is_in_hour_minute():
        __end_log_runtime()
        return

    menu_options = (("Settings", None, __open_settings),)
    systray = SysTrayIcon("icon-normal.ico", "Wifi password rotater", menu_options)
    systray.start()
    LOGGER.debug('System tray icon has been started')

    LOGGER.debug('Carrier is %s, trying to navigate HOST if is supported' % (CARRIER,))

    if CARRIER == 'TTCL':
        state_manage_trayIcon(systray, TTCL_HostNav)
    else:
        LOGGER.debug('carrier is not supported, exiting')
        
        systray.update(hover_text="This Carrier is not supported yet!", icon="icon-yellow.ico")

        for i in range(timeToClose):
            systray.update(hover_text="Failed the run, exiting in %s seconds" % (timeToClose - (i+1),))
            time.sleep(1)
    
    systray.shutdown()

    LOGGER.debug('System tray icon shutdown')
    __end_log_runtime()
    
if __name__ == "__main__":
    #__setVariables()
    #__Connected_to_router()
    run()
    #__GeneratePassword()
