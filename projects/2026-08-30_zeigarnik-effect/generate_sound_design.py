#!/usr/bin/env python3
"""
Sound Design & BGM Engine for The Zeigarnik Effect (The Unclosed Mental Tab)
Generates:
1. Procedural SFX: insomnia hum, dissolve flutter, tension arc, cafe bill stamp, tab warning, pen stroke, closure lock.
2. Cinematic BGM: Nocturnal cognitive tension & resolution score.
3. Master 3-Layer Audio Mix: Voiceover + BGM + SFX with -14 LUFS loudness mastering.
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

def write_wav(filename, data, peak=0.75):
    data = data / (np.max(np.abs(data)) + 1e-7) * peak
    wav_data = (data * 32767).astype(np.int16)
    wavfile.write(os.path.join(SFX_DIR, filename), SR, wav_data)

def write_wav_path(path, data, peak=0.85):
    data = data / (np.max(np.abs(data)) + 1e-7) * peak
    wav_data = (data * 32767).astype(np.int16)
    wavfile.write(path, SR, wav_data)

def synth_insomnia_hum():
    """Nocturnal brain hum & low-frequency mental loop."""
    t = np.linspace(0, 2.5, int(SR * 2.5), False)
    drone = np.sin(2 * np.pi * 55.0 * t) + 0.5 * np.sin(2 * np.pi * 110.0 * t)
    beating = np.sin(2 * np.pi * 4.0 * t) * 0.3
    sig = (drone * (1.0 + beating)) * np.exp(-t * 0.8)
    write_wav("insomnia_hum.wav", sig, peak=0.8)

def synth_dissolve_dust():
    """Granular decaying dust whisper when completed tasks vanish."""
    t = np.linspace(0, 1.5, int(SR * 1.5), False)
    noise = np.random.normal(0, 1, len(t))
    env = np.exp(-t * 3.5)
    sig = np.convolve(noise * env, np.ones(30) / 30, mode='same')
    write_wav("dissolve_dust.wav", sig, peak=0.7)

def synth_tension_arc():
    """Electric cognitive tension arc / burning open loop."""
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    freq = np.linspace(800, 2400, len(t))
    carrier = np.sin(2 * np.pi * freq * t)
    mod = np.sin(2 * np.pi * 18.0 * t)
    env = np.sin(np.pi * t / 2.0) ** 1.5
    sub = np.sin(2 * np.pi * 65.0 * t) * env * 0.5
    sig = (carrier * (0.6 + 0.4 * mod) + sub) * env
    write_wav("tension_arc.wav", sig, peak=0.8)

def synth_vintage_stamp():
    """Tactile vintage cafe bill stamp & receipt impact."""
    t = np.linspace(0, 0.4, int(SR * 0.4), False)
    thud = np.sin(2 * np.pi * 110.0 * t) * np.exp(-t * 35)
    click = (np.random.rand(len(t)) - 0.5) * np.exp(-t * 80)
    sig = thud * 0.7 + click * 0.4
    write_wav("vintage_stamp.wav", sig, peak=0.85)

def synth_tab_warning():
    """Neural memory bus buzz & unclosed tab alert wave."""
    t = np.linspace(0, 1.8, int(SR * 1.8), False)
    freq = np.geomspace(350, 1400, len(t))
    pulse = np.sin(2 * np.pi * freq * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 12.0 * t))
    env = np.exp(-t * 1.8)
    sig = pulse * env
    write_wav("tab_warning.wav", sig, peak=0.75)

def synth_pen_stroke():
    """Tactile paper friction & writing stroke."""
    t = np.linspace(0, 0.5, int(SR * 0.5), False)
    noise = np.random.normal(0, 0.5, len(t))
    b, a = np.array([0.2, -0.1]), np.array([1.0, -0.8])
    friction = noise * np.sin(np.pi * t / 0.5)
    write_wav("pen_stroke.wav", friction, peak=0.7)

def synth_closure_lock():
    """Grand harmonic golden chime + grounded satisfying closure click."""
    t = np.linspace(0, 3.5, int(SR * 3.5), False)
    freqs = [587.33, 880.0, 1174.66, 1760.0]  # D-major harmonic chime
    weights = [0.7, 0.5, 0.4, 0.2]
    sig = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        sig += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 360.0))
    sub_click = np.sin(2 * np.pi * 50.0 * t) * np.exp(-t * 15) * 0.5
    full = sig + sub_click
    write_wav("closure_lock.wav", full, peak=0.85)

def synth_cinematic_bgm():
    """Evolving cinematic nocturnal & psychological documentary score."""
    print("Synthesizing Zeigarnik Effect cinematic score...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Nocturnal Sub & Deep Pad Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo = 1.0 + 0.12 * np.sin(2 * np.pi * 0.08 * t)
    drone = (
        0.50 * np.sin(2 * np.pi * 36.71 * t) +
        0.35 * np.sin(2 * np.pi * 55.00 * t + 0.5) +
        0.30 * np.sin(2 * np.pi * 73.42 * t) * lfo +
        0.20 * np.sin(2 * np.pi * 87.31 * t + 1.0)
    )
    
    # 2. Clockwork Working-Memory Pulse (120 BPM = 0.5s period)
    pulse_t = t % 0.5
    tick_sig = np.sin(2 * np.pi * 2600 * pulse_t) * np.exp(-pulse_t * 65)
    sub_click = np.sin(2 * np.pi * 60 * pulse_t) * np.exp(-pulse_t * 22)
    rhythm_track = (tick_sig * 0.12 + sub_click * 0.35)
    # Rhythm enters smoothly at Shot 2 (6.6s)
    rhythm_env = np.clip((t - 6.66) / 4.0, 0, 1.0)
    
    # 3. Minimalist Piano / Glass Ostinato (D4, F4, A4, E5)
    ostinato_notes = [293.66, 349.23, 440.0, 659.25]
    note_dur = 0.5
    piano_track = np.zeros_like(t)
    for i, start_time in enumerate(np.arange(0, TOTAL_DURATION, note_dur)):
        if start_time < TOTAL_DURATION:
            freq = ostinato_notes[i % len(ostinato_notes)]
            t_n = np.linspace(0, 1.2, int(SR * 1.2), False)
            n_sig = (0.7 * np.sin(2 * np.pi * freq * t_n) + 0.3 * np.sin(2 * np.pi * freq * 2 * t_n)) * np.exp(-t_n * 3.0)
            idx_s = int(start_time * SR)
            idx_e = min(len(t), idx_s + len(t_n))
            piano_track[idx_s:idx_e] += n_sig[:idx_e - idx_s] * 0.3
            
    # 4. Climax / Harmonic Resolution Swell (from Shot 4 to Shot 5: 28s to end)
    swell_env = np.clip((t - 28.0) / 8.0, 0, 1.0)
    swell = (0.35 * np.sin(2 * np.pi * 220.0 * t) + 0.25 * np.sin(2 * np.pi * 440.0 * t) + 0.20 * np.sin(2 * np.pi * 587.33 * t)) * swell_env
    
    bgm = drone + (rhythm_track * rhythm_env) + (piano_track * 0.4) + (swell * 0.5)
    bgm = np.tanh(bgm * 1.2)
    
    # Smooth fades
    fade_in = np.linspace(0, 1, int(SR * 1.5))
    fade_out = np.linspace(1, 0, int(SR * 3.0))
    bgm[:len(fade_in)] *= fade_in
    bgm[-len(fade_out):] *= fade_out
    
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    write_wav_path(bgm_path, bgm, peak=0.9)
    print(f"BGM score synthesized: {bgm_path}")
    return bgm_path

def build_all_audio():
    print("=== Step 1: Synthesizing Procedural SFX & Score ===")
    synth_insomnia_hum()
    synth_dissolve_dust()
    synth_tension_arc()
    synth_vintage_stamp()
    synth_tab_warning()
    synth_pen_stroke()
    synth_closure_lock()
    synth_cinematic_bgm()
    
    print("\n=== Step 2: Multi-Track Mastering Mix ===")
    narration_path = os.path.join(TEMP_DIR, "narration_full.wav")
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    output_path = os.path.join(TEMP_DIR, "master_sound_design.wav")
    
    # SFX Event Placement locked to shot timings:
    # Shot 01: 0.00s - 6.66s
    # Shot 02: 6.66s - 13.80s
    # Shot 03: 13.80s - 24.62s
    # Shot 04: 24.62s - 32.64s
    # Shot 05: 32.64s - 40.90s
    sfx_events = [
        # Shot 01: The Midnight Loop
        ("insomnia_hum.wav", 0.30, -15),
        ("tension_arc.wav", 3.20, -16),     # "unfinished email from 3 PM"
        
        # Shot 02: The Asymmetry
        ("dissolve_dust.wav", 7.20, -15),    # "forgot the 10 tasks you finished"
        ("tension_arc.wav", 10.50, -14),     # "one open loop refuses to let you rest"
        
        # Shot 03: The Berlin Waiter
        ("tab_warning.wav", 14.20, -17),     # "Berlin waiters remembered unpaid orders"
        ("vintage_stamp.wav", 20.80, -13),   # "the instant the bill was settled"
        ("dissolve_dust.wav", 21.20, -16),
        
        # Shot 04: The Open Mental Tab
        ("tab_warning.wav", 25.00, -15),     # "treats an unfinished goal like an open tab"
        ("tension_arc.wav", 28.50, -16),     # "burning active working memory"
        
        # Shot 05: The Cognitive Closure
        ("pen_stroke.wav", 34.50, -14),      # "simply writing down the next step"
        ("closure_lock.wav", 36.80, -13),    # "closing the tab"
    ]
    
    inputs = ["-i", narration_path, "-i", bgm_path]
    filter_parts = []
    
    # Voiceover input
    filter_parts.append("[0:a]volume=1.0[voice]")
    
    # BGM input at -23dB
    bgm_gain = 10 ** (-23.0 / 20.0)
    filter_parts.append(f"[1:a]volume={bgm_gain:.4f}[bgm]")
    
    mix_sources = ["[voice]", "[bgm]"]
    
    for idx, (sfx_file, start_sec, gain_db) in enumerate(sfx_events, start=2):
        sfx_path = os.path.join(SFX_DIR, sfx_file)
        inputs.extend(["-i", sfx_path])
        delay_ms = int(start_sec * 1000)
        gain_linear = 10 ** (gain_db / 20.0)
        filter_parts.append(f"[{idx}:a]volume={gain_linear:.3f},adelay={delay_ms}|{delay_ms}[sfx{idx}]")
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
        output_path
    ]
    
    print("Mixing Voiceover + Cinematic BGM + Procedural SFX into master audio...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Master soundtrack complete: {output_path}")
    else:
        print(f"Error mixing audio:\n{res.stderr}")

if __name__ == "__main__":
    build_all_audio()
