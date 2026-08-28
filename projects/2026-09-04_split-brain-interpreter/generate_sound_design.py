#!/usr/bin/env python3
"""
Sound Design & BGM Engine for The Left-Brain Interpreter (The Illusion of Reason)
Generates:
1. Procedural SFX: optical flash, footsteps, synaptic sever, soda pop fizz, interpreter engine, revelation sub, gold chime.
2. Cinematic BGM: Multi-act minimalist documentary score with D-minor pad, heartbeat pulse, glass ostinato, and golden crescendo.
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
    
    # 1. Optical Flash / Tachistoscope Beam (Light trigger)
    t = np.linspace(0, 0.6, int(SR * 0.6), False)
    strobe_click = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 120)
    optic_ping = np.sin(2 * np.pi * 1850 * t) * np.exp(-t * 14) * 0.4
    low_thump = np.sin(2 * np.pi * 85 * t) * np.exp(-t * 22) * 0.5
    write_wav("optical_flash.wav", strobe_click + optic_ping + low_thump, peak=0.85)
    
    # 2. Footstep Sub / Physical Movement impulse
    t = np.linspace(0, 1.2, int(SR * 1.2), False)
    freq = np.geomspace(80, 35, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 3.5)
    friction = np.random.normal(0, 0.2, len(t)) * np.exp(-t * 25)
    write_wav("footstep_sub.wav", np.tanh(sub * 1.4) + friction, peak=0.80)
    
    # 3. Synaptic Sever / Disconnection Snap (Fracture of corpus callosum)
    t = np.linspace(0, 1.5, int(SR * 1.5), False)
    snap = np.sin(2 * np.pi * 2800 * t) * np.exp(-t * 80)
    fracture_noise = np.random.uniform(-0.5, 0.5, len(t)) * np.exp(-t * 12)
    sub_drop = np.sin(2 * np.pi * np.geomspace(120, 40, len(t)) * t) * np.exp(-t * 2.5) * 0.6
    write_wav("synaptic_sever.wav", snap * 0.6 + fracture_noise * 0.3 + sub_drop, peak=0.85)
    
    # 4. Confabulation Spark / Instant Story Invention
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    f_list = [523.25, 783.99, 1046.50, 1318.51, 1567.98] # C-major 9th sparkle
    spark = np.zeros_like(t)
    for i, freq in enumerate(f_list):
        spark += (1.0 / (i + 1)) * np.sin(2 * np.pi * freq * t) * np.exp(-t * (3.0 + i))
    whoosh = np.random.normal(0, 0.15, len(t)) * np.sin(np.pi * (t / 0.8) ** 0.5) * np.clip(1 - t / 0.8, 0, 1)
    write_wav("confabulation_chime.wav", spark * 0.8 + whoosh * 0.3, peak=0.82)
    
    # 5. Soda Tab Pop & Chilled Fizz
    t = np.linspace(0, 1.0, int(SR * 1.0), False)
    can_crack = np.sin(2 * np.pi * 3600 * t) * np.exp(-t * 140)
    hollow_pop = np.sin(2 * np.pi * 420 * t) * np.exp(-t * 40) * 0.8
    fizz_noise = np.random.normal(0, 0.3, len(t)) * np.exp(-t * 4.0) * np.sin(2 * np.pi * 4500 * t)
    write_wav("can_fizz_click.wav", can_crack + hollow_pop + fizz_noise * 0.4, peak=0.80)
    
    # 6. Interpreter Engine / Dual-Track Neural Schematic Sweep
    t = np.linspace(0, 1.8, int(SR * 1.8), False)
    fm = np.sin(2 * np.pi * 45 * t) * 200
    engine = np.sin(2 * np.pi * (440 + fm) * t) * np.exp(-t * 2.0)
    matrix_sweep = np.random.normal(0, 0.25, len(t)) * np.geomspace(0.01, 1.0, len(t)) * np.exp(-t * 2.2)
    write_wav("interpreter_engine.wav", np.tanh(engine * 0.7 + matrix_sweep * 0.4), peak=0.80)
    
    # 7. Revelation Sub Drop (The Illusion of Reason)
    t = np.linspace(0, 2.5, int(SR * 2.5), False)
    freq = np.geomspace(95, 26, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 1.6)
    warm_bloom = np.sin(2 * np.pi * 110 * t) * np.exp(-t * 2.2) * 0.35
    write_wav("revelation_sub.wav", np.tanh(sub * 1.5) + warm_bloom, peak=0.88)
    
    # 8. Manifesto Gold Strike (Final realization lock)
    t = np.linspace(0, 3.2, int(SR * 3.2), False)
    freqs = [587.33, 880.00, 1174.66, 1760.00, 2349.32] # D-major 9th
    weights = [0.7, 0.5, 0.4, 0.3, 0.2]
    chime = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        chime += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 360.0))
    write_wav("manifesto_strike.wav", chime, peak=0.85)

def synth_cinematic_bgm():
    print("Synthesizing custom cinematic score for Left-Brain Interpreter...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Deep Analog Sub & Atmosphere Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo = 1.0 + 0.15 * np.sin(2 * np.pi * 0.07 * t)
    drone = (
        0.50 * np.sin(2 * np.pi * 36.71 * t) +
        0.35 * np.sin(2 * np.pi * 55.00 * t + 0.4) +
        0.30 * np.sin(2 * np.pi * 73.42 * t) * lfo +
        0.20 * np.sin(2 * np.pi * 87.31 * t + 0.8)
    )
    
    # 2. Subtle Heartbeat / Neural Pulse (100 BPM = 0.6s period)
    pulse_period = 0.60
    pulse_t = t % pulse_period
    heart_sub = np.sin(2 * np.pi * 50 * pulse_t) * np.exp(-pulse_t * 18)
    heart_click = np.sin(2 * np.pi * 92 * pulse_t) * np.exp(-pulse_t * 35) * 0.35
    heartbeat = heart_sub + heart_click
    
    # Fade heartbeat in at 9.0s, keep rolling through Act 4
    heart_env = np.clip((t - 9.0) / 3.5, 0, 1.0) * np.clip((44.0 - t) / 3.0, 0, 1.0)
    
    # 3. Minimalist Glass / Celesta Ostinato (D4=293.66, F4=349.23, A4=440.00, C5=523.25, E5=659.25)
    ostinato_notes = [293.66, 440.0, 349.23, 523.25, 659.25, 440.0, 349.23, 293.66]
    note_dur = 0.60
    glass_track = np.zeros_like(t)
    for i, start_time in enumerate(np.arange(0, TOTAL_DURATION, note_dur)):
        if start_time < TOTAL_DURATION:
            freq = ostinato_notes[i % len(ostinato_notes)]
            t_n = np.linspace(0, 1.2, int(SR * 1.2), False)
            n_sig = (0.75 * np.sin(2 * np.pi * freq * t_n) + 0.25 * np.sin(2 * np.pi * freq * 2 * t_n)) * np.exp(-t_n * 2.8)
            idx_s = int(start_time * SR)
            idx_e = min(len(t), idx_s + len(t_n))
            glass_track[idx_s:idx_e] += n_sig[:idx_e - idx_s] * 0.35
            
    # Glass track enters smoothly at 16.0s
    glass_env = np.clip((t - 16.0) / 4.0, 0, 1.0)
    
    # 4. Cinematic Tension Strings (Act 4 -> Act 5, 27s to end)
    swell_env = np.clip((t - 27.0) / 9.0, 0, 1.0)
    strings = (
        0.30 * np.sin(2 * np.pi * 220.0 * t) +
        0.25 * np.sin(2 * np.pi * 329.63 * t + 0.3) +
        0.20 * np.sin(2 * np.pi * 440.0 * t + 0.6)
    ) * swell_env
    
    # 5. Golden Climax Harmonic Bed (Act 5 payoff, 38s to end)
    climax_env = np.clip((t - 38.0) / 3.0, 0, 1.0)
    climax_bed = (
        0.40 * np.sin(2 * np.pi * 146.83 * t) + # D3
        0.30 * np.sin(2 * np.pi * 220.00 * t) + # A3
        0.25 * np.sin(2 * np.pi * 293.66 * t) + # D4
        0.20 * np.sin(2 * np.pi * 370.00 * t)   # F#4 (Major resolution!)
    ) * climax_env
    
    bgm = drone + (heartbeat * heart_env * 0.30) + (glass_track * glass_env * 0.40) + strings + climax_bed
    bgm = np.tanh(bgm * 1.1)
    
    # Master BGM In / Out Envelopes
    fade_in = np.linspace(0, 1, int(SR * 1.8))
    fade_out = np.linspace(1, 0, int(SR * 3.0))
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
    
    # Exact SFX placement aligned with shots and visual keyframes:
    # Shot 1: 0.00s - 10.26s ("WALK" flash, footstep standing)
    # Shot 2: 10.26s - 17.64s (Bridge severance snap, silent left brain)
    # Shot 3: 17.64s - 28.78s (Interrogation ping, instant confabulation shimmer, soda can click)
    # Shot 4: 28.78s - 38.56s (Gazzaniga engine sweep, retroactive storytelling matrix)
    # Shot 5: 38.56s - 47.78s (Philosophical revelation sub, golden manifesto strike)
    sfx_events = [
        # Shot 1: The Silent Command
        ("optical_flash.wav", 0.40, -15),        # Tachistoscope "WALK" flash
        ("footstep_sub.wav", 5.80, -14),         # "the patient stood up and began walking"
        ("footstep_sub.wav", 8.20, -16),         # walking pace
        
        # Shot 2: The Severed Bridge
        ("synaptic_sever.wav", 10.80, -14),      # "Because the neural bridge between hemispheres was severed"
        ("footstep_sub.wav", 14.50, -17),        # "zero knowledge of the command"
        
        # Shot 3: The Soda Confabulation
        ("optical_flash.wav", 18.00, -16),       # "Yet when asked why he stood up"
        ("confabulation_chime.wav", 22.50, -14), # "his left brain instantly confabulated"
        ("can_fizz_click.wav", 25.40, -15),      # "'I wanted to get a soda'"
        
        # Shot 4: The Left-Brain Interpreter
        ("interpreter_engine.wav", 29.20, -14),  # "Michael Gazzaniga discovered the Left-Brain Interpreter"
        ("synaptic_sever.wav", 34.00, -16),      # "actions it never commanded"
        
        # Shot 5: The Illusion of Reason (Climax Payoff)
        ("revelation_sub.wav", 39.00, -13),      # "You believe you act because you reason..."
        ("manifesto_strike.wav", 43.50, -14),    # "what your brain has already decided to do"
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
