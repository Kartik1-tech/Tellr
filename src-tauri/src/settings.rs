use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;
use directories::ProjectDirs;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Settings {
    pub engine: String,
    pub groq_api_key: String,
    pub hotkey: String,
    pub microphone_id: String,
    pub language: String,
    pub local_model: String,
}

impl Default for Settings {
    fn default() -> Self {
        dotenvy::dotenv().ok();
        Self {
            engine: std::env::var("DEFAULT_ENGINE").unwrap_or_else(|_| "groq".to_string()),
            groq_api_key: std::env::var("GROQ_API_KEY").unwrap_or_else(|_| "".to_string()),
            hotkey: std::env::var("DEFAULT_HOTKEY").unwrap_or_else(|_| "Ctrl+Shift+M".to_string()),
            microphone_id: "default".to_string(),
            language: "en".to_string(),
            local_model: "base".to_string(),
        }
    }
}

pub fn get_settings_path() -> PathBuf {
    let proj_dirs = ProjectDirs::from("com", "tellr", "app").unwrap();
    let config_dir = proj_dirs.config_dir();
    fs::create_dir_all(config_dir).unwrap();
    config_dir.join("settings.json")
}

pub fn load_settings() -> Settings {
    let path = get_settings_path();
    if path.exists() {
        let content = fs::read_to_string(path).unwrap_or_default();
        serde_json::from_str(&content).unwrap_or_default()
    } else {
        Settings::default()
    }
}

pub fn save_settings(settings: &Settings) {
    let path = get_settings_path();
    let content = serde_json::to_string_pretty(settings).unwrap();
    fs::write(path, content).unwrap();
}
