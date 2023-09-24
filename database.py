from app import app
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') or '20.168.118.97'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER') or 'digitronik'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD') or 'digitronik'
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') or 'digitronikDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)