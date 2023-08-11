from flask import Flask, request, redirect, url_for, render_template,session,Blueprint
from flask_class_web.config import app,db
from flask_class_web.model import User,AdminUser,Staff,Courses,Batch
from flask_class_web.staffserviceImpl import StaffSericeImpl
from flask_class_web.batchseerviceImpl import BatchSericeImpl
from flask_class_web.userserviceimpl import UserSericeImpl
from flask_class_web.pwd_check import get_hash_password,get_password_from_hash,password_check


staffservice = StaffSericeImpl()
batchservice = BatchSericeImpl()
userservice = UserSericeImpl()

@app.route('/admin/staff/show_all',methods =['GET','POST'])
def show_staff():
    msg = ''
    stafflist = staffservice.get_all_staff()
    if not stafflist:
        msg = 'No records'
    return render_template('admin.html' ,page='admin',stafflist= stafflist,msg=msg, user = session['user_id'])

@app.route('/admin/staff/delete/<int:staffid>',methods =['GET','POST'])
def delete_staff(staffid):
    msg = ''
    if staffservice.get_staff(staffid):
        staffservice.delete_staff(staffid)
        msg = 'staff id deleted'
        return redirect(url_for('show_staff'))
    msg = 'staff id not found'
    return render_template('admin.html',page = 'admin',msg= msg,user = session['user_id'])

@app.route('/admin/staff/add',methods =['GET','POST'])
def add_staff():
    if request.method== 'POST':
        staffname = request.form.get('username')
        staffpwd = request.form.get('password')
        staff = Staff(staffname=staffname,staffpwd =staffpwd)
        staffservice.add_staff(staff)
        return redirect(url_for('show_staff'))
    return render_template('admin.html',page ='addstaff',user = session['user_id'])

@app.route('/admin/staff/edit/<int:staffid>',methods =['GET',])
def update_staff(staffid):
    session['staffid'] =staffid

    return render_template('admin.html',page ='updatestaff', user = session['user_id'])

@app.route('/admin/staff/edit/', methods=['POST'])
def update_staff1():
    if request.method== 'POST':
        sid = session['staffid']
        staffname = request.form.get('username')
        staffpwd = request.form.get('password')
        dbstaff = Staff(staffname =staffname,staffpwd =staffpwd)
        staffservice.update_staff(dbstaff,sid)
        session.pop('staffid',)
        return redirect(url_for('show_staff'))

@app.route('/admin/staff/assign/<int:staffid>',methods =['GET'])
def assign_staff(staffid):
    # print(staffid)
    session['stfid'] =staffid
    return render_template('admin.html', page ='assignstaff', stfid =session['stfid'],user = session['user_id'],stafflist =staffservice.get_all_staff()
    ,batchlist = batchservice.get_all_batch())

@app.route('/admin/staff/assign/',methods =['POST'])
def assign_staff1():
    if request.method == 'POST':
        staffid= session['stfid']
        dbid = request.form.getlist('bid')
        staffservice.assign_batch(staffid,dbid)
        session.pop('stfid', )
        return redirect(url_for('show_staff'))


@app.route('/admin/batch/show_all',methods =['GET','POST'])
def show_batch():
    msg = ''
    batchlist = batchservice.get_all_batch()
    if not batchlist:
        msg = 'No records'
    return render_template('admin.html' ,page='admin', batchlist= batchlist, msg=msg, user = session['user_id'])

@app.route('/admin/batch/delete/<int:batchid>',methods =['GET','POST'])
def delete_batch(batchid):
    msg = ''
    if batchservice.get_batch(batchid):
        batchservice.delete_batch(batchid)
        msg = 'batch id deleted'
        return redirect(url_for('show_batch'))
    msg = 'staff id not found'
    return render_template('assignstaff.html',user =session['user_id'],msg= msg)

@app.route('/admin/batch/add',methods =['GET','POST'])
def add_batch():
    if request.method== 'POST':
        batchcourse = request.form.get('batchcourse')
        batchtime = request.form.get('batchtime')
        batch = Batch(batchtime=batchtime,batchcourse =batchcourse)
        batchservice.add_batch(batch)
        return redirect(url_for('show_batch'))
    return render_template('admin.html',page ='addbatch',user = session['user_id'])


@app.route('/admin/batch/edit/<int:batchid>',methods =['GET'])
def update_batch(batchid):
    batch = batchservice.get_batch(batchid)
    session['batchid'] =batchid

    return render_template('admin.html',page ='editbatch', user = session['user_id'])

@app.route('/admin/batch/edit/', methods=['POST'])
def update_batch1():
    batchid = session['batchid']
    batchcourse = request.form.get('batchcourse')
    batchtime = request.form.get('batchtime')
    batch = Batch(batchcourse=batchcourse, batchtime=batchtime)
    batchservice.update_batch(batch, batchid)
    session.pop('batchid',)
    return redirect(url_for('show_batch'))

@app.route('/admin/user/show_user', methods=['GET','POST'])
def show_user():
    page = request.args.get('page', 1,type=int)
    userlist = User.query.paginate(per_page=5)
    msg = ''
    # userlist = userservice.get_all_user()
    if not userlist:
        msg= 'No records Found'
    return render_template('admin.html',page='admin',userlist =userlist,user =session['user_id'],msg =msg)

