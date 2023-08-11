from flask_class_web.config import db,app
from flask_class_web.model import *
from flask import render_template, request, session, Blueprint
from flask_class_web.admin_controller import userservice,staffservice,batchservice

staff = Blueprint('staff', __name__)

@app.route('/staff/show_batch', methods = ['GET'])
def show_staff_batch():
    staffname = session['user_id']
    staff = Staff.query.filter_by(staffname=staffname).first()
    print(staff)
    batchlist = staff.batchrefs
    return render_template('staff.html' ,batchlist = batchlist ,user =session['user_id'])
    # return render_template('admin.html',user=session['user_id'],page='staff')

@app.route('/staff/batch/user/<int:batchid>', methods = ['GET'])
def show_staff_user(batchid):
    batch = batchservice.get_batch(batchid)
    userlist = batch.userrefs
    return render_template('staff.html' ,userlist = userlist ,user =session['user_id'])