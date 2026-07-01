// app.js
// Handles the chat form and keeps the storage inspector panel in sync.
// No frameworks — the surface area here is small enough that plain DOM
// APIs keep the file easy to read alongside app.py / storage.py.

const chatScroll = document.getElementById("chat-scroll");
const chatForm = document.getElementById("chat-form");
const chatText = document.getElementById("chat-text");
const username = document.querySelector(".app").dataset.username;

document.getElementById("session-id-display").textContent = `session_default_user_${username}`;

function addBubble(role, content) {
  const bubble = document.createElement("div");
  bubble.className = `bubble bubble--${role === "human" ? "human" : "ai"}`;

  const meta = document.createElement("div");
  meta.className = "bubble-meta";
  meta.textContent = role === "human" ? "you" : "gemini";

  const body = document.createElement("div");
  body.textContent = content;

  bubble.appendChild(meta);
  bubble.appendChild(body);
  chatScroll.appendChild(bubble);
  chatScroll.scrollTop = chatScroll.scrollHeight;
}

async function loadHistory() {
  const res = await fetch("/api/history");
  const messages = await res.json();
  messages.forEach((m) => addBubble(m.role, m.content));
}

function renderStorage(stats) {
  document.getElementById("db-file-name").textContent = stats.db_file;
  document.getElementById("db-size").textContent = `${stats.size_human} on disk`;

  const tableList = document.getElementById("table-list");
  tableList.innerHTML = "";
  stats.tables.forEach((t) => {
    const row = document.createElement("div");
    row.className = "table-row";
    row.innerHTML = `<span class="table-row-name">${t.name}</span><span class="table-row-count">${t.rows}</span>`;
    tableList.appendChild(row);
  });

  document.getElementById("session-count").textContent = `${stats.session_messages} messages stored`;

  const ledger = document.getElementById("ledger");
  ledger.innerHTML = "";
  stats.ledger.forEach((entry) => {
    const row = document.createElement("div");
    row.className = "ledger-row";
    row.innerHTML = `
      <span class="ts">${entry.ts}</span>
      <span class="event event--${entry.event}">${entry.event}</span>
      <span class="who">${entry.username || ""}</span>
      <span class="detail">${entry.detail || ""}</span>
    `;
    ledger.appendChild(row);
  });
}

async function loadStorage() {
  const res = await fetch("/api/storage");
  renderStorage(await res.json());
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatText.value.trim();
  if (!message) return;

  addBubble("human", message);
  chatText.value = "";
  chatText.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    if (data.error) {
      addBubble("ai", `Error: ${data.error}`);
    } else {
      addBubble("ai", data.reply);
      renderStorage(data.storage);
    }
  } catch (err) {
    addBubble("ai", "Connection error — message may not have been saved.");
  } finally {
    chatText.disabled = false;
    chatText.focus();
  }
});

loadHistory();
loadStorage();
setInterval(loadStorage, 8000); // keep the ledger fresh even if this tab is idle