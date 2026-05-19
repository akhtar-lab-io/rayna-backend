from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from flask_cors import CORS

# --- Setup Flask
app = Flask(__name__, static_url_path='', static_folder='script')
CORS(app, resources={r"/*": {"origins": "https://raynae-commerce.netlify.app/"}})

# --- Path ke database (fix di folder 'database')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'orders.db')
print("📍 File database digunakan:", db_path)

if not os.path.exists(os.path.join(BASE_DIR, 'database')):
    os.makedirs(os.path.join(BASE_DIR, 'database'))


# --- Fungsi koneksi DB
def get_db_connection():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# --- Buat tabel
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_detail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lengkap TEXT,
            alamat_lengkap TEXT,
            metode_pembayaran TEXT,
            nomor_whatsapp TEXT,
            waktu_pengiriman TEXT,
            nama_item TEXT,
            quantity INTEGER,
            total_harga REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# --- Home
@app.route('/')
def home():
    return "Rayna API jalan boss!"

#--- Approval session
@app.route('/update-status/<int:user_id>', methods=['PUT'])
def update_status(user_id):
    try:
        data = request.get_json()
        new_status = data.get("status")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE order_detail SET status = ? WHERE id = ?", (new_status, user_id))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Status updated"}), 200
    except Exception as e:
        print("❌ Error update status:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# --- API Cart dummy
@app.route('/api/cart')
def get_cart_items():
    cart_items = [
        {'name': 'Brownies Coklat', 'price': 25000},
        {'name': 'Cookies Kacang', 'price': 15000}
    ]
    return jsonify(cart_items)

# --- Checkout Cart
@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()

        for item in data:
            name = item.get('name')
            price = item.get('price')
            quantity = item.get('quantity')
            total = price * quantity

            cursor.execute(
                "INSERT INTO orders (product_name, quantity, total_amount) VALUES (?, ?, ?)",
                (name, quantity, total)
            )

        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Order berhasil disimpan"}), 200

    except Exception as e:
        print("❌ Error di /checkout:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Data user saat payment
@app.route('/payment', methods=['POST'])
def payment():
    try:
        data = request.get_json()
        cart_items = data.get("items", [])  # Ambil keranjang dari frontend

        conn = get_db_connection()
        cursor = conn.cursor()

        for item in cart_items:
            total = item['price'] * item['quantity']
            cursor.execute('''
                INSERT INTO order_detail (
                    nama_lengkap,
                    alamat_lengkap,
                    metode_pembayaran,
                    nomor_whatsapp,
                    waktu_pengiriman,
                    nama_item,
                    quantity,
                    total_harga
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['nama_lengkap'],
                data['alamat_lengkap'],
                data['metode_pembayaran'],
                data['nomor_whatsapp'],
                data['waktu_pengiriman'],
                item['name'],
                item['quantity'],
                total
            ))

        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Data user & pesanan disimpan"}), 200

    except Exception as e:
        print("❌ Error di /payment:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Lihat semua orders
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
        rows = cursor.fetchall()
        orders = [dict(row) for row in rows]
        conn.close()
        return jsonify(orders), 200

    except Exception as e:
        print("❌ Error di /orders:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Lihat semua data user
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM order_detail ORDER BY created_at DESC")
        rows = cursor.fetchall()
        users = [dict(row) for row in rows]
        conn.close()
        return jsonify(users), 200

    except Exception as e:
        print("❌ Error di /users:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Start App
if __name__ == '__main__':
    create_tables()
    app.run(port=5050, debug=True)
