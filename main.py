import random
import smtplib

# generate random passwords

def GeneratePassword():
    prefix = "Normet2019-"

    letters = list('abcdefghijklmnopqrstuvwxyz')

    number = random.randrange(100,1000)

    randomLetter = random.choice(letters)

    randomPass = prefix + randomLetter + str(number)

    return randomPass


# Email the password to the admin
def send_password_via_email():
    gmail_user = 'giftnakembetwa@gmail.com'  
    gmail_password = 'n8181818'

    sent_from = gmail_user  
    to = ['mcrider45g@gmail.com']  
    subject = 'NEW WIFI PASSWORD'  
    body = 'The new WIFI password is:\n %s' % (GeneratePassword(),)

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