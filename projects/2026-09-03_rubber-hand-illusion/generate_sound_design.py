#!/usr/bin/env python3
"""
Sound Design & BGM Engine for The Rubber Hand Illusion (Body Ownership Plasticity)
Generates:
1. Procedural SFX: lab hum, tactile brush strokes, neural sync pings, thermal drops, body ownership swells, hammer whoosh, violent strike impact, cardiac alarm surges, plasticity chimes.
2. Cinematic BGM: 5-act documentary score with D-minor sub-drone, synchronous pulse, glass arpeggio, tension riser, and golden resolution.
3. Master 3-Layer Audio Mix: Voiceover + BGM (-23dB) + SFX (-14 to -18dB) with -14 LUFS loudness mastering.
"""

import os
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess
import json

SR = 44100
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = os.path.join(PROJECT_DIR, ".sfx_library")
TEMP_DIR = os.path.join(PROJECT_DIR, ".temp_audio")
os.makedirs(SFX_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

with open(os.path.join(PROJECT_DIR, "timings.json"), "r") as f:
    TIMINGS = json.load(f)

TOTAL_DURATION = TIMINGS["total_duration"]

def write_wav(filename, data, peak=0.80):
    data = data / (np.max(np.abs(data)) + 1e-7) * peak
    wav_data = (data * 32767).astype(np.int16)
    wavfile.write(os.path.join(SFX_DIR, filename), SR, wav_data)

def write_wav_path(path, data, peak=0.85):
    data = data / (np.max(np.abs(data)) + 1e-7) * peak
    wav_data = (data * 32767).astype(np.int16)
    wavfile.write(path, SR, wav_data)

def synth_sfx_library():
    print("Synthesizing procedural SFX library...")
    
    # 1. Lab Atmosphere & Sub Ambient Hum
    t = np.linspace(0, 3.5, int(SR * 3.5), False)
    hum = 0.5 * np.sin(2 * np.pi * 55.0 * t) + 0.3 * np.sin(2 * np.pi * 110.0 * t)
    noise = np.random.normal(0, 0.04, len(t))
    env = np.exp(-t * 0.4)
    write_wav("lab_hum.wav", (hum + noise) * env, peak=0.70)
    
    # 2. Tactile Paintbrush Stroke (Soft bristle friction whisper)
    t = np.linspace(0, 1.4, int(SR * 1.4), False)
    noise = np.random.normal(0, 1, len(t))
    # Sweep bandpass filter from 1800Hz to 800Hz
    mod = np.sin(np.pi * (t / 1.4))
    sweep_carrier = np.sin(2 * np.pi * (1400 - 600 * (t / 1.4)) * t)
    stroke = noise * (sweep_carrier * 0.4 + 0.6) * mod ** 1.5
    sub_whisper = np.sin(2 * np.pi * 120 * t) * np.exp(-t * 3.0) * 0.2
    write_wav("brush_stroke.wav", stroke + sub_whisper, peak=0.75)
    
    # 3. Neural Synchrony Ping (Phase-lock resonance)
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    freqs = [880.0, 1320.0, 1760.0]
    ping = np.zeros_like(t)
    for f in freqs:
        ping += np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 320.0))
    # Sub-lock thump
    thump = np.sin(2 * np.pi * 75 * t) * np.exp(-t * 12.0) * 0.5
    write_wav("neural_sync_ping.wav", ping + thump, peak=0.80)
    
    # 4. Thermal Drop Drone (Somatosensory cooling)
    t = np.linspace(0, 2.8, int(SR * 2.8), False)
    freq = np.geomspace(160, 42, len(t))
    cold_sweep = np.sin(2 * np.pi * freq * t) * np.exp(-t * 0.8)
    shimmer = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 4.0) * 0.15
    write_wav("thermal_drop.wav", cold_sweep + shimmer, peak=0.80)
    
    # 5. Body Ownership Adoption Swell (Sub thud + cortical lock)
    t = np.linspace(0, 2.4, int(SR * 2.4), False)
    freq = np.geomspace(90, 32, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 1.6)
    chord = (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 277.18 * t) + np.sin(2 * np.pi * 330 * t)) * np.exp(-t * 2.2) * 0.4
    write_wav("ownership_swell.wav", np.tanh(sub * 1.4) + chord, peak=0.85)
    
    # 6. Hammer Fast Strike Whoosh
    t = np.linspace(0, 0.65, int(SR * 0.65), False)
    noise = np.random.normal(0, 1, len(t))
    f_sweep = np.geomspace(3200, 120, len(t))
    whoosh = noise * np.sin(2 * np.pi * f_sweep * t) * (np.sin(np.pi * (t / 0.65)) ** 2)
    write_wav("hammer_whoosh.wav", whoosh, peak=0.85)
    
    # 7. Hammer Strike Impact (Heavy sub-impact + metallic crack)
    t = np.linspace(0, 2.2, int(SR * 2.2), False)
    sub = np.sin(2 * np.pi * np.geomspace(120, 28, len(t)) * t) * np.exp(-t * 2.5)
    crack = (np.sin(2 * np.pi * 950 * t[:int(SR*0.08)]) + np.sin(2 * np.pi * 1800 * t[:int(SR*0.08)])) * np.exp(-t[:int(SR*0.08)] * 60)
    full_crack = np.zeros_like(t)
    full_crack[:len(crack)] = crack * 0.9
    write_wav("hammer_strike_impact.wav", np.tanh(sub * 1.8) + full_crack, peak=0.92)
    
    # 8. Autonomic Threat Alarm & Heart Rate Spike
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    heart_p1 = np.sin(2 * np.pi * 55 * t) * np.exp(-((t - 0.1)**2) * 200)
    heart_p2 = np.sin(2 * np.pi * 65 * t) * np.exp(-((t - 0.45)**2) * 200)
    heart_p3 = np.sin(2 * np.pi * 75 * t) * np.exp(-((t - 0.78)**2) * 200)
    heart_p4 = np.sin(2 * np.pi * 85 * t) * np.exp(-((t - 1.08)**2) * 200)
    alarm = np.sin(2 * np.pi * 1250 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 8 * t)) * np.exp(-t * 1.5) * 0.3
    write_wav("alarm_heart_spike.wav", heart_p1 + heart_p2 + heart_p3 + heart_p4 + alarm, peak=0.85)
    
    # 9. Plasticity Golden Revelation Chime (D-major celestial resolution)
    t = np.linspace(0, 3.2, int(SR * 3.2), False)
    freqs = [587.33, 739.99, 880.00, 1174.66, 1760.00] # D, F#, A, D, A
    weights = [0.8, 0.6, 0.5, 0.4, 0.25]
    chime = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        chime += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 400.0))
    sub_warm = np.sin(2 * np.pi * 146.83 * t) * np.exp(-t * 1.2) * 0.4
    write_wav("plasticity_revelation.wav", chime + sub_warm, peak=0.85)

