const API_BASE_URL = "http://127.0.0.1:5000/api";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let data = {};
  try {
    data = await response.json();
  } catch (_) {
    data = {};
  }

  if (!response.ok) {
    const message = data.error || "Request failed";
    const error = new Error(message);
    error.status = response.status;
    error.payload = data;
    throw error;
  }

  return data;
}

async function getCurrentUser() {
  const data = await apiRequest("/auth/me", { method: "GET" });
  return data.user;
}

function redirectTo(path) {
  window.location.href = path;
}

window.API = {
  apiRequest,
  getCurrentUser,
  redirectTo,
};
