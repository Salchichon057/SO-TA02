from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from flask_mysqldb import MySQL


from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['MYSQL_HOST'] = '20.168.118.97'
app.config['MYSQL_USER'] = 'digitronik'
app.config['MYSQL_PASSWORD'] = 'digitronik'
app.config['MYSQL_DB'] = 'digitronikDB'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)

app.config['ENV'] = 'development'

@app.route('/home')
def index():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
        p.product_name as product,
        c.category_name as category,
        p.stock as stock,
        p.unit_price as price,
        p.picture as picture
        FROM
        digitronikDB.Product p INNER JOIN digitronikDB.Category c
        ON p.Category_id = c.id
    """
    )
    # cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    print(data)
    
    return render_template('cards.html', dataset=data)

if __name__ == '__main__':
    app.run(debug=True)