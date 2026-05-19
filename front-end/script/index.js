// Add to cart biasa
document.querySelectorAll('.add-cart').forEach(button => {
    button.addEventListener('click', () => {
      const name = button.dataset.name;
      const price = parseInt(button.dataset.price);
      const cart = JSON.parse(localStorage.getItem('cart')) || [];
  
      const existing = cart.find(item => item.name === name);
      if (existing) {
        existing.quantity += 1;
      } else {
        cart.push({ name, price, quantity: 1 });
      }
  
      localStorage.setItem('cart', JSON.stringify(cart));
      alert("✅ Ditambahkan ke keranjang!");
    });
  });
  
  // Pilih ukuran (Lasagna)
  function pilihUkuran(nama) {
    let ukuran = prompt("Pilih ukuran (500ml / 700ml):");
    if (!ukuran) {
      alert("Ukuran tidak boleh kosong!");
      return;
    }
  
    ukuran = ukuran.trim().toLowerCase();
  
    if (ukuran !== '500ml' && ukuran !== '700ml') {
      alert("Ukuran tidak valid! Pilih 500ml atau 700ml");
      return;
    }
  
    const finalName = `${nama} (${ukuran})`;
    const price = ukuran === "700ml" ? 35000 : 27000;
  
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const exist = cart.find(item => item.name === finalName);
  
    if (exist) exist.quantity += 1;
    else cart.push({ name: finalName, price, quantity: 1 });
  
    localStorage.setItem("cart", JSON.stringify(cart));
    alert(`✅ ${finalName} ditambahkan ke keranjang!`);
  }
  