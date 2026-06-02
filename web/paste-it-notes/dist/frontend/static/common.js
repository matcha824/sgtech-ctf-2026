export function setHidden(element, hidden) {
  element.hidden = hidden;
}

export function requestJson(url, options) {
  return fetch(url, options).then(async (response) => ({
    response,
    result: await response.json(),
  }));
}

export function formatTimestamp(value) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return String(value);
  }

  return new Date(value * 1000).toLocaleString();
}

export function getPastePath(id) {
  return `/paste/${encodeURIComponent(id)}`;
}

export function updateDeleteAction(
  responseActions,
  deleteButton,
  activeDeleteId,
) {
  const hasActiveDeleteTarget = Boolean(activeDeleteId);
  responseActions.classList.toggle("is-hidden", !hasActiveDeleteTarget);
  responseActions.setAttribute(
    "aria-hidden",
    hasActiveDeleteTarget ? "false" : "true",
  );
  deleteButton.disabled = !hasActiveDeleteTarget;
}

export function appendErrorRows(errorDetails, result) {
  const entries = Object.entries(result ?? {});
  const rows = entries.length ? entries : [["status", "No additional details"]];

  for (const [key, value] of rows) {
    const row = document.createElement("div");
    row.className = "response-row";

    const term = document.createElement("dt");
    term.textContent = key;

    const detail = document.createElement("dd");
    detail.textContent =
      typeof value === "string" ? value : JSON.stringify(value);

    row.append(term, detail);
    errorDetails.append(row);
  }
}

export function setPasteLink(linkElement, id, label = "Open paste page") {
  linkElement.href = getPastePath(id);
  linkElement.textContent = label;
}
