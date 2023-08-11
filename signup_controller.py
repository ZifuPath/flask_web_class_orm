from flask import render_template ,request ,flash,session ,redirect,url_for,Blueprint
from flask_class_web.config import app,db
from flask_class_web.model import *
from flask_class_web.pwd_check import password_check ,mail_otp , get_hash_password , get_password_from_hash
from flask_class_web.userservice import UserService
from flask_class_web.userserviceimpl import UserSericeImpl
from flask_class_web.admin_controller import *
from flask_class_web.staff_controller import *
from flask_class_web.user_controller import *
import random

auth = Blueprint('auth', __name__)


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            msg = 'Email ID already exist'

        elif len(email) < 4 :
            msg = 'Email id should be correct'

        elif len(first_name) < 2:
            msg = 'Length of first name should be more than 2'

        elif password1 != password2:
            msg  ='password doesnt match'

        elif password_check(password1):
            msg = password_check(password1)
            if msg == True:
                msg = 'Email authorization required'

                formdata = request.form
                password = get_hash_password(password1)
                temp_user = User(firstname=formdata.get('firstname'),
                                          lastname=formdata.get('lastname'),
                                          dob=formdata.get('dob'),
                                          mob=formdata.get('mob'),
                                          email=formdata.get('email'),
                                          qual=formdata.get('qual'),
                                          cour=formdata.get('cour'),
                                      pwd = password,)
                db.session.add(temp_user)
                db.session.commit()


                # temp_user = User(username = email, pwd = password ,usid = temp_user_info.userid)
                #
                # db.session.add(temp_user)
                # db.session.commit()
                # otp = mail_otp(email)
                otp = random.randint(100000, 999999)
                print(otp)
                session['response'] = str(otp)
                session['user'] = temp_user.email
                return render_template('email_auth.html' , page= 'email_auth',msg =msg , user = temp_user )

    return render_template('signup.html', msg = msg)

@app.route('/email_auth' , methods = ['GET', 'POST'])
def email_check():
    msg = ''
    if request.method == 'POST':
        OTP = request.form.get('OTP')
        username = session['user']
        user = User.query.filter_by(email= username).first()
        print(user.status)
        print(OTP)
        if 'response' in session:

            resp = session['response']
            if resp == OTP:
                msg = 'Account Created Succusfully'
                user.status = 'APPROVED'
                db.session.commit()
                session.pop('user',)
                session.pop('response')
                return render_template('home.html', msg= msg)
            else:

                msg = 'incorrect OTP'
                return render_template('email_auth.html',page = 'email_reg', msg = msg)

    return render_template('email_auth.html')

@app.route('/login', methods =['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('email')
        hpassword = request.form.get('password')
        user = User.query.filter_by(email=username).first()


        if not username:
            flash('username is empty',category='error')
            msg = 'username is empty'
            return render_template('login.html',msg = msg)
        if not hpassword:
            flash('password is empty',category='error')
            msg = 'password is empty'
            return render_template('login.html', msg = msg)

        if user:
            if get_password_from_hash(user.pwd,hpassword):
                if user.status == 'APPROVED':
                    msg = 'User login succusfully'
                    session['user_id'] = user.userid
                    return render_template('user.html',user = user.firstname ,msg =msg)
                msg = f'user status is{user.status}'
                return render_template('login.html' , msg = msg)
            else:
                msg = 'password is incorrect'
                return render_template('login.html',msg = msg , user = user)

    return render_template('login.html')

@app.route('/logout', methods =['GET'])
def logout():
    msg = ''
    session.pop('user_id',)
    return render_template('home.html')

@app.route('/admin_login', methods =['GET','POST'])
def admin_login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = AdminUser.query.filter_by(username=username).first()
        staff = Staff.query.filter_by(staffname=username).first()
        if admin:
            if admin.password == password:
                flash('Admin login succusfully', category='succuss')
                msg = 'Admin login succusfully'
                session['user_id'] = admin.username

                return render_template('admin.html',page = 'admin',user= admin.username , msg=msg,role ='admin')
            else:
                msg = 'Password is incorrect'
                return render_template('admin_login.html', msg=msg )

        elif staff:
            if staff.staffpwd == password:
                flash('Admin login succusfully', category='succuss')
                msg = 'Admin login succusfully'
                session['user_id'] = staff.staffname

                return render_template('admin.html', page = 'staff',user = staff.staffname,  msg=msg,role ='staff')
            else:
                msg = 'Password is incorrect'
                return render_template('admin_login.html', msg=msg)
        else:
            msg = 'Username is not present'
        return render_template('admin_login.html', user = admin , msg=msg)
    # if session['user_id']:
    #     if AdminUser.query.filter_by(aid=session['user_id']).first():
    #         page = 'admin'
    #     else:
    #         page = 'staff'
    #     return render_template('admin.html' ,user = session['user_id'] , page=page)
    return render_template('admin_login.html' ,msg =msg)

@app.route('/forget_pwd', methods =['GET','POST'])
def forgot_password():
    msg = ''
    if request.method == 'POST':
        # otp = mail_otp(email)
        otp = random.randint(100000, 999999)
        print(otp)
        session['response'] = str(otp)
        session['user'] = request.form.get('email')
        msg = 'OTP generated sent your email'
        return render_template('email_auth.html' , page = 'change_pwd' ,msg= msg)
    return render_template('forget_pwd.html')

@app.route('/change_pwd', methods =['GET','POST'])
def change_pwd():
    msg = ''
    if request.method == 'POST':
        OTP = request.form.get('OTP')
        # get_hash_password(password)
        email = session['user']
        user = User.query.filter_by(email=email).first()
        if user:
            print(user.status)
            print(OTP)
            if 'response' in session:

                resp = session['response']
                if resp == OTP:
                    msg = 'OTP Validated '
                    db.session.commit()
                    session.pop('response')
                    return render_template('change_pwd.html', msg=msg)
                else:

                    msg = 'incorrect OTP'
                    return render_template('email_auth.html', page='email_reg', msg=msg)
            else:
                msg = 'Email id does not registered'
                return redirect(url_for('sign_up'))
    return render_template('change_pwd.html')

@app.route('/pwd_check', methods =['GET','POST'])
def pwd_check():
    msg = ''
    if request.method == 'POST':
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password1')
        if pass1==pass2:
            val = password_check(pass1)
            if val:
                email = session['user']
                user = User.query.filter_by(email=email).first()
                pwd = get_hash_password(pass1)
                user.pwd = pwd
                db.session.commit()
                msg = 'password changed succussfuly'
                session.pop('user')
                return render_template('login.html', msg=msg)

            else:
                return render_template('change_pwd.html', msg=val)


        return render_template('change_pwd', msg=msg)

    return redirect(url_for('login'))

@app.route('/admin_home', methods =['GET'])
def admin():
    user =AdminUser.query.filter_by(username = session['user_id']).first()
    render_template('admin.html',user =user ,page ='admin')

@app.route('/staff_home', methods =['GET'])
def staff():
    user = Staff.query.filter_by(staffname=session['user_id']).first()
    render_template('admin.html',user=session['user_id'],page='staff')

