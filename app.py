from flask import Flask

app = Flask(__name__, template_folder='./src/templates', static_folder='./src/static')

app.config['ENV'] = 'development' 
app.config['DEBUG'] = True
app.secret_key = "my_super_secret_key"

