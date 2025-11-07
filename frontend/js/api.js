const BASE_URL = "http://127.0.0.1:8000";

async function apiRequest(endpoint, method = "GET", params = null) {
  let url = `${BASE_URL}${endpoint}`;
  let options = { method, headers: { "Content-Type": "application/json" } };

  if (method === "GET" && params) {
    url += "?" + new URLSearchParams(params);
  } else if (params) {
    options.body = JSON.stringify(params);
  }

  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
