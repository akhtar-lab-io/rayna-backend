# 🍮 Rayna Homemade — F&B UMKM Web App

A full-stack web application built to digitalize order management for a real small-scale F&B business (UMKM), eliminating manual order recording and reducing data entry overhead.

**Live Demo:** [rayna-homemade.netlify.app](https://rayna-homemade.netlify.app)  
**Backend API:** [rayna-backend-update.vercel.app](https://rayna-backend-update.vercel.app)

---

## 🧩 Problem Statement

The business previously relied entirely on WhatsApp for receiving orders and Microsoft Excel for monthly sales recaps — requiring manual data entry for every single transaction. This created inefficiencies in record-keeping and made it difficult to track orders in real time.

**Rayna Homemade Web App** solves this by providing a digital storefront with an automated order recording system, so customer data flows directly into a database without any manual input.

---

## ✨ Features

- **Product Catalog** — Displays available F&B products with descriptions and pricing
- **Shopping Cart** — Add-to-cart functionality with quantity management
- **Order & Payment Form** — Captures customer details (name, address, WhatsApp number, delivery time, payment method)
- **Admin Panel** — View and manage incoming orders with status approval system
- **Automated Order Recording** — All transactions stored directly to database, ready for export

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask, Flask-CORS |
| Database | Supabase (PostgreSQL) |
| Frontend Hosting | Netlify |
| Backend Hosting | Vercel |

---

## 🏗️ System Architecture

```
Frontend (Netlify)
      │
      │  HTTP Requests
      ▼
Backend API (Vercel - Flask)
      │
      │  Supabase Python Client
      ▼
Database (Supabase - PostgreSQL)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/checkout` | Save cart items to orders table |
| POST | `/payment` | Save customer details + order items |
| GET | `/orders` | Retrieve all orders |
| GET | `/users` | Retrieve all order details |
| PUT | `/update-status/<id>` | Update order status |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.x
- Supabase account
- Vercel account

### 1. Clone the repository
```bash
git clone https://github.com/akhtar-lab-io/rayna-backend.git
cd rayna-backend
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file or set the following in your hosting platform:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
```

### 4. Set up database
Run the following SQL in your Supabase SQL Editor:
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount NUMERIC NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_detail (
    id SERIAL PRIMARY KEY,
    nama_lengkap TEXT,
    alamat_lengkap TEXT,
    metode_pembayaran TEXT,
    nomor_whatsapp TEXT,
    waktu_pengiriman TEXT,
    nama_item TEXT,
    quantity INTEGER,
    total_harga NUMERIC,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5. Run locally
```bash
python app.py
```

---

## 🚧 Challenges & Learnings

- **Backend development** — First time building a REST API with Flask; learned routing, request handling, and CORS configuration from scratch
- **Database migration** — Migrated from SQLite to Supabase (PostgreSQL) to solve Vercel's ephemeral filesystem limitation
- **API integration** — Connecting frontend JavaScript to a live backend API, handling async fetch requests and JSON responses
- **Deployment pipeline** — Setting up a split deployment (frontend on Netlify, backend on Vercel) with proper environment variable management

---

## 🗺️ Roadmap

- [ ] WhatsApp notification integration when new order arrives
- [ ] Monthly sales report export to Excel
- [ ] Product stock management
- [ ] Order history page for customers

---

## 👤 Author

**Rayyan Akhtar**  
GitHub: [@akhtar-lab-io](https://github.com/akhtar-lab-io)
