const form = document.querySelector("#chat-form");
const promptInput = document.querySelector("#prompt");
const sendButton = document.querySelector("#send");
const newChatButton = document.querySelector("#new-chat");
const messagesEl = document.querySelector("#messages");
const profileButton = document.querySelector("#profile-button");
const profileMenu = document.querySelector("#profile-menu");
const welcomeMessage = "Welcome back. I can help with NotARealBank balances, recent transactions, cards, and account policies. What would you like to review?";
const sessionStorageKey = "notarealbank.sessionId";
const chatTimeoutMs = 35000;
let activeChatController = null;
let activeTypingBubble = null;

function createSessionId() {
  const bytes = new Uint8Array(24);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
}

function getSessionId() {
  let sessionId = sessionStorage.getItem(sessionStorageKey);
  if (!sessionId) {
    sessionId = createSessionId();
    sessionStorage.setItem(sessionStorageKey, sessionId);
  }
  return sessionId;
}

function startNewWindowSession() {
  const sessionId = createSessionId();
  sessionStorage.setItem(sessionStorageKey, sessionId);
  return sessionId;
}

function appendFormattedText(parent, text) {
  const boldPattern = /\*\*([^*]+)\*\*/g;
  let cursor = 0;
  let match = boldPattern.exec(text);

  while (match) {
    if (match.index > cursor) {
      parent.appendChild(document.createTextNode(text.slice(cursor, match.index)));
    }
    const strong = document.createElement("strong");
    strong.textContent = match[1];
    parent.appendChild(strong);
    cursor = match.index + match[0].length;
    match = boldPattern.exec(text);
  }

  if (cursor < text.length) {
    parent.appendChild(document.createTextNode(text.slice(cursor)));
  }
}

function renderAssistantContent(parent, content) {
  const lines = content.split(/\r?\n/);
  let list = null;

  for (const line of lines) {
    const itemMatch = line.match(/^\s*-\s+(.+)$/);
    if (itemMatch) {
      if (!list) {
        list = document.createElement("ul");
        parent.appendChild(list);
      }
      const item = document.createElement("li");
      appendFormattedText(item, itemMatch[1]);
      list.appendChild(item);
      continue;
    }

    list = null;
    if (!line.trim()) {
      parent.appendChild(document.createElement("br"));
      continue;
    }

    const paragraph = document.createElement("p");
    appendFormattedText(paragraph, line);
    parent.appendChild(paragraph);
  }
}

function scrollMessagesToBottom() {
  requestAnimationFrame(() => {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  });
}

function addMessage(role, content, extraClass = "") {
  const message = document.createElement("article");
  message.className = `message ${role} ${extraClass}`.trim();
  const body = document.createElement("div");
  if (role === "assistant") {
    renderAssistantContent(body, content);
  } else {
    body.textContent = content;
  }
  message.appendChild(body);
  messagesEl.appendChild(message);
  scrollMessagesToBottom();
  return message;
}

function addLimitWarning() {
  addMessage("assistant", "Response size limit was reached. The answer may be incomplete.", "limit-warning");
}

function addTypingBubble() {
  const message = document.createElement("article");
  message.className = "message assistant typing";
  message.setAttribute("aria-label", "Buddy Bot is replying");
  message.innerHTML = `
    <span></span>
    <span></span>
    <span></span>
  `;
  messagesEl.appendChild(message);
  scrollMessagesToBottom();
  return message;
}

function resetMessages() {
  messagesEl.textContent = "";
  addMessage("assistant", welcomeMessage);
}

function setComposerEnabled(enabled) {
  promptInput.disabled = !enabled;
  sendButton.disabled = !enabled;
}

function abortActiveChat() {
  if (activeChatController) {
    activeChatController.abort();
    activeChatController = null;
  }
  if (activeTypingBubble) {
    activeTypingBubble.remove();
    activeTypingBubble = null;
  }
  setComposerEnabled(true);
}

async function sendMessage(content, signal) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: content, session_id: getSessionId() }),
    signal,
  });
  const data = await response.json();
  if (data.session_id) {
    sessionStorage.setItem(sessionStorageKey, data.session_id);
  }
  if (!response.ok || data.error) {
    throw new Error(data.error || `Request failed with HTTP ${response.status}`);
  }
  return data;
}

async function resetSession() {
  const response = await fetch("/api/session/reset", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: startNewWindowSession() }),
  });
  const data = await response.json();
  if (data.session_id) {
    sessionStorage.setItem(sessionStorageKey, data.session_id);
  }
  if (!response.ok || data.error) {
    throw new Error(data.error || `Request failed with HTTP ${response.status}`);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (activeChatController) {
    return;
  }

  const content = promptInput.value.trim();
  if (!content) {
    return;
  }

  promptInput.value = "";
  setComposerEnabled(false);
  addMessage("user", content);
  const typingBubble = addTypingBubble();
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), chatTimeoutMs);
  activeTypingBubble = typingBubble;
  activeChatController = controller;

  try {
    const reply = await sendMessage(content, controller.signal);
    typingBubble.remove();
    if (activeTypingBubble === typingBubble) {
      activeTypingBubble = null;
    }
    addMessage("assistant", reply.reply);
    if (reply.finish_reason === "length") {
      addLimitWarning();
    }
  } catch (error) {
    typingBubble.remove();
    if (activeTypingBubble === typingBubble) {
      activeTypingBubble = null;
    }
    if (error.name !== "AbortError") {
      addMessage("assistant", error.message, "error");
    } else if (activeChatController === controller) {
      addMessage("assistant", "Chat request timed out. Please try again.", "error");
    }
  } finally {
    window.clearTimeout(timeoutId);
    if (activeChatController === controller) {
      activeChatController = null;
      setComposerEnabled(true);
      promptInput.focus();
    }
  }
});

promptInput.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" || event.shiftKey || event.isComposing) {
    return;
  }

  event.preventDefault();
  if (!sendButton.disabled) {
    form.requestSubmit();
  }
});

newChatButton.addEventListener("click", async () => {
  newChatButton.disabled = true;
  abortActiveChat();
  setComposerEnabled(false);

  try {
    await resetSession();
    resetMessages();
  } catch (error) {
    addMessage("assistant", error.message, "error");
  } finally {
    newChatButton.disabled = false;
    setComposerEnabled(true);
    promptInput.focus();
  }
});

profileButton.addEventListener("click", (event) => {
  event.stopPropagation();
  const shouldOpen = profileMenu.hidden;
  profileMenu.hidden = !shouldOpen;
  profileButton.setAttribute("aria-expanded", String(shouldOpen));
});

document.addEventListener("click", (event) => {
  if (profileMenu.hidden || event.target.closest(".profile")) {
    return;
  }
  profileMenu.hidden = true;
  profileButton.setAttribute("aria-expanded", "false");
});

profileMenu.addEventListener("click", (event) => {
  event.preventDefault();
  profileMenu.hidden = true;
  profileButton.setAttribute("aria-expanded", "false");
});
