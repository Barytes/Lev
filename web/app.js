const state = {
  documents: [],
  activePath: "",
  content: "",
  previousAssistContent: "",
  paused: false,
  saveTimer: null,
  assistTimer: null,
  assistAbort: null,
};

const els = {
  documentSelect: document.querySelector("#documentSelect"),
  documentName: document.querySelector("#documentName"),
  editor: document.querySelector("#editor"),
  assistance: document.querySelector("#assistance"),
  saveState: document.querySelector("#saveState"),
  assistState: document.querySelector("#assistState"),
  pauseButton: document.querySelector("#pauseButton"),
};

function setSaveState(text) {
  els.saveState.textContent = text;
}

function setAssistState(text) {
  els.assistState.textContent = text;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.error || `Request failed: ${response.status}`);
  }
  return payload;
}

async function loadDocuments() {
  state.documents = await api("/api/documents");
  els.documentSelect.innerHTML = "";

  for (const doc of state.documents) {
    const option = document.createElement("option");
    option.value = doc.path;
    option.textContent = doc.path;
    els.documentSelect.append(option);
  }

  if (state.documents.length === 0) {
    els.documentName.textContent = "No Markdown/TXT document";
    els.editor.disabled = true;
    els.assistance.value =
      "Lev 没有在当前 workspace 找到 .md 或 .txt 文件。先在项目里创建一个文档，然后刷新页面。";
    return;
  }

  await openDocument(state.documents[0].path);
}

async function openDocument(path) {
  const payload = await api(`/api/document?path=${encodeURIComponent(path)}`);
  state.activePath = payload.path;
  state.content = payload.content;
  state.previousAssistContent = payload.content;
  els.documentSelect.value = path;
  els.documentName.textContent = path;
  els.editor.disabled = false;
  els.editor.value = payload.content;
  els.assistance.value = "Lev 正在观察这个文档。继续写，它会在旁边整理材料。";
  setSaveState("Loaded");
  setAssistState("Waiting");
}

function scheduleSave() {
  clearTimeout(state.saveTimer);
  setSaveState("Editing");
  state.saveTimer = setTimeout(saveDocument, 550);
}

async function saveDocument() {
  if (!state.activePath) return;
  setSaveState("Saving");
  try {
    await api("/api/document", {
      method: "POST",
      body: JSON.stringify({
        path: state.activePath,
        content: els.editor.value,
      }),
    });
    state.content = els.editor.value;
    setSaveState("Saved");
  } catch (error) {
    setSaveState("Save failed");
    els.assistance.value = `保存失败：${error.message}`;
  }
}

function scheduleAssistance() {
  if (state.paused || !state.activePath) return;
  clearTimeout(state.assistTimer);
  setAssistState("Observing");
  state.assistTimer = setTimeout(requestAssistance, 1600);
}

async function requestAssistance() {
  if (state.paused || !state.activePath) return;

  if (state.assistAbort) {
    state.assistAbort.abort();
  }
  state.assistAbort = new AbortController();

  const content = els.editor.value;
  setAssistState("Thinking");
  try {
    const payload = await api("/api/assist", {
      method: "POST",
      signal: state.assistAbort.signal,
      body: JSON.stringify({
        path: state.activePath,
        content,
        previous_content: state.previousAssistContent,
        cursor: els.editor.selectionStart,
        selection_start: els.editor.selectionStart,
        selection_end: els.editor.selectionEnd,
      }),
    });
    state.previousAssistContent = content;
    els.assistance.value = payload.assistance;
    setAssistState(payload.source === "fallback" ? "Local" : "Updated");
  } catch (error) {
    if (error.name === "AbortError") return;
    setAssistState("Error");
    els.assistance.value = `Lev 暂时无法生成协助：${error.message}`;
  }
}

els.editor.addEventListener("input", () => {
  scheduleSave();
  scheduleAssistance();
});

els.editor.addEventListener("keyup", scheduleAssistance);
els.editor.addEventListener("click", scheduleAssistance);

els.documentSelect.addEventListener("change", async (event) => {
  await openDocument(event.target.value);
});

els.pauseButton.addEventListener("click", () => {
  state.paused = !state.paused;
  els.pauseButton.setAttribute("aria-pressed", String(state.paused));
  els.pauseButton.textContent = state.paused ? "Resume" : "Pause";
  setAssistState(state.paused ? "Paused" : "Waiting");
});

loadDocuments().catch((error) => {
  els.assistance.value = `Lev 启动失败：${error.message}`;
  setAssistState("Error");
});

