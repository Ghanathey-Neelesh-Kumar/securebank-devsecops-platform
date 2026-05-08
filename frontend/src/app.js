console.log("SecureBank frontend loaded");

const API_BASE_URL = "/api";

const apiStatus = document.getElementById("api-status");
const accountsContainer = document.getElementById("accounts");
const transactionsContainer = document.getElementById("transactions");
const auditEventsContainer = document.getElementById("audit-events");
const transferForm = document.getElementById("transfer-form");
const transferResult = document.getElementById("transfer-result");

const totalAccounts = document.getElementById("total-accounts");
const totalBalance = document.getElementById("total-balance");
const totalTransactions = document.getElementById("total-transactions");
const totalAuditEvents = document.getElementById("total-audit-events");

function setText(element, value) {
  if (element) {
    element.textContent = value;
  }
}

function formatCurrency(value) {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
  }).format(Number(value));
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || `Request failed: ${response.status}`);
  }

  return data;
}

async function checkApiHealth() {
  try {
    const data = await fetchJson("/health");

    if (apiStatus) {
      apiStatus.textContent = `${data.service} is ${data.status}`;
      apiStatus.classList.remove("error");
    }
  } catch (error) {
    console.error("Health check failed:", error);

    if (apiStatus) {
      apiStatus.textContent = "API unavailable";
      apiStatus.classList.add("error");
    }
  }
}

async function loadAccounts() {
  try {
    const data = await fetchJson(`${API_BASE_URL}/accounts`);

    setText(totalAccounts, data.count);

    const total = data.accounts.reduce(
      (sum, account) => sum + Number(account.balance),
      0
    );

    setText(totalBalance, formatCurrency(total));

    if (!accountsContainer) return;

    accountsContainer.innerHTML = data.accounts
      .map(
        (account) => `
          <article class="account-card">
            <div class="account-top">
              <div class="account-number">${account.account_number}</div>
              <div class="account-type">${account.account_type}</div>
            </div>

            <div class="account-owner">
              ${account.user.full_name} • ${account.currency}
            </div>

            <div class="balance">${formatCurrency(account.balance)}</div>
          </article>
        `
      )
      .join("");
  } catch (error) {
    console.error("Failed to load accounts:", error);

    if (accountsContainer) {
      accountsContainer.innerHTML = `<div class="empty-state">Failed to load accounts: ${error.message}</div>`;
    }
  }
}

async function loadTransactions() {
  try {
    const data = await fetchJson(`${API_BASE_URL}/transactions`);

    setText(totalTransactions, data.count);

    if (!transactionsContainer) return;

    if (data.count === 0) {
      transactionsContainer.innerHTML = `<div class="empty-state">No transactions yet.</div>`;
      return;
    }

    transactionsContainer.innerHTML = `
      <table>
        <thead>
          <tr>
            <th>Reference</th>
            <th>From</th>
            <th>To</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${data.transactions
            .map(
              (transaction) => `
                <tr>
                  <td>${transaction.reference}</td>
                  <td>${transaction.from_account_id}</td>
                  <td>${transaction.to_account_id}</td>
                  <td>${formatCurrency(transaction.amount)}</td>
                  <td><span class="status success">${transaction.status}</span></td>
                </tr>
              `
            )
            .join("")}
        </tbody>
      </table>
    `;
  } catch (error) {
    console.error("Failed to load transactions:", error);

    if (transactionsContainer) {
      transactionsContainer.innerHTML = `<div class="empty-state">Failed to load transactions: ${error.message}</div>`;
    }
  }
}

async function loadAuditEvents() {
  try {
    const data = await fetchJson(`${API_BASE_URL}/audit-events`);

    setText(totalAuditEvents, data.count);

    if (!auditEventsContainer) return;

    if (data.count === 0) {
      auditEventsContainer.innerHTML = `<div class="empty-state">No audit events yet.</div>`;
      return;
    }

    auditEventsContainer.innerHTML = `
      <table>
        <thead>
          <tr>
            <th>Event</th>
            <th>Outcome</th>
            <th>Actor</th>
            <th>Entity</th>
          </tr>
        </thead>
        <tbody>
          ${data.audit_events
            .map(
              (event) => `
                <tr>
                  <td>${event.event_type}</td>
                  <td>
                    <span class="status ${event.outcome === "success" ? "success" : "failure"}">
                      ${event.outcome}
                    </span>
                  </td>
                  <td>${event.actor || "-"}</td>
                  <td>${event.entity_type || "-"}</td>
                </tr>
              `
            )
            .join("")}
        </tbody>
      </table>
    `;
  } catch (error) {
    console.error("Failed to load audit events:", error);

    if (auditEventsContainer) {
      auditEventsContainer.innerHTML = `<div class="empty-state">Failed to load audit events: ${error.message}</div>`;
    }
  }
}

async function refreshDashboard() {
  await checkApiHealth();

  await Promise.all([
    loadAccounts(),
    loadTransactions(),
    loadAuditEvents(),
  ]);
}

if (transferForm) {
  transferForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (transferResult) {
      transferResult.className = "result-box";
      transferResult.textContent = "";
    }

    const payload = {
      from_account_id: Number(document.getElementById("from-account").value),
      to_account_id: Number(document.getElementById("to-account").value),
      amount: document.getElementById("amount").value,
      actor: "frontend-user",
    };

    try {
      const data = await fetchJson(`${API_BASE_URL}/transfer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (transferResult) {
        transferResult.className = "result-box success";
        transferResult.textContent = `${data.message}. Reference: ${data.transaction.reference}`;
      }

      await refreshDashboard();
    } catch (error) {
      console.error("Transfer failed:", error);

      if (transferResult) {
        transferResult.className = "result-box error";
        transferResult.textContent = error.message;
      }
    }
  });
}

refreshDashboard();
