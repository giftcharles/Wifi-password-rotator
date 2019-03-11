import random
import time
import smtplib
import selenium
from selenium import webdriver
import codecs
import datetime
import pywifi
from pywifi import const

# generate random passwords

def GeneratePassword():

    today = datetime.datetime.now().strftime('%d-%m-%Y')
    prefix = "Normet2019-"

    letters = list('abcdefghijklmnopqrstuvwxyz')

    number = random.randrange(100,1000)

    randomLetter = random.choice(letters)

    randomPass = prefix + randomLetter + str(number)

    print(randomPass)

    with codecs.open('logs.txt', 'a', 'utf-8') as f:
        f.write(today + " => " + randomPass + "\n")

    return [randomPass, today]


# Email the password to the admin
def send_password_via_email(genPass):
    gmail_user = 'giftnakembetwa@gmail.com'  
    gmail_password = 'n8181818'

    sent_from = gmail_user  
    to = ['mcrider45g@gmail.com', 'dykedvd@gmail.com']  
    subject = 'NEW WIFI PASSWORD'  
    body = 'The new WIFI password is:\n %s => %s' % (genPass[0], genPass[1],)

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

def connect_to_WIFI_connection_new_pass(genpass):
    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    profile = pywifi.Profile()
    profile.ssid = 'Travellers home'
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = genpass

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    assert iface.status() == const.IFACE_CONNECTED

if __name__ == "__main__":
    
    NewPassword = GeneratePassword()
    send_password_via_email(NewPassword)


    # Using Chrome to access web
    driver = webdriver.Chrome()
    # Open the website
    driver.get('http://192.168.1.1')

    user_box = driver.find_element_by_name('router_username')
    pass_box = driver.find_element_by_id('tbarouter_password')

    time.sleep(2)

    user_box.send_keys('admin')
    pass_box.send_keys('admin')

    time.sleep(2)

    # Click login
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
    WIFI_pass_box.send_keys(NewPassword[0])
    time.sleep(2)

    save_pass_button = driver.find_element_by_css_selector('.ssids #lt_btnApply')
    save_pass_button.click()

    time.sleep(5)
    connect_to_WIFI_connection_new_pass(NewPassword[0])

