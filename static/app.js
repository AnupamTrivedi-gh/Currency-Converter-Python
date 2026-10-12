const $ = (id) => document.getElementById(id);
const form = $("convertForm");
const amountInput = $("amount");
const sourceSelect = $("source");
const targetSelect = $("target");
const message = $("message");
const resultPanel = $("resultPanel");

function showMessage(text, isError = false) {
  message.textContent = text;
  message.className = isError ? "message error" : "message";
}

function formatMoney(value, code) {
  try {
    return new Intl.NumberFormat(undefined, {style: "currency", currency: code, maximumFractionDigits: 4}).format(value);
  } catch {
    return `${Number(value).toFixed(2)} ${code}`;
  }
}

async function loadCurrencies() {
  const response = await fetch("/api/currencies");
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Could not load currencies.");
  const previousSource = sourceSelect.value || "USD";
  const previousTarget = targetSelect.value || "INR";
  sourceSelect.replaceChildren();
  targetSelect.replaceChildren();
  data.currencies.forEach(({code, name}) => {
    const label = `${code} — ${name}`;
    sourceSelect.add(new Option(label, code));
    targetSelect.add(new Option(label, code));
  });
  sourceSelect.value = [...sourceSelect.options].some(o => o.value === previousSource) ? previousSource : "USD";
  targetSelect.value = [...targetSelect.options].some(o => o.value === previousTarget) ? previousTarget : "INR";
  const status = $("rateStatus");
  status.className = data.is_live ? "status live" : "status";
  status.lastChild.textContent = data.is_live ? " Live rates available" : " Offline fallback rates";
}

async function loadHistory() {
  const list = $("historyList");
  try {
    const response = await fetch("/api/history");
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "History unavailable.");
    list.replaceChildren();
    if (!data.history.length) {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = "No conversions yet. Your first conversion will appear here.";
      list.append(empty);
      return;
    }
    data.history.forEach(line => {
      const item = document.createElement("div");
      item.className = "history-item";
      const left = document.createElement("div");
      const pair = document.createElement("div");
      pair.className = "history-pair";
      pair.textContent = line.split("|").slice(1, 2)[0]?.trim() || line;
      const date = document.createElement("div");
      date.className = "history-date";
      date.textContent = line.split("|")[0].replace(/^\[|\]$/g, "").trim();
      left.append(pair, date);
      const mode = document.createElement("div");
      mode.className = "history-mode";
      mode.textContent = line.includes("Offline fallback") ? "Offline fallback" : "Live API";
      item.append(left, mode);
      list.append(item);
    });
  } catch (error) {
    list.textContent = error.message;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = $("convertBtn");
  button.disabled = true;
  resultPanel.hidden = true;
  showMessage("Converting…");
  try {
    const response = await fetch("/api/convert", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({amount: amountInput.value, source: sourceSelect.value, target: targetSelect.value})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Conversion failed.");
    $("resultValue").textContent = `${formatMoney(data.result, data.target)}`;
    $("resultMeta").textContent = `${formatMoney(data.amount, data.source)} → ${data.target} · ${data.mode}`;
    resultPanel.hidden = false;
    showMessage(data.history_saved ? "Conversion complete. Saved to history." : "Conversion complete, but history could not be saved.");
    await loadHistory();
  } catch (error) {
    showMessage(error.message, true);
  } finally {
    button.disabled = false;
  }
});

$("swapBtn").addEventListener("click", () => {
  const oldSource = sourceSelect.value;
  sourceSelect.value = targetSelect.value;
  targetSelect.value = oldSource;
});
$("refreshHistory").addEventListener("click", loadHistory);

(async function init() {
  try {
    await loadCurrencies();
  } catch (error) {
    showMessage(`Could not load currency list: ${error.message}`, true);
  }
  await loadHistory();
})();
