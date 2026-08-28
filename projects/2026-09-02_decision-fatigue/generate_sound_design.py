#!/usr/bin/env python3
"""
Sound Design & BGM Engine for Decision Fatigue (Why Willpower Drains by 9 PM)
Generates:
1. Procedural SFX: hums, sub-drops, metabolic burns, power downs, gavel strikes, lock chimes.
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
    
    # 1. Refrigerator Ambient Hum & Sub Drone (Nighttime isolation)
    t = np.linspace(0, 3.0, int(SR * 3.0), False)
    hum = 0.6 * np.sin(2 * np.pi * 60.0 * t) + 0.3 * np.sin(2 * np.pi * 120.0 * t) + 0.1 * np.sin(2 * np.pi * 180.0 * t)
    noise = np.random.normal(0, 0.05, len(t))
    env = np.exp(-t * 0.6)
    write_wav("fridge_hum.wav", (hum + noise) * env, peak=0.75)
    
    # 2. Freeze Sub Drop (Mental paralysis / staring blankly)
    t = np.linspace(0, 2.5, int(SR * 2.5), False)
    freq = np.geomspace(95, 28, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 1.8)
    chime = np.sin(2 * np.pi * 1480 * t) * np.exp(-t * 3.5) * 0.25
    write_wav("freeze_sub.wav", np.tanh(sub * 1.3) + chime, peak=0.85)
    
    # 3. Glucose Siphon / Neural Drain Zap
    t = np.linspace(0, 0.8, int(SR * 0.8), False)
    fm_mod = np.sin(2 * np.pi * 85 * t) * 400
    carrier = np.sin(2 * np.pi * (600 + fm_mod) * t)
    noise = np.random.uniform(-0.4, 0.4, len(t))
    env = np.exp(-t * 5.0)
    write_wav("glucose_drain.wav", (carrier * 0.6 + noise * 0.4) * env, peak=0.75)
    
    # 4. Heavy Sub-Bass Impact (Biological Fuel Depleted)
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    freq = np.geomspace(110, 30, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2.2)
    punch = np.sin(2 * np.pi * 70 * t[:int(SR*0.06)]) * np.exp(-t[:int(SR*0.06)] * 80)
    full_punch = np.zeros_like(t)
    full_punch[:len(punch)] = punch * 0.8
    write_wav("depletion_impact.wav", np.tanh(sub * 1.5) + full_punch, peak=0.90)
    
    # 5. Downshift Powerdown (Turbine / Prefrontal Grid fading)
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    freq = np.geomspace(800, 75, len(t))
    sweep = np.sin(2 * np.pi * freq * t) * np.exp(-t * 1.5)
    low_rumble = np.sin(2 * np.pi * 45 * t) * np.exp(-t * 1.2) * 0.5
    write_wav("downshift_powerdown.wav", np.tanh((sweep + low_rumble) * 1.2), peak=0.80)
    
    # 6. Mechanical Relay Switch / Impulse Click
    t = np.linspace(0, 0.15, int(SR * 0.15), False)
    click = np.sin(2 * np.pi * 2800 * t) * np.exp(-t * 90)
    body = np.sin(2 * np.pi * 320 * t) * np.exp(-t * 50) * 0.7
    write_wav("relay_click.wav", click + body, peak=0.80)
    
    # 7. Judicial Gavel Impact (Acoustic wood strike + sub resonance)
    t = np.linspace(0, 1.8, int(SR * 1.8), False)
    impact = np.sin(2 * np.pi * 140 * t) * np.exp(-t * 18)
    wood_crack = np.sin(2 * np.pi * 1250 * t) * np.exp(-t * 90) * 0.6
    sub_tail = np.sin(2 * np.pi * 48 * t) * np.exp(-t * 3.0) * 0.7
    write_wav("gavel_impact.wav", impact + wood_crack + sub_tail, peak=0.85)
    
    # 8. Graph Plummet Whoosh (Rapid plunge)
    t = np.linspace(0, 1.2, int(SR * 1.2), False)
    noise = np.random.normal(0, 1, len(t))
    freq_sweep = np.geomspace(2400, 180, len(t))
    filter_sig = noise * np.sin(2 * np.pi * freq_sweep * t)
    env = np.sin(np.pi * (t / 1.2) ** 0.8)
    write_wav("graph_plummet.wav", filter_sig * env, peak=0.75)
    
    # 9. Golden Routine Lock Chime (High crystalline clarity + harmonic lock)
    t = np.linspace(0, 3.0, int(SR * 3.0), False)
    freqs = [587.33, 880.00, 1174.66, 1760.00, 2349.32] # D-major 9th
    weights = [0.7, 0.5, 0.4, 0.3, 0.2]
    chime = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        chime += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 350.0))
    write_wav("routine_lock_chime.wav", chime, peak=0.85)

def synth_cinematic_bgm():
    print("Synthesizing custom cinematic score for Decision Fatigue...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Analog Sub & Deep Cinematic Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo = 1.0 + 0.12 * np.sin(2 * np.pi * 0.08 * t)
    drone = (
        0.50 * np.sin(2 * np.pi * 36.71 * t) +
        0.35 * np.sin(2 * np.pi * 55.00 * t + 0.4) +
        0.30 * np.sin(2 * np.pi * 73.42 * t) * lfo +
        0.20 * np.sin(2 * np.pi * 87.31 * t + 0.8)
    )
    
    # 2. Subtle Heartbeat / Metabolic Pulse (100 BPM = 0.6s period)
    pulse_period = 0.60
    pulse_t = t % pulse_period
    heart_sub = np.sin(2 * np.pi * 52 * pulse_t) * np.exp(-pulse_t * 18)
    heart_click = np.sin(2 * np.pi * 95 * pulse_t) * np.exp(-pulse_t * 35) * 0.4
    heartbeat = heart_sub + heart_click
    
    # Fade heartbeat in at 10.0s, keep rolling through Act 4
    heart_env = np.clip((t - 10.0) / 4.0, 0, 1.0) * np.clip((50.0 - t) / 3.0, 0, 1.0)
    
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
            
    # Glass track enters smoothly at 18.0s
    glass_env = np.clip((t - 18.0) / 4.0, 0, 1.0)
    
    # 4. Cinematic Tension Strings & Swell (Act 4 -> Act 5, 30s to end)
    swell_env = np.clip((t - 32.0) / 10.0, 0, 1.0)
    strings = (
        0.30 * np.sin(2 * np.pi * 220.0 * t) +
        0.25 * np.sin(2 * np.pi * 329.63 * t + 0.3) +
        0.20 * np.sin(2 * np.pi * 440.0 * t + 0.6)
    ) * swell_env
    
    # 5. Golden Climax Harmonic Bed (Act 5 payoff, 44s to end)
    climax_env = np.clip((t - 44.0) / 3.0, 0, 1.0)
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
    # Shot 1: 0.00s - 10.58s
    # Shot 2: 10.58s - 21.16s
    # Shot 3: 21.16s - 31.74s
    # Shot 4: 31.74s - 44.72s
    # Shot 5: 44.72s - 53.62s
    sfx_events = [
        # Shot 1: Nighttime Paralysis
        ("fridge_hum.wav", 0.20, -18),
        ("freeze_sub.wav", 6.80, -14),           # "stand paralyzed before an open refrigerator"
        
        # Shot 2: Neural Fuel Tank
        ("glucose_drain.wav", 11.20, -15),       # "Every single choice"
        ("glucose_drain.wav", 14.50, -16),       # "from drafting an email"
        ("depletion_impact.wav", 18.00, -14),    # "prefrontal glucose"
        
        # Shot 3: The Cognitive Downshift
        ("downshift_powerdown.wav", 22.00, -14), # "aggressively downshifts into survival mode"
        ("relay_click.wav", 27.50, -16),         # "defaulting to pure impulse"
        ("freeze_sub.wav", 28.20, -15),
        
        # Shot 4: The Judicial Curve (Court Study)
        ("gavel_impact.wav", 32.20, -13),        # "In landmark court studies, judges granted parole"
        ("graph_plummet.wav", 37.00, -15),       # "plummeted to zero before lunch"
        ("relay_click.wav", 41.50, -16),         # "saying no requires less mental energy"
        
        # Shot 5: The Shield of Routine (Payoff)
        ("routine_lock_chime.wav", 45.20, -14),  # "The most disciplined minds..."
        ("relay_click.wav", 48.80, -16),         # "ruthlessly eliminate trivial decisions"
        ("routine_lock_chime.wav", 50.00, -15),  # golden resolution
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
