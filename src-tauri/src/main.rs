// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod settings;
mod audio;
mod transcribe;
mod paste;

use std::sync::Mutex;
use std::sync::mpsc::{channel, Sender};
use tauri::{AppHandle, Manager, State, Emitter, image::Image};
use tauri::tray::{TrayIconBuilder, TrayIconEvent, MouseButton, MouseButtonState};
use tauri_plugin_global_shortcut::{GlobalShortcutExt, Shortcut, ShortcutState};
use tauri_plugin_clipboard_manager::ClipboardExt;

enum AudioCommand {
    Start(String),
    Stop(oneshot::Sender<Result<Vec<u8>, String>>),
}

struct AppState {
    audio_tx: Sender<AudioCommand>,
    settings: Mutex<settings::Settings>,
    is_recording: Mutex<bool>,
}

#[tauri::command]
fn get_microphones() -> Vec<String> {
    audio::AudioRecorder::list_microphones()
}

#[tauri::command]
async fn start_recording(state: State<'_, AppState>) -> Result<(), String> {
    let settings = state.inner().settings.lock().unwrap();
    state.inner().audio_tx.send(AudioCommand::Start(settings.microphone_id.clone()))
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn stop_and_transcribe(app: AppHandle, state: State<'_, AppState>) -> Result<String, String> {
    let (tx, rx) = oneshot::channel();
    state.inner().audio_tx.send(AudioCommand::Stop(tx)).map_err(|e| e.to_string())?;
    
    let wav_bytes = rx.await.map_err(|e| e.to_string())??;
    
    let settings = state.inner().settings.lock().unwrap().clone();
    
    let text = if settings.engine == "groq" {
        transcribe::transcribe_groq(wav_bytes, &settings.groq_api_key, &settings.language).await?
    } else {
        let proj_dirs = directories::ProjectDirs::from("com", "speakr", "app").unwrap();
        let model_path = proj_dirs.config_dir().join(format!("ggml-{}.bin", settings.local_model));
        transcribe::transcribe_local(wav_bytes, model_path.to_str().ok_or("Invalid model path")?)?
    };

    if !text.is_empty() {
        app.clipboard().write_text(text.clone()).map_err(|e| e.to_string())?;
        paste::auto_paste();
    }

    Ok(text)
}

#[tauri::command]
fn get_settings(state: State<'_, AppState>) -> settings::Settings {
    state.inner().settings.lock().unwrap().clone()
}

#[tauri::command]
fn save_settings(app: AppHandle, state: State<'_, AppState>, settings: settings::Settings) -> Result<(), String> {
    let mut old_settings = state.inner().settings.lock().unwrap();
    let old_hotkey = old_settings.hotkey.clone();
    
    *old_settings = settings.clone();
    settings::save_settings(&settings);

    if old_hotkey != settings.hotkey {
        let _ = app.global_shortcut().unregister_all();
        if let Ok(shortcut) = settings.hotkey.parse::<Shortcut>() {
            app.global_shortcut().register(shortcut).map_err(|e| e.to_string())?;
        }
    }
    
    Ok(())
}

#[tauri::command]
async fn download_local_model(state: State<'_, AppState>) -> Result<(), String> {
    let model = {
        let settings = state.inner().settings.lock().unwrap();
        settings.local_model.clone()
    };
    let url = format!("https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{}.bin", model);
    
    let proj_dirs = directories::ProjectDirs::from("com", "speakr", "app").unwrap();
    let path = proj_dirs.config_dir().join(format!("ggml-{}.bin", model));
    
    transcribe::download_model(&url, path.to_str().unwrap()).await
}

fn main() {
    let (audio_tx, audio_rx) = channel::<AudioCommand>();
    
    // Spawn dedicated audio thread to handle non-Send Stream on Windows
    std::thread::spawn(move || {
        let mut recorder = audio::AudioRecorder::new();
        while let Ok(cmd) = audio_rx.recv() {
            match cmd {
                AudioCommand::Start(device) => {
                    let _ = recorder.start_recording(&device);
                }
                AudioCommand::Stop(tx) => {
                    let res = recorder.stop_recording();
                    let _ = tx.send(res);
                }
            }
        }
    });

    let initial_settings = settings::load_settings();
    
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_global_shortcut::Builder::new().with_handler(|app: &AppHandle, _shortcut: &Shortcut, event: tauri_plugin_global_shortcut::ShortcutEvent| {
            if event.state() == ShortcutState::Pressed {
                let state = app.state::<AppState>();
                let mut is_recording = state.is_recording.lock().unwrap();
                
                if *is_recording {
                    *is_recording = false;
                    let _ = app.emit("status", "transcribing");
                    let app_handle = app.clone();
                    tauri::async_runtime::spawn(async move {
                        match stop_and_transcribe(app_handle.clone(), app_handle.state()).await {
                            Ok(text) => {
                                let _ = app_handle.emit("transcription", text);
                                let _ = app_handle.emit("status", "idle");
                            },
                            Err(e) => { let _ = app_handle.emit("error", e); },
                        }
                    });
                } else {
                    *is_recording = true;
                    let _ = app.emit("status", "recording");
                    let state_clone = app.state::<AppState>();
                    let app_handle = app.clone();
                    tauri::async_runtime::spawn(async move {
                        if let Err(e) = start_recording(state_clone).await {
                            let _ = app_handle.emit("error", e);
                        }
                    });
                }
            }
        }).build())
        .plugin(tauri_plugin_clipboard_manager::init())
        .plugin(tauri_plugin_dialog::init())
        .manage(AppState {
            audio_tx,
            settings: Mutex::new(initial_settings.clone()),
            is_recording: Mutex::new(false),
        })
        .invoke_handler(tauri::generate_handler![
            get_microphones,
            start_recording,
            stop_and_transcribe,
            get_settings,
            save_settings,
            download_local_model
        ])
        .setup(|app| {
            let hotkey_str = initial_settings.hotkey.clone();
            if let Ok(shortcut) = hotkey_str.parse::<Shortcut>() {
                let _ = app.global_shortcut().register(shortcut);
            }

            // System tray icon with left-click toggle window
            let img = image::load_from_memory(include_bytes!("../icons/icon.png"))
                .expect("Failed to load tray icon")
                .to_rgba8();
            let (width, height) = img.dimensions();
            let icon = tauri::image::Image::new_owned(img.into_raw(), width, height);
            let app_handle = app.handle().clone();
            TrayIconBuilder::new()
                .icon(icon)
                .tooltip("Speakr")
                .on_tray_icon_event(move |_tray, event| {
                    if let TrayIconEvent::Click { button: MouseButton::Left, button_state: MouseButtonState::Up, .. } = event {
                        if let Some(window) = app_handle.get_webview_window("main") {
                            if window.is_visible().unwrap_or(false) {
                                let _ = window.hide();
                            } else {
                                let _ = window.show();
                                let _ = window.set_focus();
                            }
                        }
                    }
                })
                .build(app)?;

            // Minimize to tray on window close
            if let Some(window) = app.get_webview_window("main") {
                let handle = app.handle().clone();
                window.on_window_event(move |event| {
                    if let tauri::WindowEvent::CloseRequested { api, .. } = event {
                        api.prevent_close();
                        if let Some(win) = handle.get_webview_window("main") {
                            let _ = win.hide();
                        }
                    }
                });
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
