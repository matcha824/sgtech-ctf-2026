import {
  appendErrorRows,
  formatTimestamp,
  requestJson,
  setHidden,
  setPasteLink,
  updateDeleteAction,
} from "./common.js";

const elements = {
  contents: document.getElementById("contents"),
  pasteForm: document.getElementById("pasteForm"),
  response: document.getElementById("response"),
  responseCard: document.getElementById("responseCard"),
  responseStatus: document.getElementById("responseStatus"),
  responseNotice: document.getElementById("responseNotice"),
  idBlock: document.getElementById("idBlock"),
  responseid: document.getElementById("responseid"),
  pasteLinkBlock: document.getElementById("pasteLinkBlock"),
  pastePageLink: document.getElementById("pastePageLink"),
  searchForm: document.getElementById("searchForm"),
  searchid: document.getElementById("searchid"),
  searchDetails: document.getElementById("searchDetails"),
  searchTimestamp: document.getElementById("searchTimestamp"),
  searchContents: document.getElementById("searchContents"),
  errorDetails: document.getElementById("errorDetails"),
  responseActions: document.getElementById("responseActions"),
  deletePasteButton: document.getElementById("deletePasteButton"),
};

let activeDeleteId = "";

function syncDeleteAction() {
  updateDeleteAction(
    elements.responseActions,
    elements.deletePasteButton,
    activeDeleteId,
  );
}

function resetResponse() {
  setHidden(elements.response, false);
  setHidden(elements.responseCard, false);
  setHidden(elements.responseNotice, true);
  setHidden(elements.idBlock, true);
  setHidden(elements.pasteLinkBlock, true);
  setHidden(elements.searchDetails, true);
  setHidden(elements.errorDetails, true);

  elements.responseNotice.textContent = "";
  elements.responseid.textContent = "";
  elements.pastePageLink.href = "#";
  elements.pastePageLink.textContent = "";
  elements.searchTimestamp.textContent = "";
  elements.searchContents.textContent = "";
  elements.errorDetails.replaceChildren();
  activeDeleteId = "";
  syncDeleteAction();
}

function showResponseCard(statusLabel, statusClass) {
  elements.responseStatus.textContent = statusLabel;
  elements.responseCard.className = `response-card ${statusClass}`;
}

function showid(id) {
  setHidden(elements.idBlock, false);
  elements.responseid.textContent = id;
}

function showPasteLink(id) {
  setHidden(elements.pasteLinkBlock, false);
  setPasteLink(elements.pastePageLink, id);
}

function showNotice(message) {
  elements.responseNotice.textContent = message;
  setHidden(elements.responseNotice, false);
}

function showCreateSuccess(result) {
  resetResponse();
  showResponseCard("Success", "success");
  showid(result.id);
  showPasteLink(result.id);
  activeDeleteId = result.id;
  syncDeleteAction();
}

function showSearchSuccess(result) {
  resetResponse();
  showResponseCard("Success", "success");
  showid(result.id);
  showPasteLink(result.id);

  elements.searchTimestamp.textContent = formatTimestamp(result.created_at);
  elements.searchContents.textContent = result.contents;
  activeDeleteId = result.id;

  setHidden(elements.searchDetails, false);
  syncDeleteAction();
}

function showDeleteSuccess(result) {
  resetResponse();
  showResponseCard("Success", "success");
  showNotice("Paste deleted successfully.");
  showid(result.id);
  showPasteLink(result.id);
}

function showError(result) {
  resetResponse();
  showResponseCard("Error", "error");

  appendErrorRows(elements.errorDetails, result);

  setHidden(elements.errorDetails, false);
}

function renderResponse(response, result, mode) {
  if (mode === "create" && response.ok && result.id) {
    showCreateSuccess(result);
    return;
  }

  if (mode === "search" && result.contents && result.created_at) {
    showSearchSuccess(result);
    return;
  }

  if (mode === "delete" && response.ok && result.id) {
    showDeleteSuccess(result);
    return;
  }

  showError(result);
}

async function handleCreatePaste(event) {
  event.preventDefault();

  const contents = elements.contents.innerText.trim();
  const { response, result } = await requestJson("/api/paste", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ contents }),
  });

  renderResponse(response, result, "create");
}

async function handleSearchPaste(event) {
  event.preventDefault();

  const id = elements.searchid.value.trim();
  const { response, result } = await requestJson(
    `/api/paste?id=${encodeURIComponent(id)}`,
  );

  renderResponse(response, result, "search");
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

  renderResponse(response, result, "delete");
}

elements.pasteForm.addEventListener("submit", handleCreatePaste);
elements.searchForm.addEventListener("submit", handleSearchPaste);
elements.deletePasteButton.addEventListener("click", handleDeletePaste);
