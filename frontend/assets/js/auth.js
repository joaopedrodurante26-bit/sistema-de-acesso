function showMessage(target, text, type = "info") {
  target.textContent = text;
  target.dataset.type = type;
}

async function handleLoginSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const messageBox = document.querySelector("#message");
  const username = form.username.value.trim();
  const password = form.password.value;

  try {
    await window.API.apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    window.API.redirectTo("./dashboard.html");
  } catch (error) {
    showMessage(messageBox, error.message, "error");
  }
}

async function handleRegisterSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const messageBox = document.querySelector("#message");
  const username = form.username.value.trim();
  const password = form.password.value;

  try {
    await window.API.apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    showMessage(messageBox, "Conta criada com sucesso. Faça login.", "success");
    form.reset();
    setTimeout(() => window.API.redirectTo("./login.html"), 900);
  } catch (error) {
    showMessage(messageBox, error.message, "error");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const page = document.body.dataset.page;
  const form = document.querySelector("form");
  const messageBox = document.querySelector("#message");

  if (messageBox) {
    showMessage(messageBox, "", "info");
  }

  if (!form) return;

  if (page === "login") {
    form.addEventListener("submit", handleLoginSubmit);
  }

  if (page === "register") {
    form.addEventListener("submit", handleRegisterSubmit);
  }
});
