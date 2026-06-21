use enigo::{Enigo, Key, KeyboardControllable};
use std::thread;
use std::time::Duration;

pub fn auto_paste() {
    let mut enigo = Enigo::new();
    
    // Small delay to ensure clipboard is updated and system is ready
    thread::sleep(Duration::from_millis(150));

    #[cfg(target_os = "macos")]
    {
        enigo.key_down(Key::Command);
        enigo.key_click(Key::V);
        enigo.key_up(Key::Command);
    }

    #[cfg(not(target_os = "macos"))]
    {
        enigo.key_down(Key::Control);
        enigo.key_click(Key::V);
        enigo.key_up(Key::Control);
    }
}
