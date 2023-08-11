from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.template_folder = 'templates'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:abcdef@localhost/clapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=False
db = SQLAlchemy(app)
app.secret_key = 'super secret key'