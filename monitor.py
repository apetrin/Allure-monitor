def send_email (message, subject, recipients):
    import smtplib
    from smtplib import SMTP_SSL
    from email.mime.text import MIMEText
    fromaddr = 'email@yandex.ru'
    server = SMTP_SSL('smtp.yandex.ru:465')
    msg = MIMEText(message)
    msg['Subject']=subject
    msg['To'] = ",".join(recipients)
    msg['From'] = "email@yandex.ru"
    server.ehlo()
    server.login('email@yandex.ru', 'superpassword')
    server.sendmail(fromaddr, recipients, msg.as_string())
    server.quit()


if __name__ == '__main__':
    from urllib2 import urlopen, Request
    from bs4 import BeautifulSoup
    import pickle
    import time
    import os
    from random import random

    time.sleep(37*random())
    req = Request("http://www.allurebox.ru/subscriptions", headers={ 'User-Agent': 'Mozilla/5.0' })
    f=urlopen(req)
    page=BeautifulSoup(f)
    alldivs = page.findAll('div')
    targetdivs=[]
    for div in alldivs: 
        try:
            if (div["class"]==["twelve","columns","alpha","omega","border", "box"]):
                targetdivs.append(div)
        except KeyError:
            continue
    currentLen = len(targetdivs)
    print "CurrentLen = ", currentLen

    f = file("allure_status", "r")
    oldLen = pickle.load(f)
    f.close()

    print "oldLen = ", oldLen

    if oldLen != currentLen:
        print "NEW VALUE, composing email!!!"
        message = """Attention \n \n New item discovered on Allure[Box] website 
        \n Old Number of Boxed: %i, NEW Number of Boxes: %i
        \n Please visit http://www.allurebox.ru/subscriptions
        """%(oldLen, currentLen )
        subject = "Allure[Box] monitor: new item"
        recipients = ['apetrin@mail.ru', 'marie.tsh@gmail.com']
        print "Sending emails!"
        send_email (message, subject, recipients)
        print "Email sent successfully!"

    f = file("allure_status", "w")
    oldLen = pickle.dump(currentLen,f)
    f.close()
