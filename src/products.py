from flask import Blueprint, render_template, request, redirect, flash, url_for
from database import mysql
import random


products = Blueprint('products', __name__, template_folder='templates', static_folder='static')

@products.route("/view_products", methods=['GET', 'POST'])
def menu():
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
    
    print(data)
    
    return render_template('data-table.html', dataset=data)

@products.route('/add_product', methods=['GET', 'POST'])
def add_product():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, category_name, description FROM digitronikdb.category")
    data = cursor.fetchall()
    
    if request.method == 'POST':
        # Get Form Fields
        product = request.form['product']
        category = request.form['category']
        price = request.form['price']
        stock = request.form['stock']
        picture = request.form['picture']
        numero_aleatorio = random.randint(1, 4)
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("""
            INSERT INTO digitronikDB.Product(product_name, Category_id, unit_price, stock, picture, discontinued, Supplier_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        """,
        (product, category, price, stock, picture, 0, numero_aleatorio))
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('Product Created', 'success')
        return redirect(url_for('products.menu'))
    return render_template('add_product.html', categories=data )

@products.route('/edit_product/<string:id>', methods=['GET', 'POST'])
def get_product(id):
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
        where p.id = %s
    """, [id])
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, category_name, description FROM digitronikdb.category")
    category_data = cursor.fetchall()
    
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_product.html', product=data[0], categories=category_data)

@products.route('/update_product/<string:id>', methods=['POST'])
def update_product(id):
    if request.method == 'POST':
        product = request.form['product']
        category = request.form['category']
        price = request.form['price']
        stock = request.form['stock']
        picture = request.form['picture']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE digitronikDB.Product
            SET 
                product_name = %s,
                Category_id = %s,
                unit_price = %s,
                stock = %s,
                picture = %s
            WHERE id = %s
        """, (product, category , price, stock, picture, id))
        mysql.connection.commit()
        return redirect(url_for('products.menu'))
    
@products.route('/delete_product/<string:id>', methods=['POST','GET'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM digitronikDB.Product WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for('products.menu'))