def synth_cinematic_bgm():
    print("Synthesizing custom cinematic score for The Rubber Hand Illusion...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Analog Sub & Deep Cinematic Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo = 1.0 + 0.15 * np.sin(2 * np.pi * 0.07 * t)
    drone = (
        0.50 * np.sin(2 * np.pi * 36.71 * t) +
        0.35 * np.sin(2 * np.pi * 55.00 * t + 0.5) +
        0.30 * np.sin(2 * np.pi * 73.42 * t) * lfo +
        0.20 * np.sin(2 * np.pi * 87.31 * t + 0.9)
    )
    
    # 2. Tactile Synchrony Pulse (75 BPM = 0.8s period)
    pulse_period = 0.80
    pulse_t = t % pulse_period
    sync_sub = np.sin(2 * np.pi * 58 * pulse_t) * np.exp(-pulse_t * 14)
    sync_tap = np.sin(2 * np.pi * 880 * pulse_t) * np.exp(-pulse_t * 60) * 0.15
    sync_track = sync_sub + sync_tap
    
    # Enter in Act 2 (8.5s) and continue through Act 3
    sync_env = np.clip((t - 8.5) / 3.0, 0, 1.0) * np.clip((28.5 - t) / 2.0, 0, 1.0)
    
    # 3. Glass / Celesta Neural Arpeggio (D4=293.66, F4=349.23, A4=440.00, C5=523.25, D5=587.33)
    ostinato_notes = [293.66, 440.00, 349.23, 523.25, 587.33, 440.00, 349.23, 293.66]
    note_dur = 0.40
    glass_track = np.zeros_like(t)
    for i, start_time in enumerate(np.arange(0, TOTAL_DURATION, note_dur)):
        if start_time < TOTAL_DURATION:
            freq = ostinato_notes[i % len(ostinato_notes)]
            t_n = np.linspace(0, 1.0, int(SR * 1.0), False)
            n_sig = (0.75 * np.sin(2 * np.pi * freq * t_n) + 0.25 * np.sin(2 * np.pi * freq * 2 * t_n)) * np.exp(-t_n * 3.2)
            idx_s = int(start_time * SR)
            idx_e = min(len(t), idx_s + len(t_n))
            glass_track[idx_s:idx_e] += n_sig[:idx_e - idx_s] * 0.35
            
    # Glass track enters during Act 3 (18.0s)
    glass_env = np.clip((t - 18.0) / 3.5, 0, 1.0) * np.clip((38.0 - t) / 2.0, 0, 1.0)
    
    # 4. Cinematic Tension Strings & Threat Rise (28.0s to 36.0s)
    tension_env = np.clip((t - 28.0) / 4.0, 0, 1.0) * np.clip((40.0 - t) / 2.0, 0, 1.0)
    tension_strings = (
        0.35 * np.sin(2 * np.pi * 233.08 * t) + # Bb3 (Dissonant tritone / tension)
        0.30 * np.sin(2 * np.pi * 311.13 * t + 0.3) + # Eb4
        0.25 * np.sin(2 * np.pi * 466.16 * t + 0.6)
    ) * tension_env
    
    # 5. Golden Climax Harmonic Bed (Act 5 Payoff, 39.5s to end)
    climax_env = np.clip((t - 39.5) / 2.5, 0, 1.0)
    climax_bed = (
        0.45 * np.sin(2 * np.pi * 146.83 * t) + # D3
        0.35 * np.sin(2 * np.pi * 220.00 * t) + # A3
        0.30 * np.sin(2 * np.pi * 293.66 * t) + # D4
        0.25 * np.sin(2 * np.pi * 370.00 * t)   # F#4 (Major resolution!)
    ) * climax_env
    
    bgm = drone + (sync_track * sync_env * 0.35) + (glass_track * glass_env * 0.40) + tension_strings + climax_bed
    bgm = np.tanh(bgm * 1.1)
    
    # Master BGM In / Out Envelopes
    fade_in = np.linspace(0, 1, int(SR * 1.5))
    fade_out = np.linspace(1, 0, int(SR * 2.8))
    bgm[:len(fade_in)] *= fade_in
    bgm[-len(fade_out):] *= fade_out
    
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    write_wav_path(bgm_path, bgm, peak=0.88)
    print(f"BGM score written: {bgm_path}")
    return bgm_path

def build_soundtrack():
    synth_sfx_library()
    synth_cinematic_bgm()
    
    print("\n=== Mastering 3-Layer Audio Mix (-14 LUFS) ===")
    narration_path = os.path.join(TEMP_DIR, "narration_full.wav")
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    master_output = os.path.join(TEMP_DIR, "master_sound_design.wav")
    
    # Shot Timings:
    # Shot 1: 0.00s - 8.74s
    # Shot 2: 8.74s - 18.60s
    # Shot 3: 18.60s - 28.46s
    # Shot 4: 28.46s - 39.92s
    # Shot 5: 39.92s - 48.90s
    sfx_events = [
        # Shot 1: The Setup (0.00 - 8.74)
        ("lab_hum.wav", 0.20, -18),
        ("thermal_drop.wav", 5.20, -16),           # "rests in plain view directly on the table"
        
        # Shot 2: Synchronous Binding (8.74 - 18.60)
        ("brush_stroke.wav", 9.20, -14),           # "Two paintbrushes stroke both hands"
        ("brush_stroke.wav", 11.50, -15),          # second synchronized stroke
        ("neural_sync_ping.wav", 14.20, -15),      # "fuse into a single neural event"
        ("brush_stroke.wav", 15.80, -16),
        
        # Shot 3: Body Ownership Plasticity (18.60 - 28.46)
        ("thermal_drop.wav", 19.20, -15),          # "rewrites its body schema"
        ("ownership_swell.wav", 23.00, -14),       # "severing ownership of your real flesh"
        ("neural_sync_ping.wav", 25.50, -16),      # "adopting cold rubber as living biology"
        
        # Shot 4: The Strike & Terror Reflex (28.46 - 39.92)
        ("hammer_whoosh.wav", 29.20, -14),         # "When a hammer suddenly..."
        ("hammer_strike_impact.wav", 29.75, -12),  # impact on rubber hand!
        ("alarm_heart_spike.wav", 30.50, -14),     # "sympathetic nervous system fires"
        ("alarm_heart_spike.wav", 34.00, -16),     # heart spike continues
        
        # Shot 5: The Fragility of Self (39.92 - 48.90)
        ("plasticity_revelation.wav", 40.50, -14), # "Your physical body is not a fixed anatomical fact"
        ("neural_sync_ping.wav", 44.50, -16),      # "rewrite in a single minute"
        ("plasticity_revelation.wav", 45.80, -15), # golden resonance resolution
    ]
    
    inputs = ["-i", narration_path, "-i", bgm_path]
    filter_parts = []
    
    # 1. Voiceover at unity volume
    filter_parts.append("[0:a]volume=1.0[voice]")
    
    # 2. Cinematic BGM at -23.0 dB
    bgm_gain = 10 ** (-23.0 / 20.0)
    filter_parts.append(f"[1:a]volume={bgm_gain:.4f}[bgm]")
    
    mix_sources = ["[voice]", "[bgm]"]
    
    for idx, (sfx_file, start_sec, gain_db) in enumerate(sfx_events, start=2):
        sfx_path = os.path.join(SFX_DIR, sfx_file)
        inputs.extend(["-i", sfx_path])
        delay_ms = int(start_sec * 1000)
        gain_linear = 10 ** (gain_db / 20.0)
        filter_parts.append(f"[{idx}:a]volume={gain_linear:.4f},adelay={delay_ms}|{delay_ms}[sfx{idx}]")
        mix_sources.append(f"[sfx{idx}]")
        
    num_inputs = len(sfx_events) + 2
    mix_str = "".join(mix_sources)
    
    filter_parts.append(
        f"{mix_str}amix=inputs={num_inputs}:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[out]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[out]",
        "-ar", "24000", "-ac", "1",
        master_output
    ]
    
    print("Executing FFmpeg 3-Layer Master Mix...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Master soundtrack generated successfully: {master_output}")
    else:
        print(f"Error in master mix:\n{res.stderr}")
        raise RuntimeError("Master mix failed.")

if __name__ == "__main__":
    build_soundtrack()
