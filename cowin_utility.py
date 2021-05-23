#!/usr/bin/python

import re
import email
import smtplib

def colored(r, g, b, text):
    #return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)
    return text

def checkPincode(pin):   
    regex = '^[1-9]\d{5}$'
    if(re.search(regex, pin)):   
        return True   
    else:   
        return False

def checkMailId(email):   
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex, email)):   
        return True   
    else:   
        return False 

def sendMail(username, password, sendtoname, sub, content):
    if username != 'dummy':
        email_msg = email.message.EmailMessage()
        email_msg["Subject"] = sub + " > Date - Center - AgeLimit - TotalCapacity - 1stDoseCapacity - 2ndDoseCapacity"
        email_msg["From"] = username
        email_msg["To"] = username
        email_msg.set_content(content)
        try:
            with smtplib.SMTP(host='smtp.gmail.com', port='587') as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(username, password)
                server.send_message(email_msg, username, sendtoname)
                server.close()
        except smtplib.SMTPAuthenticationError:
            print(colored(255, 0, 0, "\nMail not sent, Username or Password not accepted. Pls fill valid entries.."))
    print("\n\n" + content ) 

#if __name__ == "__main__":
#    print("nothing to do")