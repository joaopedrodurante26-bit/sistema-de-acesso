let currentUser = null;

function showMessage(text, type = "info") {
  const node = document.querySelector("#message");
  node.textContent = text;
  node.dataset.type = type;
}

async function ensureAdmin() {
  try {
    currentUser = await window.API.getCurrentUser();
    if (currentUser.role !== "ADMIN") {
      window.API.redirectTo("./dashboard.html");
      return false;
    }
    return true;
  } catch (_) {
    window.API.redirectTo("./login.html");
    return false;
  }
}

function renderUsers(users) {
  const body = document.querySelector("#usersTableBody");
  body.innerHTML = "";

  users.forEach((user) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${user.id}</td>
      <td>${user.username}</td>
      <td>${user.role}</td>
      <td>${user.is_active ? "Sim" : "Não"}</td>
      <td class="actions">
        <button data-action="toggle-role" data-id="${user.id}" type="button">
          ${user.role === "ADMIN" ? "Tornar USER" : "Tornar ADMIN"}
        </button>
        <button data-action="toggle-active" data-id="${user.id}" type="button">
          ${user.is_active ? "Desativar" : "Ativar"}
        </button>
        <button data-action="delete" data-id="${user.id}" type="button">Excluir</button>
      </td>
    `;
    body.appendChild(row);
  });
}

async function fetchUsers() {
  try {
    const data = await window.API.apiRequest("/users", { method: "GET" });
    renderUsers(data.users || []);
  } catch (error) {
    showMessage(error.message, "error");
  }
}

async function createUser(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const username = form.username.value.trim();
  const password = form.password.value;
  const role = form.role.value;

  try {
    await window.API.apiRequest("/users", {
      method: "POST",
      body: JSON.stringify({ username, password, role, is_active: true }),
    });
    form.reset();
    showMessage("Usuário criado com sucesso.", "success");
    await fetchUsers();
  } catch (error) {
    showMessage(error.message, "error");
  }
}

async function handleTableClick(event) {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const id = Number(button.dataset.id);
  const action = button.dataset.action;

  try {
    if (action === "toggle-role") {
      const row = button.closest("tr");
      const roleText = row.children[2].textContent.trim();
      const newRole = roleText === "ADMIN" ? "USER" : "ADMIN";
      await window.API.apiRequest(`/users/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ role: newRole }),
      });
    }

    if (action === "toggle-active") {
      const row = button.closest("tr");
      const activeText = row.children[3].textContent.trim();
      const newStatus = activeText !== "Sim";
      await window.API.apiRequest(`/users/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ is_active: newStatus }),
      });
    }

    if (action === "delete") {
      await window.API.apiRequest(`/users/${id}`, {
        method: "DELETE",
      });
    }

    showMessage("Operação concluída.", "success");
    await fetchUsers();
  } catch (error) {
    showMessage(error.message, "error");
  }
}

async function logout() {
  try {
    await window.API.apiRequest("/auth/logout", { method: "POST" });
    window.API.redirectTo("./login.html");
  } catch (error) {
    showMessage(error.message, "error");
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const allowed = await ensureAdmin();
  if (!allowed) return;

  document.querySelector("#createUserForm").addEventListener("submit", createUser);
  document.querySelector("#usersTableBody").addEventListener("click", handleTableClick);
  document.querySelector("#logoutBtn").addEventListener("click", logout);

  await fetchUsers();
});
