#!/usr/bin/env python3
import os
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess

SR = 44100
DURATION = 47.60

def synth_cinematic_bgm():
    print("Synthesizing cinematic documentary BGM score...")
    t = np.linspace(0, DURATION, int(SR * DURATION), False)
    
    # 1. Warm Analog Sub & Mid Drone Bed (D Minor: D1=36.71Hz, D2=73.42Hz, A2=110Hz, F3=174.61Hz)
    lfo1 = 1.0 + 0.12 * np.sin(2 * np.pi * 0.08 * t)
    lfo2 = 1.0 + 0.08 * np.sin(2 * np.pi * 0.15 * t + 1.2)
    
    drone = (
        0.45 * np.sin(2 * np.pi * 36.71 * t) +
        0.35 * np.sin(2 * np.pi * 73.42 * t) * lfo1 +
        0.25 * np.sin(2 * np.pi * 110.00 * t + 0.4) +
        0.18 * np.sin(2 * np.pi * 174.61 * t + 0.8) * lfo2
    )
    
    # 2. Cinematic Heartbeat / Rhythmic Pulse (120 BPM = 0.5s period)
    # Starts entering around 10s and builds
    pulse_env = np.clip((t - 10.0) / 10.0, 0, 1.0)
    pulse_t = t % 0.5
    kick = np.sin(2 * np.pi * np.geomspace(85, 38, len(pulse_t)) * pulse_t) * np.exp(-pulse_t * 12)
    kick_track = np.tile(kick[:int(SR * 0.5)], int(DURATION / 0.5) + 1)[:len(t)]
    
    # 3. Ethereal Glass / Ambient Piano Arpeggios (Dm9 chord tones: D4=293.66, F4=349.23, A4=440.0, C5=523.25, E5=659.25)
    arp_notes = [293.66, 440.0, 523.25, 659.25, 440.0, 349.23]
    note_dur = 0.5  # 1/8th note at 120bpm
    arp_track = np.zeros_like(t)
    
    for i, start_time in enumerate(np.arange(0, DURATION, note_dur)):
        if start_time < DURATION:
            note_idx = (i % len(arp_notes))
            freq = arp_notes[note_idx]
            n_samples = int(SR * 1.5)  # 1.5s decay with overlap
            t_note = np.linspace(0, 1.5, n_samples, False)
            # Harmonic modal tone
            note_sig = (
                0.6 * np.sin(2 * np.pi * freq * t_note) +
                0.25 * np.sin(2 * np.pi * freq * 2 * t_note) +
                0.15 * np.sin(2 * np.pi * freq * 3 * t_note)
            ) * np.exp(-t_note * 2.8)
            
            idx_start = int(start_time * SR)
            idx_end = min(len(t), idx_start + n_samples)
            arp_track[idx_start:idx_end] += note_sig[:idx_end - idx_start] * 0.35
            
    # 4. Cinematic Crescendo Swell (38s to 45s)
    swell_env = np.clip((t - 36.0) / 8.0, 0, 1.0)
    swell = (
        0.3 * np.sin(2 * np.pi * 220.0 * t) +
        0.2 * np.sin(2 * np.pi * 329.63 * t) +
        0.2 * np.sin(2 * np.pi * 440.0 * t)
    ) * swell_env
    
    # Mix layers
    bgm = drone + (kick_track * pulse_env * 0.4) + (arp_track * 0.45) + (swell * 0.5)
    
    # Soft limiter & saturation
    bgm = np.tanh(bgm * 1.2)
    
    # Global Fade In (2s) and Fade Out (3s)
    fade_in = np.linspace(0, 1, int(SR * 2.0))
    fade_out = np.linspace(1, 0, int(SR * 3.0))
    bgm[:len(fade_in)] *= fade_in
    bgm[-len(fade_out):] *= fade_out
    
    # Normalize to -1dB peak
    bgm = bgm / (np.max(np.abs(bgm)) + 1e-7) * 0.9
    
    bgm_path = os.path.join(os.path.dirname(__file__), ".temp_audio", "cinematic_bgm.wav")
    wav_data = (bgm * 32767).astype(np.int16)
    wavfile.write(bgm_path, SR, wav_data)
    print(f"BGM rendered: {bgm_path}")
    return bgm_path

if __name__ == "__main__":
    synth_cinematic_bgm()
