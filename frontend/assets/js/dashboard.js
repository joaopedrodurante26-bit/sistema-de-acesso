function showDashboardMessage(text, type = "info") {
  const node = document.querySelector("#message");
  node.textContent = text;
  node.dataset.type = type;
}

async function loadDashboard() {
  try {
    const user = await window.API.getCurrentUser();
    document.querySelector("#username").textContent = user.username;
    document.querySelector("#role").textContent = user.role;

    if (user.role === "ADMIN") {
      document.querySelector("#adminCard").hidden = false;
    }
  } catch (error) {
    window.API.redirectTo("./login.html");
  }
}

async function logout() {
  try {
    await window.API.apiRequest("/auth/logout", { method: "POST" });
    window.API.redirectTo("./login.html");
  } catch (error) {
    showDashboardMessage(error.message, "error");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadDashboard();
  document.querySelector("#logoutBtn").addEventListener("click", logout);
});
