import {
  appendErrorRows,
  formatTimestamp,
  requestJson,
  setHidden,
  updateDeleteAction,
} from "/common.js";

const elements = {
  responseCard: document.getElementById("responseCard"),
  responseStatus: document.getElementById("responseStatus"),
  responseNotice: document.getElementById("responseNotice"),
  idBlock: document.getElementById("idBlock"),
  responseid: document.getElementById("responseid"),
  searchDetails: document.getElementById("searchDetails"),
  searchTimestamp: document.getElementById("searchTimestamp"),
  searchContents: document.getElementById("searchContents"),
  errorDetails: document.getElementById("errorDetails"),
  responseActions: document.getElementById("responseActions"),
  deletePasteButton: document.getElementById("deletePasteButton"),
};

let activeDeleteId = decodeURIComponent(
  location.pathname.split("/").pop() ?? "",
);

function syncDeleteAction() {
  updateDeleteAction(
    elements.responseActions,
    elements.deletePasteButton,
    activeDeleteId,
  );
}

function resetCard() {
  setHidden(elements.responseCard, false);
  setHidden(elements.responseNotice, true);
  setHidden(elements.idBlock, true);
  setHidden(elements.searchDetails, true);
  setHidden(elements.errorDetails, true);
  elements.responseNotice.textContent = "";
  elements.responseid.textContent = "";
  elements.searchTimestamp.textContent = "";
  elements.searchContents.textContent = "";
  elements.errorDetails.replaceChildren();
}

function showStatus(label, kind) {
  elements.responseStatus.textContent = label;
  elements.responseCard.className = `response-card ${kind}`;
}

function showid(id) {
  setHidden(elements.idBlock, false);
  elements.responseid.textContent = id;
}

function showNotice(message) {
  elements.responseNotice.textContent = message;
  setHidden(elements.responseNotice, false);
}

function showPaste(result) {
  resetCard();
  showStatus("Success", "success");
  showid(result.id);
  elements.searchTimestamp.textContent = formatTimestamp(result.created_at);
  elements.searchContents.textContent = result.contents;
  setHidden(elements.searchDetails, false);
  activeDeleteId = result.id;
  syncDeleteAction();
}

function showDeleteSuccess(result) {
  resetCard();
  showStatus("Success", "success");
  showNotice("Paste deleted successfully.");
  showid(result.id);
  activeDeleteId = "";
  syncDeleteAction();
}

function showError(result) {
  resetCard();
  showStatus("Error", "error");
  appendErrorRows(elements.errorDetails, result ?? { error: "unknown error" });
  setHidden(elements.errorDetails, false);
  activeDeleteId = "";
  syncDeleteAction();
}

async function loadPaste() {
  const { response, result } = await requestJson(
    `/api/paste?id=${encodeURIComponent(activeDeleteId)}`,
  );

  if (response.ok && result.contents && result.created_at) {
    showPaste(result);
    return;
  }

  showError(result);
}

async function handleDeletePaste() {
  if (!activeDeleteId) {
    syncDeleteAction();
    return;
  }

  const idToDelete = activeDeleteId;
  activeDeleteId = "";
  syncDeleteAction();

  const { response, result } = await requestJson(
    `/api/paste?id=${encodeURIComponent(idToDelete)}`,
    { method: "DELETE" },
  );

  if (response.ok && result.id) {
    showDeleteSuccess(result);
    return;
  }

  showError(result);
}

elements.deletePasteButton.addEventListener("click", handleDeletePaste);
loadPaste();
