from flask_class_web.config import app,db
from flask_class_web.staffservice import StaffService
from flask_class_web.model import Staff,Batch
from flask_class_web.pwd_check import bcrypt,password_check


class StaffSericeImpl(StaffService):

    def __init__(self):
        db.create_all()

    def add_staff(self,staff):
        db.session.add(staff)
        db.session.commit()
        msg = "Record added succussfuly"
        return msg

    def update_staff(self,dbstaff,sid):
        staff = self.get_staff(sid)

        staff.staffname = dbstaff.staffname
        staff.staffpwd = dbstaff.staffpwd
        db.session.commit()
        msg = "User updated succussfully"
        return msg


    def get_staff(self,sid):
        return Staff.query.filter_by(staffid =sid).first()

    def get_all_staff(self):
        return Staff.query.all()

    def delete_staff(self,uid):
        dbstaff = self.get_staff(uid)
        if dbstaff:
            db.session.delete(dbstaff)
            db.session.commit()
            return 'record deleted'
        return "No record with given id"

    def assign_batch(self,sid,bid):
        dbuser = self.get_staff(sid)
        if dbuser:
            if type(bid)==list:
                BATCH = []
                for item in bid:
                    batch= Batch.query.filter_by(batchid = item).first()
                    if batch:
                        batch.st_id = sid
                        BATCH.append(batch)
                    else:
                        return 'Batch id is incorrect'
                db.session.add_all(BATCH)
                db.session.commit()
                return 'Assignment of staff to batch completed'
            else:
                batch = Batch.query.filter_by(batchid=bid).first()
                if batch:
                    batch.st_id = sid
                else:
                    return 'Batch id is incorrect'
                db.session.add(batch)
                db.session.commit()
            return 'Assignment of staff to batch completed'
        return "No record with given id"

