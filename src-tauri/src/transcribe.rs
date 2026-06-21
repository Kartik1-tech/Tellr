use reqwest::Client;
use reqwest::multipart::{Form, Part};
use std::fs;
use std::io::Write;

pub async fn transcribe_groq(wav_bytes: Vec<u8>, api_key: &str, lang: &str) -> Result<String, String> {
    let client = Client::new();
    let mut form = Form::new()
        .part("file", Part::bytes(wav_bytes).file_name("audio.wav").mime_str("audio/wav").unwrap())
        .text("model", "whisper-large-v3");
    
    // Only send language parameter if a specific language is selected (not auto-detect)
    if !lang.is_empty() {
        form = form.text("language", lang.to_string());
    }

    let response = client.post("https://api.groq.com/openai/v1/audio/transcriptions")
        .bearer_auth(api_key)
        .multipart(form)
        .send()
        .await
        .map_err(|e| e.to_string())?;

    if response.status().is_success() {
        let json: serde_json::Value = response.json().await.map_err(|e| e.to_string())?;
        Ok(json["text"].as_str().unwrap_or("").to_string())
    } else {
        let status = response.status();
        let err_text = response.text().await.unwrap_or_default();
        Err(format!("Groq API error: {} - {}", status, err_text))
    }
}

pub fn transcribe_local(_wav_bytes: Vec<u8>, _model_path: &str) -> Result<String, String> {
    Err("Local transcription is currently disabled. Install LLVM and re-enable in Cargo.toml to use this feature.".to_string())
}

pub async fn download_model(url: &str, path: &str) -> Result<(), String> {
    let client = Client::new();
    let response = client.get(url).send().await.map_err(|e| e.to_string())?;
    let bytes = response.bytes().await.map_err(|e| e.to_string())?;
    
    let mut file = fs::File::create(path).map_err(|e| e.to_string())?;
    file.write_all(&bytes).map_err(|e| e.to_string())?;
    Ok(())
}
