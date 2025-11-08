function getCart() {
  return JSON.parse(localStorage.getItem("cart") || "[]");
}

function saveCart(cart) {
  localStorage.setItem("cart", JSON.stringify(cart));
  const countElement = document.getElementById("cart-count");
  if (countElement) {
    try {
      const total = Array.isArray(cart) ? cart.reduce((s, it) => s + (Number(it.qty) || 0), 0) : 0;
      countElement.textContent = total;
    } catch (e) {
      countElement.textContent = cart.length;
    }
  }
}

function addToCart(product, silent = false) {
  let cart = getCart();
  
  const existingItem = cart.find(item => item.productid === product.productid);
  
  if (existingItem) {
    existingItem.qty = (Number(existingItem.qty) || 1) + 1;
  } else {
    cart.push({
      ...product,
      qty: 1
    });
  }
  
  saveCart(cart);
  
  if (!silent) {
    const title = product.product_name || product.name || product.description || product.title || 'Item';
    if (typeof showToast === 'function') {
      showToast(`${title} added to cart!`);
    } else {
      alert(`${title} added to cart!`);
    }
  }
}
document.addEventListener("DOMContentLoaded", () => {
  saveCart(getCart());
});
