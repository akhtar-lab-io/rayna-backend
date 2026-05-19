// Load data orders
fetch("http://127.0.0.1:5050/orders")
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector("#orderTable tbody");
    data.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${item.id}</td>
        <td>${item.product_name}</td>
        <td>${item.quantity}</td>
        <td>Rp ${item.total_amount}</td>
        <td>${item.created_at}</td>
      `;
      tbody.appendChild(tr);
    });
  });

// Load data user & tombol aksi
fetch("http://127.0.0.1:5050/users")
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector("#userTable tbody");
    data.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${item.id}</td>
        <td>${item.nama_lengkap}</td>
        <td>${item.alamat_lengkap}</td>
        <td>${item.metode_pembayaran}</td>
        <td>${item.nomor_whatsapp}</td>
        <td>${item.waktu_pengiriman}</td>
        <td>${item.created_at}</td>
        <td>
          <button onclick="updateStatus(${item.id}, 'approved')">✅</button>
          <button onclick="updateStatus(${item.id}, 'rejected')">❌</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  });

function updateStatus(userId, status) {
  fetch(`http://127.0.0.1:5050/update-status/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ status })
  })
  .then(res => res.json())
  .then(res => {
    if (res.status === "success") {
      alert("✅ Status diperbarui!");
      location.reload();
    } else {
      alert("❌ Gagal update: " + res.message);
    }
  });
}
