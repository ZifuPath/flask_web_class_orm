from flask_class_web.config import db

class AdminUser(db.Model):
    aid = db.Column('aid',db.Integer(),primary_key=True)
    username = db.Column('ausername',db.String(50),unique=True)
    password = db.Column('apassword',db.String(30))
    role = db.Column('role' , db.String(50),default = 'admin')

class Staff(db.Model):
    staffid = db.Column('staffid',db.Integer(),primary_key=True)
    staffname = db.Column('staffname',db.String(100),unique=True)
    staffpwd = db.Column('apassword',db.String(100))
    role = db.Column('role', db.String(50), default='staff')
    batchrefs = db.relationship('Batch' , uselist = True ,lazy = True, backref ='staffref')

    @staticmethod
    def dummy_staff():
        return Staff(staffid = 0,staffname= '',staffpwd = '')

class Batch(db.Model):
    batchid = db.Column('bid',db.Integer(),primary_key=True)
    batchcourse = db.Column('bcourse',db.String(50))
    batchtime = db.Column('btime',db.String(50))
    st_id = db.Column('st_id',db.ForeignKey('staff.staffid' ),unique= False,nullable = True)
    userrefs = db.relationship('User', uselist=True, lazy=True ,backref ='batchref')

class User(db.Model):
    userid = db.Column('userid', db.Integer(), primary_key=True)
    firstname = db.Column('firstname', db.String(30))
    lastname = db.Column('lastname', db.String(30))
    dob = db.Column('dob', db.Date)
    mob = db.Column('mob', db.String(50))
    email = db.Column('email', db.String(50), unique = True)
    qual = db.Column('qual', db.String(30))
    cour = db.Column('cour', db.String(60))
    pwd = db.Column('u_pwd', db.String(100))
    status = db.Column('stat', db.String(60), default='PENDING',nullable = False)
    b_id = db.Column('b_id', db.ForeignKey('batch.bid'), nullable=True)
    # usid = db.Column('us_id', db.ForeignKey('user.uid'), unique=True, nullable=False)
    @staticmethod
    def dummy_user():
        return User(userid = 0,firstname= '',lastname = '',dob = '',
                        mob= '', email = '', qual='',course = '' ,pwd = '' , status= '')

# class User(db.Model):
#     username = db.Column('u_name', db.String(100), unique = True,primary_key=True)
#     pwd = db.Column('u_pwd', db.String(100))
#     status = db.Column('stat', db.String(60), default='PENDING')
#     usid = db.Column('us_id', db.ForeignKey('user_info.userid'), unique=True, nullable=False)
#
#     @staticmethod
#     def dummy_user_info():
#         return User(username = '', pwd = '' , usid = 0, status = '')
    # usid = db.Column('us_id', db.ForeignKey('userinfo.id'), unique=True, nullable=False)
    # stid = db.Column('status_id', db.ForeignKey('status.sid'), unique=True, nullable=False)

class Courses(db.Model):
    cid = db.Column('cid', db.Integer(), primary_key=True)
    course_name = db.Column('cnm', db.String(30))

# if __name__ =="__main__":
#     staff = Staff.query.filter_by(staffid=1).first()
#     print(staff.batchrefs)
#     for item in staff.batchrefs:
#         batchid = item.batchid
#         batch = Batch.query.filter_by(batchid=batchid).first()
#         print(batch)
#     db.drop_all()
#     db.create_all()
#     A1 = AdminUser(username='zorif', password='56789')
#     S1= Staff(staffname = 'ABCD1' , staffpwd = 'Abcd@1234')
#     S2 = Staff(staffname='ABCD2', staffpwd='Abcd@5678')
#     B1= Batch(batchcourse = "PYTHON" , batchtime = 'MORNING')
#     B2 = Batch(batchcourse = "JAVASCRIPT" , batchtime = 'MORNING')
#     B3 = Batch(batchcourse="PYTHON", batchtime='EVENING')
#     S1.batchrefs.extend([B1,B2])
#     # S1.batchref.a
#     db.session.add(A1)
#     db.session.add_all([S1,S2])
#     db.session.add_all([B1,B2,B3])
#
#     db.session.commit()