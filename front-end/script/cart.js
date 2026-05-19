document.addEventListener("DOMContentLoaded", () => {
  const cartContainer = document.getElementById("cart-items");
  const totalElement = document.getElementById("total");

  function loadCart() {
    const cartItems = JSON.parse(localStorage.getItem("cart")) || [];
    cartContainer.innerHTML = "";
    let total = 0;

    if (cartItems.length === 0) {
      cartContainer.innerHTML = "<p>Keranjang kosong.</p>";
    } else {
      cartItems.forEach((item, index) => {
        const el = document.createElement("div");
        el.className = "cart-item";
        const subtotal = item.price * item.quantity;
        el.innerHTML = `
          <p>
            <strong>${item.name}</strong>
            <button class="minus" data-index="${index}">−</button>
            <span>${item.quantity}</span>
            <button class="plus" data-index="${index}">+</button>
          </p>
          <p>Rp ${subtotal.toLocaleString("id-ID")}</p>
          <button class="remove" data-index="${index}">❌</button>
        `;
        cartContainer.appendChild(el);
        total += subtotal;
      });
    }

    totalElement.textContent = `Rp ${total.toLocaleString("id-ID")}`;
  }

  // Load awal
  loadCart();

  // Aksi pada tombol: plus, minus, remove
  cartContainer.addEventListener("click", function (e) {
    const index = parseInt(e.target.dataset.index);
    let cartItems = JSON.parse(localStorage.getItem("cart")) || [];

    if (e.target.classList.contains("plus")) {
      cartItems[index].quantity += 1;
    } else if (e.target.classList.contains("minus")) {
      cartItems[index].quantity -= 1;
      if (cartItems[index].quantity <= 0) {
        cartItems.splice(index, 1);
      }
    } else if (e.target.classList.contains("remove")) {
      cartItems.splice(index, 1);
    }

    localStorage.setItem("cart", JSON.stringify(cartItems));
    loadCart();
  });

  // Tombol Checkout
  document.getElementById("checkoutBtn").addEventListener("click", () => {
    const cartItems = JSON.parse(localStorage.getItem("cart")) || [];
    if (cartItems.length === 0) {
      alert("Keranjang kosong!");
    } else {
      window.location.href = "payment.html";
    }
  });
});
