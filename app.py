from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os

# --- Setup Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":[
                     "https://rayna-homemade.netlify.app",
                       "http://localhost:3000",
                      "https://rayna-react-project.vercel.app",
                       ]}})

# --- Setup Supabase
# Kedua variable ini diisi di Vercel Environment Variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Home
@app.route('/', methods=['GET'])
def home():
    return "API nya jalan"

# --- Approval / Update Status Order
@app.route('/update-status/<int:user_id>', methods=['PUT'])
def update_status(user_id):
    try:
        data = request.get_json()
        new_status = data.get("status")

        supabase.table("order_detail") \
            .update({"status": new_status}) \
            .eq("id", user_id) \
            .execute()

        return jsonify({"status": "success", "message": "Status updated"}), 200

    except Exception as e:
        print("❌ Error update status:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Checkout Cart
@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        data = request.get_json()
        rows = []

        for item in data:
            name = item.get('name')
            price = item.get('price')
            quantity = item.get('quantity')
            total = price * quantity
            rows.append({
                "product_name": name,
                "quantity": quantity,
                "total_amount": total
            })

        supabase.table("orders").insert(rows).execute()
        return jsonify({"status": "success", "message": "Order berhasil disimpan"}), 200

    except Exception as e:
        print("❌ Error di /checkout:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Payment (data user + detail item)
@app.route('/payment', methods=['POST'])
def payment():
    try:
        data = request.get_json()
        cart_items = data.get("items", [])
        rows = []

        for item in cart_items:
            total = item['price'] * item['quantity']
            rows.append({
                "nama_lengkap":       data['nama_lengkap'],
                "alamat_lengkap":     data['alamat_lengkap'],
                "metode_pembayaran":  data['metode_pembayaran'],
                "nomor_whatsapp":     data['nomor_whatsapp'],
                "waktu_pengiriman":   data['waktu_pengiriman'],
                "nama_item":          item['name'],
                "quantity":           item['quantity'],
                "total_harga":        total,
                "status":             "pending"
            })

        supabase.table("order_detail").insert(rows).execute()
        return jsonify({"status": "success", "message": "Data user & pesanan disimpan"}), 200

    except Exception as e:
        print("❌ Error di /payment:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Lihat semua orders
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        result = supabase.table("orders") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()
        return jsonify(result.data), 200

    except Exception as e:
        print("❌ Error di /orders:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Lihat semua data user / order detail
@app.route('/users', methods=['GET'])
def get_users():
    try:
        result = supabase.table("order_detail") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()
        return jsonify(result.data), 200

    except Exception as e:
        print("❌ Error di /users:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Start App (local only, Vercel gak pake ini)
if __name__ == '__main__':
    app.run(port=5050, debug=True)

# --- End point baru buat ngambil data produk dari database Supabase
@app.route('/products', methods=['GET'])
def get_products():
    try:
        result = supabase.table("products") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()
        return jsonify(result.data), 200
    except Exception as e:
        print("❌ Error di /products:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
    
    
