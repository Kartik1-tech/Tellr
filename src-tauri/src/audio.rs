use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use std::sync::{Arc, Mutex};
use hound::{WavSpec, WavWriter};
use std::io::Cursor;

pub struct AudioRecorder {
    pub buffer: Arc<Mutex<Vec<f32>>>,
    stream: Option<cpal::Stream>,
    input_sample_rate: u32,
}

impl AudioRecorder {
    pub fn new() -> Self {
        Self {
            buffer: Arc::new(Mutex::new(Vec::new())),
            stream: None,
            input_sample_rate: 44100,
        }
    }

    pub fn list_microphones() -> Vec<String> {
        let host = cpal::default_host();
        let mut mics = Vec::new();
        if let Ok(devices) = host.input_devices() {
            for device in devices {
                if let Ok(name) = device.name() {
                    mics.push(name);
                }
            }
        }
        mics
    }

    pub fn start_recording(&mut self, device_name: &str) -> Result<(), String> {
        let host = cpal::default_host();
        let device = if device_name == "default" {
            host.default_input_device()
        } else {
            host.input_devices()
                .map_err(|e| e.to_string())?
                .find(|d| d.name().unwrap_or_default() == device_name)
        }.ok_or("Device not found")?;

        let config = device.default_input_config().map_err(|e| e.to_string())?;
        self.input_sample_rate = config.sample_rate().0;
        let channels = config.channels();
        
        let buffer = self.buffer.clone();
        buffer.lock().unwrap().clear();

        let stream = device.build_input_stream(
            &config.into(),
            move |data: &[f32], _: &_| {
                let mut b = buffer.lock().unwrap();
                // Simple mono mixdown if needed
                if channels > 1 {
                    for chunk in data.chunks(channels as usize) {
                        let mono = chunk.iter().sum::<f32>() / channels as f32;
                        b.push(mono);
                    }
                } else {
                    b.extend_from_slice(data);
                }
            },
            |err| eprintln!("Stream error: {}", err),
            None
        ).map_err(|e| e.to_string())?;

        stream.play().map_err(|e| e.to_string())?;
        self.stream = Some(stream);
        Ok(())
    }

    pub fn stop_recording(&mut self) -> Result<Vec<u8>, String> {
        self.stream.take(); 
        let data = self.buffer.lock().unwrap().clone();
        
        // Resample to 16kHz for Whisper compatibility
        let target_rate = 16000;
        let resampled = if self.input_sample_rate != target_rate {
            linear_resample(&data, self.input_sample_rate, target_rate)
        } else {
            data
        };

        let spec = WavSpec {
            channels: 1,
            sample_rate: target_rate,
            bits_per_sample: 16,
            sample_format: hound::SampleFormat::Int,
        };

        let mut wav_data = Vec::new();
        {
            let mut writer = WavWriter::new(Cursor::new(&mut wav_data), spec).map_err(|e| e.to_string())?;
            for &sample in &resampled {
                let s = (sample * i16::MAX as f32) as i16;
                writer.write_sample(s).map_err(|e| e.to_string())?;
            }
            writer.finalize().map_err(|e| e.to_string())?;
        }
        
        Ok(wav_data)
    }
}

/// Linear interpolation resampler: converts audio from input_rate Hz to output_rate Hz
fn linear_resample(input: &[f32], input_rate: u32, output_rate: u32) -> Vec<f32> {
    if input_rate == output_rate || input.is_empty() {
        return input.to_vec();
    }

    let ratio = output_rate as f64 / input_rate as f64;
    let output_len = (input.len() as f64 * ratio).ceil() as usize;
    let mut output = Vec::with_capacity(output_len);
    let last_idx = input.len() - 1;

    for i in 0..output_len {
        let input_pos = i as f64 / ratio;
        let idx_floor = input_pos.floor() as usize;
        let idx_ceil = (idx_floor + 1).min(last_idx);
        let frac = input_pos - idx_floor as f64;

        let sample = input[idx_floor] as f64 * (1.0 - frac) + input[idx_ceil] as f64 * frac;
        output.push(sample as f32);
    }

    output
}
