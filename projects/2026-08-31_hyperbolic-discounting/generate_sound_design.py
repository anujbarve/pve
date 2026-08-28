#!/usr/bin/env python3
"""
Sound Design & BGM Engine for Hyperbolic Discounting (The Present Bias Trap)
Generates:
1. Procedural SFX: digital alarm beeps, snooze slams, hyperbolic surges, neural fractures, vault locks, revelation chimes.
2. Cinematic BGM: Evolving psychological tension & D-minor ambient documentary score.
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

def synth_alarm_digital_beep():
    """Crisp high-tech dual-tone digital alarm beep."""
    t = np.linspace(0, 0.18, int(SR * 0.18), False)
    f1 = 2048
    f2 = 4096
    tone = (0.7 * np.sin(2 * np.pi * f1 * t) + 0.3 * np.sin(2 * np.pi * f2 * t))
    env = np.sin(np.pi * t / 0.18) ** 1.5
    write_wav("alarm_digital_beep.wav", tone * env, peak=0.8)

def synth_sub_impact():
    """Deep exponential sub-bass drop with resonant bottom end."""
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    freq = np.geomspace(85, 28, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2.8)
    body = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 4.0) * 0.5
    sig = np.tanh(sub * 1.5 + body)
    write_wav("sub_impact.wav", sig, peak=0.85)

def synth_tactile_snooze_slam():
    """Heavy mechanical button smash / physical impulse."""
    t = np.linspace(0, 0.45, int(SR * 0.45), False)
    thud_freq = np.geomspace(160, 35, len(t))
    thud = np.sin(2 * np.pi * thud_freq * t) * np.exp(-t * 18)
    click = np.sin(2 * np.pi * 3800 * t) * np.exp(-t * 90) * 0.6
    noise = np.random.normal(0, 0.4, len(t)) * np.exp(-t * 30)
    sig = np.tanh(thud * 1.6 + click + noise)
    write_wav("tactile_snooze_slam.wav", sig, peak=0.9)

def synth_whoosh_swoop():
    """Fast cinematic air whoosh / camera whip."""
    t = np.linspace(0, 0.38, int(SR * 0.38), False)
    noise = np.random.normal(0, 1, len(t))
    sweep = np.sin(np.pi * t / 0.38) ** 2
    env = np.exp(-((t - 0.19) ** 2) / 0.009)
    sig = np.convolve(noise * env * sweep, np.ones(18) / 18, mode='same')
    write_wav("whoosh_swoop.wav", sig, peak=0.8)

def synth_hyperbolic_surge():
    """Exponentially rising resonant tension curve chirp."""
    t = np.linspace(0, 1.4, int(SR * 1.4), False)
    freq = np.geomspace(90, 1400, len(t))
    env = np.exp((t - 1.4) * 3.5)
    sig = np.sin(2 * np.pi * freq * t) * env
    harm = np.sin(4 * np.pi * freq * t) * env * 0.3
    sub_grow = np.sin(2 * np.pi * 45 * t) * env * 0.5
    write_wav("hyperbolic_surge.wav", sig + harm + sub_grow, peak=0.8)

def synth_neural_fracture_zap():
    """Low-voltage glitch disconnect / neurological dissonance pulse."""
    t = np.linspace(0, 0.35, int(SR * 0.35), False)
    fm = np.sin(2 * np.pi * 220 * t + 4.0 * np.sin(2 * np.pi * 60 * t)) * np.exp(-t * 12)
    noise = np.random.uniform(-0.4, 0.4, len(t)) * np.exp(-t * 22)
    sig = fm + noise
    write_wav("neural_fracture_zap.wav", sig, peak=0.75)

def synth_vault_lock_snap():
    """Heavy mechanical vault ratchet / solid steel lock clamp."""
    t = np.linspace(0, 0.55, int(SR * 0.55), False)
    snap1 = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 70)
    snap2 = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 90) * 0.5
    metal_body = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 15) * 0.8
    sub_clamp = np.sin(2 * np.pi * 48 * t) * np.exp(-t * 10) * 0.9
    sig = np.tanh(snap1 + snap2 + metal_body + sub_clamp)
    write_wav("vault_lock_snap.wav", sig, peak=0.85)

def synth_revelation_chime():
    """Grand harmonic golden chime for the Ulysses Contract payoff."""
    t = np.linspace(0, 2.8, int(SR * 2.8), False)
    freqs = [587.33, 880.0, 1174.66, 1760.0]  # D-major 9th harmonics
    weights = [0.8, 0.6, 0.4, 0.2]
    sig = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        sig += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 320.0))
    write_wav("revelation_chime.wav", sig, peak=0.85)

def synth_cinematic_bgm():
    """Evolving psychological tension score & ambient drone for Hyperbolic Discounting."""
    print("Synthesizing Hyperbolic Discounting cinematic score...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Analog Sub & Deep Pad Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo = 1.0 + 0.12 * np.sin(2 * np.pi * 0.08 * t)
    drone = (
        0.50 * np.sin(2 * np.pi * 36.71 * t) +
        0.35 * np.sin(2 * np.pi * 55.00 * t + 0.4) +
        0.30 * np.sin(2 * np.pi * 73.42 * t) * lfo +
        0.20 * np.sin(2 * np.pi * 87.31 * t + 0.9)
    )
    
    # 2. Clockwork Pulse / Heartbeat Rhythm (120 BPM = 0.5s period)
    pulse_t = t % 0.5
    tick_sig = np.sin(2 * np.pi * 2600 * pulse_t) * np.exp(-pulse_t * 65)
    sub_pulse = np.sin(2 * np.pi * 58 * pulse_t) * np.exp(-pulse_t * 18)
    rhythm_track = (tick_sig * 0.15 + sub_pulse * 0.40)
    # Rhythm enters smoothly at 6.0s
    rhythm_env = np.clip((t - 6.0) / 4.0, 0, 1.0)
    
    # 3. Minimalist Piano / Glass Ostinato (D4, A4, F4, C5)
    ostinato_notes = [293.66, 440.0, 349.23, 523.25]
    note_dur = 0.5
    piano_track = np.zeros_like(t)
    for i, start_time in enumerate(np.arange(0, TOTAL_DURATION, note_dur)):
        if start_time < TOTAL_DURATION:
            freq = ostinato_notes[i % len(ostinato_notes)]
            t_n = np.linspace(0, 1.2, int(SR * 1.2), False)
            n_sig = (0.7 * np.sin(2 * np.pi * freq * t_n) + 0.3 * np.sin(2 * np.pi * freq * 2 * t_n)) * np.exp(-t_n * 3.2)
            idx_s = int(start_time * SR)
            idx_e = min(len(t), idx_s + len(t_n))
            piano_track[idx_s:idx_e] += n_sig[:idx_e - idx_s] * 0.32
            
    # 4. Tension String / High Overtone (A5 = 880Hz, D6 = 1174Hz)
    tension_env = np.clip((t - 14.0) / 10.0, 0, 1.0)
    tension_string = (0.2 * np.sin(2 * np.pi * 880.0 * t) + 0.15 * np.sin(2 * np.pi * 1174.6 * t)) * tension_env
    
    # 5. Climax Swell (from 26s to end)
    swell_env = np.clip((t - 25.0) / 6.5, 0, 1.0)
    swell = (0.35 * np.sin(2 * np.pi * 220.0 * t) + 0.25 * np.sin(2 * np.pi * 440.0 * t)) * swell_env
    
    bgm = drone + (rhythm_track * rhythm_env) + (piano_track * 0.42) + tension_string + (swell * 0.5)
    bgm = np.tanh(bgm * 1.2)
    
    # Fade in & out
    fade_in = np.linspace(0, 1, int(SR * 1.5))
    fade_out = np.linspace(1, 0, int(SR * 2.5))
    bgm[:len(fade_in)] *= fade_in
    bgm[-len(fade_out):] *= fade_out
    
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    write_wav_path(bgm_path, bgm, peak=0.9)
    print(f"BGM score synthesized: {bgm_path}")
    return bgm_path

def build_all_audio():
    print("=== Step 1: Synthesizing Procedural SFX & Score ===")
    synth_alarm_digital_beep()
    synth_sub_impact()
    synth_tactile_snooze_slam()
    synth_whoosh_swoop()
    synth_hyperbolic_surge()
    synth_neural_fracture_zap()
    synth_vault_lock_snap()
    synth_revelation_chime()
    synth_cinematic_bgm()
    
    print("\n=== Step 2: Multi-Track Mastering Mix ===")
    narration_path = os.path.join(TEMP_DIR, "narration_full.wav")
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    output_path = os.path.join(TEMP_DIR, "master_sound_design.wav")
    
    # SFX Event Placement locked to shot timing from timings.json
    sfx_events = [
        # Shot 01 (0.00s - 6.98s): "At eleven PM, you set an alarm for six in the morning..."
        ("whoosh_swoop.wav", 0.20, -18),
        ("alarm_digital_beep.wav", 2.00, -16),
        ("alarm_digital_beep.wav", 2.30, -17),
        ("sub_impact.wav", 4.60, -14),  # "iron discipline"
        
        # Shot 02 (6.98s - 14.12s): "At six AM, that discipline vanishes..."
        ("whoosh_swoop.wav", 7.00, -18),
        ("alarm_digital_beep.wav", 7.30, -14),
        ("alarm_digital_beep.wav", 7.60, -14),
        ("alarm_digital_beep.wav", 7.90, -14),
        ("tactile_snooze_slam.wav", 9.80, -12), # "hits snooze"
        ("sub_impact.wav", 9.90, -15),
        
        # Shot 03 (14.12s - 21.18s): "steep hyperbolic cliff..."
        ("whoosh_swoop.wav", 14.20, -18),
        ("hyperbolic_surge.wav", 17.20, -15), # "steep hyperbolic cliff"
        ("sub_impact.wav", 18.50, -14),
        
        # Shot 04 (21.18s - 28.24s): "future self is not you—it is a stranger..."
        ("neural_fracture_zap.wav", 21.40, -15), # "not you"
        ("whoosh_swoop.wav", 24.60, -18),
        ("sub_impact.wav", 25.20, -15), # "stranger you can abandon"
        
        # Shot 05 (28.24s - 34.90s): "lock the steering wheel tonight..."
        ("revelation_chime.wav", 28.40, -13), # "win tomorrow"
        ("vault_lock_snap.wav", 31.40, -12), # "lock the steering wheel"
        ("sub_impact.wav", 31.60, -14),
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
