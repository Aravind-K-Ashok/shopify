(async function(){
  const placeholder = document.getElementById('site-header');
  if (!placeholder) return;
  try {
    const res = await fetch('header.html');
    if (!res.ok) throw new Error('Failed to fetch header.html');
    const html = await res.text();
    placeholder.innerHTML = html;

    const customerID = localStorage.getItem('customerID');
    const loginLink = placeholder.querySelector('#login-link');
    const profileLink = placeholder.querySelector('#profile-link');
    const logoutBtn = placeholder.querySelector('#logout-btn');
    const cartCount = placeholder.querySelector('#cart-count');

    // Toggle visibility
    const isLoggedIn = customerID && customerID.trim() !== '' && !isNaN(customerID);
    if (loginLink) loginLink.style.display = isLoggedIn ? 'none' : 'inline';
    if (profileLink) profileLink.style.display = isLoggedIn ? 'inline' : 'none';
    if (logoutBtn) logoutBtn.style.display = isLoggedIn ? 'inline' : 'none';

    // Update cart count
    try {
      const cart = JSON.parse(localStorage.getItem('cart') || '[]');
      cartCount && (cartCount.textContent = Array.isArray(cart) ? cart.length : 0);
    } catch (e) {
      cartCount && (cartCount.textContent = '0');
    }

    // Logout handler
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('customerID');
        localStorage.removeItem('cart');
        // Update UI immediately
        if (loginLink) loginLink.style.display = 'inline';
        if (profileLink) profileLink.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'none';
        cartCount && (cartCount.textContent = '0');
        // small delay then reload to refresh page-specific state
        setTimeout(() => location.reload(), 300);
      });
    }

  } catch (err) {
    console.error('header.js error:', err);
  }
})();
