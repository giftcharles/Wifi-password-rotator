import random
import time
import smtplib
import selenium
from selenium import webdriver
import codecs
import datetime
import pywifi
from pywifi import const
import gspread
from oauth2client.service_account import ServiceAccountCredentials

EXTRA_EMAILS = ['giftnakembetwa@gmail.com', 'mcrider45g@gmail.com']
REGISTRY = "T.H Registry"
_PASSWORD_PREFIX = "Normet2019-"
_GMAIL_USER = 'giftnakembetwa@gmail.com'
_GMAIL_USER_PASS = 'n8181818'
SSID = 'Travellers home'
WaitAfterEmail = 300
CARRIER = 'TTCL'

def get_checked_in_customer_emails():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('Registry-f2600ffbcc35.json', scope)

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

    print(email_list)

    return email_list



def GeneratePassword():

    today = datetime.datetime.now().strftime('%d-%m-%Y')

    letters = list('abcdefghijklmnopqrstuvwxyz')

    number = random.randrange(100,1000)

    randomLetter = random.choice(letters)

    randomPass = _PASSWORD_PREFIX + randomLetter + str(number)

    print(randomPass)

    with codecs.open('logs.log', 'a', 'utf-8') as f:
        f.write(today + " => " + randomPass + "\n")

    return [randomPass, today]


# Email the password to the admin
def send_password_via_email(genPassAndTime):
    gmail_user = _GMAIL_USER  
    gmail_password = _GMAIL_USER_PASS

    sent_from = gmail_user  
    to = get_checked_in_customer_emails()  
    subject = '(Kifumbu) NEW WIFI PASSWORD'  
    body = 'The new WIFI password is:\n %s' % (genPassAndTime[1],)

    email_text = 'From: %s \nTo: %s\nSubject: %s\n\n %s' % (sent_from, ", ".join(to), subject, body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:  
        print('Something went wrong...')

def connect_to_WIFI_connection_new_pass(NewPassword):
    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)
    try:
        assert iface.status() in\
            [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
    except:
        pass

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
    except:
        pass

def TTCL_HostNav():
    
    NewPasswordAndTime = GeneratePassword()

    send_password_via_email(NewPasswordAndTime)
    time.sleep(WaitAfterEmail)

    driver = webdriver.Chrome()

    driver.get('http://192.168.1.1')

    user_box = driver.find_element_by_name('router_username')
    pass_box = driver.find_element_by_id('tbarouter_password')

    time.sleep(2)

    user_box.send_keys('admin')
    time.sleep(1)
    pass_box.send_keys('Normet')

    time.sleep(2)

    login_button = driver.find_element_by_id('btnSignIn')
    login_button.click()

    time.sleep(2)

    try:
        skip_setup_button = driver.find_element_by_id('lt_btnSkip')
        skip_setup_button.click()
        time.sleep(2)
    except:
        pass

    wireless_tab_button = driver.find_element_by_id('7')
    wireless_tab_button.click()

    time.sleep(2)

    WIFI_pass_box = driver.find_element_by_id('txtPasswd_0')
    WIFI_pass_box.clear()
    time.sleep(1)
    WIFI_pass_box.send_keys(NewPasswordAndTime[0])
    time.sleep(2)

    save_pass_button = driver.find_element_by_css_selector('.ssids #lt_btnApply')
    save_pass_button.click()

    time.sleep(5)
    connect_to_WIFI_connection_new_pass(NewPasswordAndTime[0])
