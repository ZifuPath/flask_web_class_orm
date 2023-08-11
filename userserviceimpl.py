from flask_class_web.config import app,db
from flask_class_web.userservice import UserService
from flask_class_web.model import User
from flask_class_web.pwd_check import bcrypt,password_check


class UserSericeImpl(UserService):

    def __init__(self):
        db.create_all()

    def add_user(self,user):
        db.session.add(user)
        db.session.commit()
        return "Record added succussfuly"

    def update_user(self,dbuser,user):
        dbuser.firstname = user.firstname
        dbuser.lastname = user.lastname
        dbuser.dob = user.dob
        dbuser.mob = user.mob
        dbuser.email = user.email
        dbuser.qual = user.qual
        dbuser.cour = user.cour
        if password_check(user.pwd):
            dbuser.pwd = bcrypt.generate_password_hash(user.pwd)
            db.session.commit()
            return "User updated succussfully"
        return password_check(user.pwd)

    def get_user(self,uid):
        return User.query.filter_by(userid =uid).first()

    def get_all_user(self):
        return User.query.all()

    def delete_user(self,uid):
        dbuser = self.get_user(uid)
        if dbuser:
            db.session.delete(dbuser)
            db.session.commit()
            return 'record deleted'
        return "No record with given id"