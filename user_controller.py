from flask_class_web.config import db,app
from flask_class_web.model import *
from flask import render_template, request, session ,redirect,url_for,Blueprint
from flask_class_web.admin_controller import userservice,staffservice,batchservice

student = Blueprint('student', __name__)

@app.route('/user/detail', methods = ['GET'])
def show_user_detail():
    userid = session['user_id']
    student = userservice.get_user(userid)
    print(student)
    return render_template('user.html' ,student = student ,user =student.firstname)

@app.route('/user/edit/', methods = ['GET','POST'])
def edit_user_detail():
    msg = ''
    userid = session['user_id']
    user = userservice.get_user(userid)

    if request.method == 'POST':
        userid = session['user_id']
        user = userservice.get_user(userid)
        user.firstname = request.form.get('firstname')
        user.lastname = request.form.get('lastname')
        user.dob = request.form.get('dob')
        user.mob = request.form.get('mob')
        user.email = request.form.get('email')
        user.qual = request.form.get('qual')
        user.cour = request.form.get('cour')
        db.session.commit()
        return redirect(url_for('show_user_detail'))
    return render_template('user.html',user =user.firstname ,page ='edit', dummy = user)