@app.route('/admin/user/delete/<int:uid>', methods=['GET','POST'])
def delete_user(uid):
    msg = ''
    user=userservice.get_user(uid)
    if user:
        userservice.delete_user(uid=uid)
        msg = f'userid {uid} deleted succussfuly'
    msg= 'No records Found'
    return render_template('admin.html',page='admin',userlist =userservice.get_all_user(),msg =msg,user =session['user_id'])

@app.route('/admin/user/add',methods =['GET','POST'])
def add_user():
    msg = ''
    if request.method== 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')

        dob = request.form.get('dob')
        mob = request.form.get('mob')
        email = request.form.get('email')
        qual = request.form.get('qual')
        cour = request.form.get('cour')
        pwd = request.form.get('password')

        if password_check(pwd):
            user = User(firstname=firstname,lastname=lastname,dob=dob,mob=mob,email=email,qual=qual,
                        cour= cour,pwd=get_hash_password(pwd),status ="APPROVED")
            userservice.add_user(user)
            return redirect(url_for('show_user'))
        return render_template('admin.html',page='adduser',msg =password_check(pwd),user =session['user_id'])
    return render_template('admin.html', page='adduser', msg=msg,user =session['user_id'])

@app.route('/admin/user/edit/<int:userid>',methods =['GET'])
def update_user(userid):
    user = userservice.get_user(userid)
    if user:
        session['userid'] =userid

    return render_template('admin.html',page ='edituser', user = session['user_id'],dummy =user  )

@app.route('/admin/user/edit', methods=['POST'])
def update_user1():
    msg= ''
    userid = session['userid']
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    dob = request.form.get('dob')
    mob = request.form.get('mob')
    email = request.form.get('email')
    qual = request.form.get('qual')
    cour = request.form.get('cour')
    pwd = request.form.get('password')
    if password_check(pwd):
        user = User(firstname=firstname, lastname=lastname,
                    dob=dob, mob=mob, email=email, qual=qual,
                    cour=cour, pwd=get_hash_password(pwd), status="APPROVED")
        dbuser =userservice.get_user(userid)
        userservice.update_user(dbuser,user)
        session.pop('userid',)
        msg = 'student updated succussfuly'
        page = request.args.get('page', 1, type=int)
        userlist = User.query.paginate(per_page=5)
        return render_template('admin.html',page='admin',
                               userlist =userlist,
                               user =session['user_id'],msg =msg)
    return render_template('admin.html', page='edituser' ,
                           msg = password_check(pwd),user =session['user_id'] )


@app.route('/admin/batch/assign/<int:batchid>',methods =['GET'])
def assign_student(batchid):
    # print(staffid)
    session['batchid'] =batchid
    return render_template('admin.html', page ='assignbatch',
                           user = session['user_id'],
                           userlist =userservice.get_all_user())

@app.route('/admin/batch/assign/',methods =['POST'])
def assign_student1():
    if request.method== 'POST':
        bid= session['batchid']
        print(bid)
        sid = request.form.getlist('sid')
        print(sid)
        batchservice.assign_student(sid,bid)
        session.pop('batchid', )
        return redirect(url_for('show_user'))

@app.route('/admin/user/status/<int:userid>', methods  =['GET'])
def status(userid):
    msg= ''
    session['sid'] =userid
    return render_template('admin.html' , page= 'status',user = session['user_id'])

@app.route('/admin/user/status/', methods  =['POST'])
def status1():
    msg= ''
    userid = session['sid']
    status=request.form.get('status')
    print(status)
    user = userservice.get_user(userid)
    print(user)
    user.status=status
    db.session.commit()
    msg= 'user status changed'
    return render_template('admin.html', msg = msg ,user = session['user_id'])



# if __name__ == '__main__':
#     import random
#     import datetime
#     import string
#     FIRSTNAME  = ['Firoz',  'Mandar' , 'John',  'Mahesh' , 'Hemant']
#     LASTNAME = ['Pathan' ,'Shinde' , 'Raut' , 'Vahadne' , 'Surale']
#     QUAL = ['Diploma' ,'Graduate' , 'PG']
#     COURSE = ['PYTHON' , 'JAVA' , 'AWS' , 'C']
#     # date = random.randint(1988, 1991)
#     # dob = datetime.date(random.randint(1988, 1991), random.randint(1, 12), random.randint(1, 28))
#     # print(dob)
#     for num in range(100):
#         firstname =FIRSTNAME[random.randint(0,4)] + str(num)
#         lastname =LASTNAME[random.randint(0,4)]
#         dob = datetime.date(random.randint(1988, 1991), random.randint(1, 12), random.randint(1, 28))
#         mob = '80874905'+str(random.randint(10,99))
#         email = firstname +str(random.randint(1988, 1991)) +'@'+'gmail.com'
#         qual = QUAL[random.randint(0,2)]
#         cour = COURSE[random.randint(0, 3)]
#         char_set = string.ascii_uppercase + string.digits +string.ascii_lowercase
#         password =''.join(random.sample(char_set * 6, 9))
#         pwd = get_hash_password(random.choice(password))
#         user = User(firstname=firstname, lastname=lastname, dob=dob, mob=mob, email=email, qual=qual,
#                     cour=cour, pwd=get_hash_password(pwd), status="APPROVED")
#         userservice.add_user(user)
#

# if __name__ == '__main__':
#     user = User.query.paginate (page =2)
#     print(user.per_page)
#     for us in user.items:
#         print(us)