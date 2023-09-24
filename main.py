from flask import render_template, request, redirect, url_for, flash, session, jsonify
from database import mysql
from app import app
from src.products import products


app.register_blueprint(products)

@app.route("/")
def index():
    response  = app.make_response(redirect('/home'))
    return response

@app.route('/home', methods=['GET', 'POST'])
def cards():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
		p.id as id,
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
    data = cur.fetchall()
    # print(data)
    return render_template('landing.html', dataset=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Customer WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()

        if user is not None:
            return redirect('/view_products')
        else:
            flash('Credenciales incorrectas')
            return redirect('/login')

    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)