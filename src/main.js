const { invoke } = window.__TAURI__.core;
const { listen } = window.__TAURI__.event;

let currentSettings = {};

// UI Elements
const statusText = document.getElementById("status-text");
const statusContainer = document.getElementById("app");
const micSelect = document.getElementById("mic-select");
const engineGroq = document.getElementById("engine-groq");
const engineLocal = document.getElementById("engine-local");
const apiKeyInput = document.getElementById("api-key");
const langSelect = document.getElementById("language");
const modelSelect = document.getElementById("model-select");
const hotkeyDisplay = document.getElementById("hotkey-display");
const saveBtn = document.getElementById("save-btn");
const localModelSection = document.getElementById("local-model-section");
const downloadBtn = document.getElementById("download-model-btn");
const downloadProgress = document.getElementById("download-progress");
const transcriptionText = document.getElementById("transcription-text");
const clearTextBtn = document.getElementById("clear-text-btn");

async function init() {
    // Load Settings
    currentSettings = await invoke("get_settings");
    updateUIFromSettings();

    // Load Mics
    const mics = await invoke("get_microphones");
    mics.forEach(mic => {
        const option = document.createElement("option");
        option.value = mic;
        option.textContent = mic;
        micSelect.appendChild(option);
    });
    micSelect.value = currentSettings.microphone_id;

    // Listen for Status Updates
    listen("status", (event) => {
        updateStatus(event.payload);
    });

    listen("error", (event) => {
        alert("Error: " + event.payload);
        updateStatus("idle");
    });

    listen("transcription", (event) => {
        transcriptionText.value = event.payload;
        transcriptionText.scrollTop = 0;
    });
}

clearTextBtn.onclick = () => {
    transcriptionText.value = "";
};

function updateUIFromSettings() {
    apiKeyInput.value = currentSettings.groq_api_key;
    langSelect.value = currentSettings.language;
    modelSelect.value = currentSettings.local_model;
    hotkeyDisplay.textContent = currentSettings.hotkey;
    
    if (currentSettings.engine === "groq") {
        engineGroq.classList.add("active");
        engineLocal.classList.remove("active");
        localModelSection.classList.add("hidden");
    } else {
        engineGroq.classList.remove("active");
        engineLocal.classList.add("active");
        localModelSection.classList.remove("hidden");
    }
}

function updateStatus(status) {
    statusText.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    statusContainer.classList.remove("recording", "transcribing");
    
    if (status === "recording") {
        statusContainer.classList.add("recording");
    } else if (status === "transcribing") {
        statusContainer.classList.add("transcribing");
    }
}

engineGroq.onclick = () => {
    currentSettings.engine = "groq";
    updateUIFromSettings();
};

engineLocal.onclick = () => {
    currentSettings.engine = "local";
    updateUIFromSettings();
};

saveBtn.onclick = async () => {
    currentSettings.groq_api_key = apiKeyInput.value;
    currentSettings.language = langSelect.value;
    currentSettings.local_model = modelSelect.value;
    currentSettings.microphone_id = micSelect.value;

    try {
        await invoke("save_settings", { settings: currentSettings });
        saveBtn.textContent = "Saved!";
        setTimeout(() => saveBtn.textContent = "Save Settings", 2000);
    } catch (e) {
        alert("Failed to save: " + e);
    }
};

downloadBtn.onclick = async () => {
    downloadBtn.disabled = true;
    downloadProgress.classList.remove("hidden");
    try {
        await invoke("download_local_model");
        alert("Model downloaded successfully!");
    } catch (e) {
        alert("Download failed: " + e);
    } finally {
        downloadBtn.disabled = false;
        downloadProgress.classList.add("hidden");
    }
};

init();
