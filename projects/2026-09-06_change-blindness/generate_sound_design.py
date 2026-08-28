#!/usr/bin/env python3
"""
Sound Design & BGM Engine for Change Blindness (The Illusion of Seeing Everything)
Generates:
1. Procedural SFX: door glide whooshes, swap glitch chirps, discrepancy pings, foveal lock pings, neural reconstruction sweeps, golden manifesto chimes.
2. Cinematic BGM: Multi-act minimalist documentary score with D-minor pad, urban pulse, glass ostinato, and harmonic resolution.
3. Master 3-Layer Audio Mix: Voiceover + BGM + SFX with -14.0 LUFS loudness mastering.
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
    
    # 1. Door Glide Whoosh (Heavy wood / air displacement sweep)
    t = np.linspace(0, 1.6, int(SR * 1.6), False)
    noise = np.random.normal(0, 0.8, len(t))
    freq_sweep = np.geomspace(120, 750, len(t))
    filter_sig = noise * np.sin(2 * np.pi * freq_sweep * t)
    env = np.sin(np.pi * (t / 1.6) ** 0.85)
    sub = np.sin(2 * np.pi * 65 * t) * np.exp(-t * 2.0) * 0.4
    write_wav("door_glide.wav", (filter_sig * 0.7 + sub) * env, peak=0.85)
    
    # 2. Perceptual Swap Glitch / Disconnect Zap
    t = np.linspace(0, 0.6, int(SR * 0.6), False)
    fm_mod = np.sin(2 * np.pi * 95 * t) * 550
    carrier = np.sin(2 * np.pi * (480 + fm_mod) * t)
    noise = np.random.uniform(-0.3, 0.3, len(t))
    env = np.exp(-t * 8.0)
    write_wav("swap_glitch.wav", (carrier * 0.7 + noise * 0.3) * env, peak=0.80)
    
    # 3. Discrepancy Vector Ping (High-frequency cognitive mismatch marker)
    t = np.linspace(0, 0.9, int(SR * 0.9), False)
    ping1 = np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 6.0)
    ping2 = np.sin(2 * np.pi * 2640 * t) * np.exp(-t * 9.0) * 0.5
    sub_click = np.sin(2 * np.pi * 120 * t[:int(SR*0.05)]) * np.exp(-t[:int(SR*0.05)] * 70)
    sig = np.zeros_like(t)
    sig[:len(sub_click)] += sub_click * 0.5
    sig += (ping1 + ping2) * 0.8
    write_wav("discrepancy_ping.wav", sig, peak=0.82)
    
    # 4. Foveal Lock / Reticle Snap (Precision optical focus impulse)
    t = np.linspace(0, 0.4, int(SR * 0.4), False)
    click = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 80)
    tone = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 12) * 0.6
    sub = np.sin(2 * np.pi * 90 * t) * np.exp(-t * 25) * 0.5
    write_wav("foveal_lock.wav", click + tone + sub, peak=0.85)
    
    # 5. Deep Revelation Sub-Impact (95Hz -> 30Hz exponential pitch drop)
    t = np.linspace(0, 2.2, int(SR * 2.2), False)
    freq = np.geomspace(95, 28, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 1.8)
    punch = np.sin(2 * np.pi * 80 * t[:int(SR*0.06)]) * np.exp(-t[:int(SR*0.06)] * 60)
    sig = np.tanh(sub * 1.4)
    sig[:len(punch)] += punch * 0.6
    write_wav("revelation_sub.wav", sig, peak=0.90)
    
    # 6. Neural Infill Shimmer / Sweep (Multi-harmonic forward-model sweep)
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    freqs = [659.25, 987.77, 1318.51, 1975.53] # E-minor 9th
    shimmer = np.zeros_like(t)
    for i, f in enumerate(freqs):
        sweep_f = f * (1.0 + 0.08 * np.sin(2 * np.pi * 3.5 * t))
        shimmer += (0.4 / (i + 1)) * np.sin(2 * np.pi * sweep_f * t)
    noise_air = np.random.normal(0, 0.15, len(t)) * np.sin(np.pi * (t / 2.0))
    env = np.sin(np.pi * (t / 2.0) ** 0.9)
    write_wav("neural_sweep.wav", (shimmer + noise_air) * env, peak=0.80)
    
    # 7. Golden Manifesto Resolution Chime (D-major 9th crystalline clarity)
    t = np.linspace(0, 3.2, int(SR * 3.2), False)
    chord_freqs = [587.33, 880.00, 1174.66, 1760.00, 2349.32]
    chord_weights = [0.7, 0.5, 0.4, 0.3, 0.2]
    chime = np.zeros_like(t)
    for f, w in zip(chord_freqs, chord_weights):
        chime += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 400.0))
    write_wav("manifesto_chime.wav", chime, peak=0.88)
    
    # 8. Ambient Urban Texture & Low Hum
    t = np.linspace(0, 3.5, int(SR * 3.5), False)
    hum = 0.5 * np.sin(2 * np.pi * 50 * t) + 0.3 * np.sin(2 * np.pi * 100 * t)
    traffic_noise = np.random.normal(0, 0.06, len(t))
    env = np.exp(-t * 0.35)
    write_wav("urban_ambient.wav", (hum + traffic_noise) * env, peak=0.70)

def synth_cinematic_bgm():
    print("Synthesizing custom cinematic score for Change Blindness...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Deep Analog Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo = 1.0 + 0.10 * np.sin(2 * np.pi * 0.09 * t)
    drone = (
        0.50 * np.sin(2 * np.pi * 36.71 * t) +
        0.35 * np.sin(2 * np.pi * 55.00 * t + 0.3) +
        0.30 * np.sin(2 * np.pi * 73.42 * t) * lfo +
        0.20 * np.sin(2 * np.pi * 87.31 * t + 0.7)
    )
    
    # 2. Subtle Cognitive Heartbeat Pulse (110 BPM = 0.545s period)
    pulse_period = 0.545
    pulse_t = t % pulse_period
    heart_sub = np.sin(2 * np.pi * 55 * pulse_t) * np.exp(-pulse_t * 20)
    heart_click = np.sin(2 * np.pi * 110 * pulse_t) * np.exp(-pulse_t * 40) * 0.35
    heartbeat = heart_sub + heart_click
    
    # Pulse fades in at 9.0s (Shot 2 start) and continues until Shot 5
    heart_env = np.clip((t - 9.0) / 3.0, 0, 1.0) * np.clip((38.0 - t) / 2.5, 0, 1.0)
    
    # 3. Minimalist Glass / Celesta Ostinato (D4=293.66, F4=349.23, A4=440.00, C5=523.25, E5=659.25)
    ostinato_notes = [293.66, 440.0, 349.23, 523.25, 659.25, 440.0, 349.23, 293.66]
    note_dur = 0.545
    glass_track = np.zeros_like(t)
    for i, start_time in enumerate(np.arange(0, TOTAL_DURATION, note_dur)):
        if start_time < TOTAL_DURATION:
            freq = ostinato_notes[i % len(ostinato_notes)]
            t_n = np.linspace(0, 1.1, int(SR * 1.1), False)
            n_sig = (0.75 * np.sin(2 * np.pi * freq * t_n) + 0.25 * np.sin(2 * np.pi * freq * 2 * t_n)) * np.exp(-t_n * 3.0)
            idx_s = int(start_time * SR)
            idx_e = min(len(t), idx_s + len(t_n))
            glass_track[idx_s:idx_e] += n_sig[:idx_e - idx_s] * 0.35
            
    # Glass track enters smoothly at 15.0s
    glass_env = np.clip((t - 15.0) / 4.0, 0, 1.0)
    
    # 4. Cinematic Tension Strings & Harmonic Overtone (Shot 3 -> Shot 4, 20s to end)
    swell_env = np.clip((t - 24.0) / 8.0, 0, 1.0)
    strings = (
        0.30 * np.sin(2 * np.pi * 220.0 * t) +
        0.25 * np.sin(2 * np.pi * 329.63 * t + 0.4) +
        0.20 * np.sin(2 * np.pi * 440.0 * t + 0.8)
    ) * swell_env
    
    # 5. Golden Climax Harmonic Bed (Shot 5 payoff, 37s to end)
    climax_env = np.clip((t - 37.0) / 2.5, 0, 1.0)
    climax_bed = (
        0.45 * np.sin(2 * np.pi * 146.83 * t) + # D3
        0.35 * np.sin(2 * np.pi * 220.00 * t) + # A3
        0.30 * np.sin(2 * np.pi * 293.66 * t) + # D4
        0.25 * np.sin(2 * np.pi * 370.00 * t)   # F#4 (Major resolution!)
    ) * climax_env
    
    bgm = drone + (heartbeat * heart_env * 0.35) + (glass_track * glass_env * 0.40) + strings + climax_bed
    bgm = np.tanh(bgm * 1.1)
    
    # Master BGM In / Out Envelopes
    fade_in = np.linspace(0, 1, int(SR * 1.5))
    fade_out = np.linspace(1, 0, int(SR * 2.5))
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
    
    # Precise SFX events synced with shots and visual keyframes:
    # Shot 1: 0.00s - 9.62s
    # Shot 2: 9.62s - 18.60s
    # Shot 3: 18.60s - 28.86s
    # Shot 4: 28.86s - 37.04s
    # Shot 5: 37.04s - 44.66s
    sfx_events = [
        # Shot 1: The Door Experiment
        ("urban_ambient.wav", 0.20, -18),
        ("door_glide.wav", 4.80, -14),           # "two workers carry a wooden door right between you"
        ("swap_glitch.wav", 6.80, -15),          # "swapping the person with a total stranger"
        
        # Shot 2: The Blind Conversation
        ("revelation_sub.wav", 9.80, -14),       # "Over half of all people never notice"
        ("discrepancy_ping.wav", 13.20, -16),    # "continuing the conversation for minutes"
        ("discrepancy_ping.wav", 15.80, -15),    # "entirely new face"
        
        # Shot 3: The 2-Degree Fovea
        ("foveal_lock.wav", 19.20, -15),         # "Your eyes don't record a high-definition world"
        ("foveal_lock.wav", 22.50, -14),         # "confined to just two tiny degrees"
        ("discrepancy_ping.wav", 26.00, -16),    # "width of your thumbnail"
        
        # Shot 4: The Neural Reconstruction
        ("neural_sweep.wav", 29.20, -14),        # "Everything outside that narrow spotlight"
        ("swap_glitch.wav", 33.00, -16),         # "low-resolution prediction"
        ("neural_sweep.wav", 34.50, -15),        # "filled in by memory and expectation"
        
        # Shot 5: The Minimal Summary (Payoff)
        ("manifesto_chime.wav", 37.20, -14),     # "You don't see reality as it exists"
        ("foveal_lock.wav", 40.50, -16),         # "fleeting summary"
        ("manifesto_chime.wav", 42.00, -15),     # Final resolution
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
