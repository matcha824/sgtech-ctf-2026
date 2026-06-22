const JWT_SECRET = "ZeroDay";
const AUTH_STORAGE_KEY = "Authorization";

const loginView = document.getElementById("login-view");
const dashboardView = document.getElementById("dashboard-view");
const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");

function extractBearerToken(value) {
  if (!value) return null;
  const trimmed = value.trim();
  if (trimmed.toLowerCase().startsWith("authorization: bearer ")) {
    return trimmed.slice("authorization: bearer ".length).trim();
  }
  if (trimmed.toLowerCase().startsWith("bearer ")) {
    return trimmed.slice("bearer ".length).trim();
  }
  return trimmed;
}

function saveAuthorizationHeader(tokenOrHeader) {
  const token = extractBearerToken(tokenOrHeader);
  if (!token) return;
  localStorage.setItem(AUTH_STORAGE_KEY, `Bearer ${token}`);
}

window.setAuthorizationHeader = saveAuthorizationHeader;

function getAuthorizationHeader() {
  return localStorage.getItem(AUTH_STORAGE_KEY);
}

function clearSession() {
  localStorage.removeItem(AUTH_STORAGE_KEY);
  renderLogin();
}

function renderLogin() {
  dashboardView.classList.add("hidden");
  loginView.classList.remove("hidden");
  loginMessage.textContent = "";
}

function accountCard(title, amount, detail) {
  return `
    <article class="account-card">
      <span>${title}</span>
      <strong>${amount}</strong>
      <small>${detail}</small>
    </article>
  `;
}

function renderGuestDashboard() {
  loginView.classList.add("hidden");
  dashboardView.classList.remove("hidden");
  dashboardView.innerHTML = `
    <div class="dashboard-header">
      <div>
        <p class="eyebrow">Member Portal</p>
        <h2>Welcome, Guest</h2>
      </div>
      <button class="secondary" onclick="clearSession()">Sign Out</button>
    </div>

    <div class="account-grid">
      ${accountCard("Everyday Checking", "$4,281.17", "Available balance")}
      ${accountCard("High-Yield Savings", "$12,554.02", "Projected monthly interest: $41.22")}
      ${accountCard("Rewards Credit", "$822.14", "Current statement balance")}
    </div>

    <section class="notice">
      <h3>Member Notice</h3>
      <p>Executive accounts are temporarily unavailable while Administrator privileges are being reviewed.</p>
    </section>

    <section class="content-card">
      <h3>Recent Transactions</h3>
      <ul class="transactions">
        <li><span>Payroll Deposit</span><strong>+$2,500.00</strong></li>
        <li><span>Apartment Rent</span><strong>-$1,800.00</strong></li>
        <li><span>Coffee Shop</span><strong>-$6.47</strong></li>
        <li><span>Motorcycle Insurance</span><strong>-$87.12</strong></li>
        <li><span>Guitar Center</span><strong>-$149.99</strong></li>
      </ul>
    </section>

    <footer class="footer-note">
      ZeroDay Credit Union &middot; Member Portal v1.2<br />
      For executive account issues, contact an administrator.
    </footer>
  `;
}

async function renderAdminDashboard() {
  loginView.classList.add("hidden");
  dashboardView.classList.remove("hidden");

  let flagText = "Access pending";
  try {
    const response = await fetch("/api/flag", {
      headers: { Authorization: getAuthorizationHeader() || "" }
    });
    if (response.ok) {
      const data = await response.json();
      flagText = data.flag;
    }
  } catch (_) {}

  dashboardView.innerHTML = `
    <div class="dashboard-header">
      <div>
        <p class="eyebrow">Executive Wealth Portal</p>
        <h2>Welcome, Gabriel Winter</h2>
        <p class="muted">Chief Executive Officer</p>
      </div>
      <button class="secondary" onclick="clearSession()">Sign Out</button>
    </div>

    <div class="account-grid">
      ${accountCard("Portfolio Value", "$12,487,225.84", "Consolidated assets")}
      ${accountCard("Checking", "$2,184,114.52", "Liquid operating funds")}
      ${accountCard("Brokerage", "$7,912,387.17", "Managed technology holdings")}
      ${accountCard("Private Equity", "$2,390,724.15", "Founder allocation")}
    </div>

    <section class="content-card executive-note">
      <h3>Executive Notes</h3>
      <p>The new authentication rollout is complete.</p>
      <p><strong>Security Review:</strong> JWT signing key rotation has been postponed for the seventh consecutive quarter.</p>
      <p class="flag-label">Access Code</p>
      <code>${flagText}</code>
    </section>
  `;
}

async function renderFromAuthorizationHeader() {
  const storedHeader = getAuthorizationHeader();
  if (!storedHeader) {
    renderLogin();
    return;
  }

  try {
    const response = await fetch("/api/session", {
      headers: { Authorization: storedHeader }
    });

    if (!response.ok) {
      renderLogin();
      return;
    }

    const data = await response.json();
    const payload = data.user;

    if (payload.name === "admin" && payload.role === "admin") {
      await renderAdminDashboard();
      return;
    }

    if (payload.name === "guest" && payload.role === "guest") {
      renderGuestDashboard();
      return;
    }
  } catch (_) {}

  renderLogin();
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
      loginMessage.textContent = "Unable to sign in.";
      return;
    }

    const data = await response.json();
    saveAuthorizationHeader(data.authorization);
    await renderFromAuthorizationHeader();
  } catch (_) {
    loginMessage.textContent = "Unable to sign in.";
  }
});

renderFromAuthorizationHeader();
