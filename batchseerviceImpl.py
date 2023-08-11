from flask_class_web.config import app,db
from flask_class_web.batchservice import BatchService
from flask_class_web.model import Staff,Batch,User



class BatchSericeImpl(BatchService):

    def __init__(self):
        db.create_all()

    def add_batch(self,batch):
        db.session.add(batch)
        db.session.commit()
        return "Record added succussfuly"

    def update_batch(self,dbbatch,bid):
        batch = self.get_batch(bid)
        batch.batchcourse = dbbatch.batchcourse
        batch.batchtime = dbbatch.batchtime
        db.session.commit()
        msg = "User updated succussfully"
        return msg

    def get_batch(self,bid):
        return Batch.query.filter_by(batchid =bid).first()

    def get_all_batch(self):
        return Batch.query.all()

    def delete_batch(self,bid):
        dbbatch = self.get_staff(bid)
        if dbbatch:
            db.session.delete(dbbatch)
            db.session.commit()
            msg = 'record deleted'
            return msg
        msg = "No record with given id"
        return msg


    def assign_student(self,sid,bid):
        dbuser = self.get_batch(bid)
        if dbuser:
            if type(sid)==list:
                BATCH = []
                for item in sid:
                    user= User.query.filter_by(userid = item).first()
                    if user:
                        user.b_id = bid
                        BATCH.append(user)
                    else:
                        return 'Batch id is incorrect'
                db.session.add_all(BATCH)
                db.session.commit()
                return 'Assignment of staff to batch completed'
            else:
                user = Batch.query.filter_by(userid=sid).first()
                if user:
                    user.b_id = bid
                else:
                    return 'Batch id is incorrect'
                db.session.add(user)
                db.session.commit()
            return 'Assignment of staff to batch completed'
        return "No record with given id"


