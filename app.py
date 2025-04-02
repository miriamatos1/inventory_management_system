  
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Kết nối đến cơ sở dữ liệu SQLite
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

# Trang chính - Hiển thị sản phẩm
@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Thêm sản phẩm mới
@app.route('/add', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, quantity) VALUES (?, ?)', (name, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_product.html')

# Cập nhật sản phẩm
@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update_product(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        conn.execute('UPDATE products SET name = ?, quantity = ? WHERE id = ?', (name, quantity, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update_product.html', product=product)

# Xóa sản phẩm
@app.route('/delete/<int:id>')
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Báo cáo tồn kho
@app.route('/report')
def report():
    conn = get_db_connection()
    low_stock_products = conn.execute('SELECT * FROM products WHERE quantity < 10').fetchall()
    conn.close()
    return render_template('report.html', products=low_stock_products)

if __name__ == '__main__':
    app.run(debug=True)
