document.addEventListener("DOMContentLoaded", async () => {
  await loadProducts();

  document.getElementById("searchBtn").addEventListener("click", async () => {
    const keyword = document.getElementById("searchBox").value;
    await loadProducts(keyword);
  });
});

async function loadProducts(keyword = "") {
  const productList = document.getElementById("product-list");
  productList.innerHTML = "<p>Loading products...</p>";

  try {
    const products = keyword
      ? await apiRequest(`/products/search?keyword=${keyword}`)
      : await apiRequest("/products");

    if (!Array.isArray(products) || products.length === 0) {
      productList.innerHTML = "<p>No products found.</p>";
      return;
    }

    productList.innerHTML = products
      .map(
        (p) => `
        <div class="product-card">
          <img src="assets/images/default-product.jpg" alt="Product Image" />
          <h3>${p.description}</h3>
          <p class="price">₹${(p.rating * 100 || 499).toFixed(2)}</p>
          <button onclick='addToCart(${JSON.stringify(p)})'>Add to Cart</button>
        </div>`
      )
      .join("");
  } catch (err) {
    productList.innerHTML = `<p style="color:red;">Error loading products.</p>`;
  }
}
