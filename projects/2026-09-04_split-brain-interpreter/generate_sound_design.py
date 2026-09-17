#!/usr/bin/env python3
"""
Jack Butcher / Naval Ravikant Audio Engine (V2 - Prominent Tactile Edition):
- Crystal Clear Vocal: Mastered at -14.0 LUFS
- Meditative Ambient Piano: Kept exactly as loved by user (-19.0 dB)
- Prominent Tactile SFX: Crisp mechanical switch snaps, pen clicks, line draws (-10 dB to -13 dB)
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

def write_wav(filename, data, peak=0.92):
    data = data / (np.max(np.abs(data)) + 1e-7) * peak
    wav_data = (data * 32767).astype(np.int16)
    wavfile.write(os.path.join(SFX_DIR, filename), SR, wav_data)

def synth_sfx_library():
    print("Synthesizing prominent tactile SFX library...")
    
    # 1. Crisp Mechanical Switch Snap (for breaker trip / switch)
    t = np.linspace(0, 0.14, int(SR * 0.14), False)
    click = np.sin(2 * np.pi * 4200 * t) * np.exp(-t * 200)
    metal = np.sin(2 * np.pi * 1750 * t) * np.exp(-t * 120) * 0.75
    thud = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 50) * 0.85
    noise = np.random.normal(0, 0.35, len(t)) * np.exp(-t * 140)
    write_wav("switch_snap.wav", click + metal + thud + noise, peak=0.95)

    # 2. Prominent Drafting Pen Click (for diagram snap-ins)
    t_c = np.linspace(0, 0.08, int(SR * 0.08), False)
    t_click = np.sin(2 * np.pi * 3600 * t_c) * np.exp(-t_c * 220) + np.sin(2 * np.pi * 820 * t_c) * np.exp(-t_c * 100) * 0.65
    noise_c = np.random.normal(0, 0.25, len(t_c)) * np.exp(-t_c * 260)
    write_wav("tactile_click.wav", t_click + noise_c, peak=0.95)

    # 3. Pen/Chalk Line Draw Friction (for vector line drawing)
    t_d = np.linspace(0, 0.30, int(SR * 0.30), False)
    noise_d = np.random.normal(0, 0.45, len(t_d))
    draw_env = np.sin(np.pi * (t_d / 0.30)) ** 1.6
    f_sweep = np.linspace(1100, 2600, len(t_d))
    draw_sig = noise_d * np.sin(2 * np.pi * f_sweep * t_d) * draw_env
    write_wav("pen_draw.wav", draw_sig, peak=0.90)

    # 4. Deep Grounding Sub-Swell (for mathematical resolutions)
    t_s = np.linspace(0, 1.4, int(SR * 1.4), False)
    sub = np.sin(2 * np.pi * 50.0 * t_s) * (np.sin(np.pi * (t_s / 1.4)) ** 1.8)
    write_wav("sub_swell.wav", sub, peak=0.85)

def synth_meditative_bgm():
    print("Synthesizing user-approved ambient piano score...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    chords = [
        [82.41, 196.00, 246.94, 293.66, 369.99],  # Em9
        [65.41, 196.00, 246.94, 329.63, 392.00],  # Cmaj7
        [48.99, 196.00, 246.94, 293.66, 392.00],  # G
        [73.42, 185.00, 220.00, 329.63, 440.00],  # Dadd9
    ]
    chord_dur = 6.67
    music = np.zeros_like(t)

    for i, start_time in enumerate(np.arange(0, TOTAL_DURATION, chord_dur)):
        c = chords[i % len(chords)]
        idx_s = int(start_time * SR)
        idx_e = min(len(t), idx_s + int(SR * chord_dur * 1.25))
        t_c = np.linspace(0, (idx_e - idx_s) / SR, idx_e - idx_s, False)
        
        chord_sig = np.zeros_like(t_c)
        for f in c:
            amp = 0.5 * np.exp(-t_c * 0.40)
            harm = 0.15 * np.exp(-t_c * 0.75)
            chord_sig += (np.sin(2 * np.pi * f * t_c) * amp + np.sin(2 * np.pi * f * 2 * t_c) * harm)
            
        music[idx_s:idx_e] += chord_sig[:idx_e - idx_s]

    drone = np.sin(2 * np.pi * 41.2 * t) * 0.22 * (1 + 0.08 * np.sin(2 * np.pi * 0.08 * t))
    music = music * 0.55 + drone
    music = np.tanh(music * 0.9)
    music = music / (np.max(np.abs(music)) + 1e-7) * 0.85

    fade_len = int(SR * 2.0)
    music[:fade_len] *= np.linspace(0, 1, fade_len)
    music[-fade_len:] *= np.linspace(1, 0, fade_len)

    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    wav_data = (music * 32767).astype(np.int16)
    wavfile.write(bgm_path, SR, wav_data)
    print(f"Piano score written: {bgm_path}")
    return bgm_path

def build_soundtrack():
    synth_sfx_library()
    synth_meditative_bgm()
    
    print("\n=== Mastering Vocal + Prominent Tactile Mix (-14.0 LUFS) ===")
    narration_path = os.path.join(TEMP_DIR, "narration_full.wav")
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    master_output = os.path.join(TEMP_DIR, "master_sound_design.wav")
    
    # Prominently audible tactile events
    sfx_events = [
        # Shot 01: The Silent Command (0.0s - 10.26s)
        ("tactile_click.wav", 0.05, -10),
        ("pen_draw.wav", 0.10, -11),
        ("tactile_click.wav", 5.00, -10),
        
        # Shot 02: The Severed Bridge (10.26s - 17.64s)
        ("tactile_click.wav", 10.30, -10),
        ("switch_snap.wav", 13.50, -8),
        
        # Shot 03: The Soda Confabulation (17.64s - 28.78s)
        ("tactile_click.wav", 17.70, -10),
        ("pen_draw.wav", 18.10, -11),
        ("switch_snap.wav", 23.50, -8),
        ("sub_swell.wav", 25.00, -12),
        
        # Shot 04: The Left-Brain Interpreter (28.78s - 38.56s)
        ("tactile_click.wav", 28.85, -10),
        ("pen_draw.wav", 29.20, -11),
        ("sub_swell.wav", 33.50, -12),
        
        # Shot 05: The Illusion of Reason (38.56s - 47.78s)
        ("tactile_click.wav", 38.60, -10),
        ("pen_draw.wav", 39.00, -11),
        ("sub_swell.wav", 42.50, -12),
    ]
    
    inputs = ["-i", narration_path, "-i", bgm_path]
    filter_parts = []
    
    filter_parts.append("[0:a]volume=1.0[voice]")
    
    bgm_gain = 10 ** (-19.0 / 20.0) # ~0.1122
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
    
    print("Executing FFmpeg Vocal + Prominent Tactile Mix...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Master soundtrack generated successfully: {master_output}")
    else:
        print(f"Error in master mix:\n{res.stderr}")
        raise RuntimeError("Master mix failed.")

if __name__ == "__main__":
    build_soundtrack()
