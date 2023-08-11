from flask_bcrypt import Bcrypt

from flask_class_web.config import app
def password_check(passwd):
    SPECIAL_WORD = ['$', '@', '#', '%']
    msg = ''
    val = True
    if len(passwd) < 6:
        msg = 'length should be at least 6'
        val = False
    elif len(passwd) > 20:
        msg ='length should not be greater than 20'
        val = False
    elif not any(char.isdigit() for char in passwd):
        msg = 'Password should have at least one numeral'
        val = False
    elif not any(char.isupper() for char in passwd):
        msg = 'Password should have at least one uppercase letter'
        val = False
    elif not any(char.islower() for char in passwd):
        msg ='Password should have at least one lowercase letter'
        val = False
    elif not any(char in SPECIAL_WORD for char in passwd) :
        msg = 'Password should have at least one of the symbols $@#'
        val = False
    if val:
        return val
    return msg

bcrypt = Bcrypt(app)

def get_hash_password(password):
    # print('before hash')
    hash = bcrypt.generate_password_hash(password)
    # print('inside hash function before save..!',hash)
    return hash

def get_password_from_hash(hpass,opwd):
    print('before check dbpassword {}, userentered {}'.format(hpass,opwd))
    return bcrypt.check_password_hash(hpass,opwd)

import smtplib

import random




def mail_otp(email):
    sender_mail = ""
    rec_mail = email
    otp = random.randint(100000,999999)
    pwd = ''
    password = pwd
    messege = f"EMAIL is sent to otp authorization of account /n" \
              f"The OTP is given as {otp}"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_mail, password)
    print("login Sucess")

    server.sendmail(sender_mail, rec_mail, messege)
    print("Email Sent to", rec_mail)
    return otp
if __name__ == '__main__':
    msg = password_check('')
    print(msg)
    # pwd = ''
    # hpassword = get_hash_password(pwd)
    # password  = get_password_from_hash(hpassword,pwd)
    # print(password)
    # email = ''
    # mail_otp(email)