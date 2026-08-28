#!/usr/bin/env python3
"""
Sound Design & BGM Engine for Chronostasis (The Stopped-Clock Illusion)
Generates:
1. Procedural SFX: mechanical ticks, saccade whooshes, freeze sub-drops, temporal rewinds.
2. Cinematic BGM: Clockwork pulse & orchestral drone score.
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

def synth_clock_tick():
    """Crisp mechanical clock escapement tick."""
    t = np.linspace(0, 0.08, int(SR * 0.08), False)
    impulse = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 120)
    body = np.sin(2 * np.pi * 850 * t) * np.exp(-t * 60) * 0.4
    tick = impulse + body
    write_wav("clock_tick.wav", tick, peak=0.8)

def synth_freeze_sub():
    """Deep temporal freeze sub-bass drop with high ringing bell."""
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    freq = np.geomspace(80, 28, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2.5)
    chime = np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 4.0) * 0.3
    sig = np.tanh(sub * 1.4) + chime
    write_wav("freeze_sub.wav", sig, peak=0.85)

def synth_saccade_whoosh():
    """Fast optical whip whoosh (eye saccade)."""
    t = np.linspace(0, 0.35, int(SR * 0.35), False)
    noise = np.random.normal(0, 1, len(t))
    sweep = np.sin(np.pi * t / 0.35) ** 2
    env = np.exp(-((t - 0.17) ** 2) / 0.008)
    sig = np.convolve(noise * env * sweep, np.ones(15) / 15, mode='same')
    write_wav("saccade_whoosh.wav", sig, peak=0.8)

def synth_blackout_zap():
    """Low-voltage shutter cut / blackout impulse."""
    t = np.linspace(0, 0.25, int(SR * 0.25), False)
    carrier = np.sin(2 * np.pi * 120 * t) * np.exp(-t * 15)
    noise = np.random.uniform(-0.3, 0.3, len(t)) * np.exp(-t * 25)
    sig = carrier + noise
    write_wav("blackout_zap.wav", sig, peak=0.7)

def synth_rewind_sweep():
    """Reverse time stitch sweep / tape rewind."""
    t = np.linspace(0, 1.2, int(SR * 1.2), False)
    # Pitch rises exponentially from 200Hz to 1600Hz
    freq = np.geomspace(200, 1600, len(t))
    env = np.exp((t - 1.2) * 3.0)  # swell
    sig = np.sin(2 * np.pi * freq * t) * env
    noise = np.random.normal(0, 0.15, len(t)) * env
    write_wav("rewind_sweep.wav", sig + noise, peak=0.75)

def synth_revelation_chime():
    """Grand harmonic golden chime for final payoff."""
    t = np.linspace(0, 2.5, int(SR * 2.5), False)
    freqs = [587.33, 880.0, 1174.66, 1760.0]  # D-major 9th harmonic
    weights = [0.8, 0.6, 0.4, 0.2]
    sig = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        sig += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 320.0))
    write_wav("revelation_chime.wav", sig, peak=0.85)

def synth_cinematic_bgm():
    """Evolving cinematic clockwork & ambient documentary score."""
    print("Synthesizing Chronostasis cinematic score...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Analog Sub & Deep Pad Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo = 1.0 + 0.10 * np.sin(2 * np.pi * 0.1 * t)
    drone = (
        0.50 * np.sin(2 * np.pi * 36.71 * t) +
        0.35 * np.sin(2 * np.pi * 55.00 * t + 0.5) +
        0.30 * np.sin(2 * np.pi * 73.42 * t) * lfo +
        0.20 * np.sin(2 * np.pi * 87.31 * t + 1.0)
    )
    
    # 2. Clockwork Pulse / Percussive Tick-Grid (120 BPM = 0.5s period)
    pulse_t = t % 0.5
    tick_sig = np.sin(2 * np.pi * 2400 * pulse_t) * np.exp(-pulse_t * 60)
    sub_click = np.sin(2 * np.pi * 65 * pulse_t) * np.exp(-pulse_t * 20)
    rhythm_track = (tick_sig * 0.15 + sub_click * 0.35)
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
            piano_track[idx_s:idx_e] += n_sig[:idx_e - idx_s] * 0.3
            
    # 4. Climax Swell (from 25s to end)
    swell_env = np.clip((t - 24.0) / 7.0, 0, 1.0)
    swell = (0.35 * np.sin(2 * np.pi * 220.0 * t) + 0.25 * np.sin(2 * np.pi * 440.0 * t)) * swell_env
    
    bgm = drone + (rhythm_track * rhythm_env) + (piano_track * 0.4) + (swell * 0.5)
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

def write_wav_path(path, data, peak=0.85):
    data = data / (np.max(np.abs(data)) + 1e-7) * peak
    wav_data = (data * 32767).astype(np.int16)
    wavfile.write(path, SR, wav_data)

def build_all_audio():
    print("=== Step 1: Synthesizing Procedural SFX & Score ===")
    synth_clock_tick()
    synth_freeze_sub()
    synth_saccade_whoosh()
    synth_blackout_zap()
    synth_rewind_sweep()
    synth_revelation_chime()
    synth_cinematic_bgm()
    
    print("\n=== Step 2: Multi-Track Mastering Mix ===")
    narration_path = os.path.join(TEMP_DIR, "narration_full.wav")
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    output_path = os.path.join(TEMP_DIR, "master_sound_design.wav")
    
    # SFX Event Placement locked to shot timing:
    sfx_events = [
        # Shot 01 (0.0s - 6.10s)
        ("clock_tick.wav", 0.50, -14),
        ("clock_tick.wav", 1.50, -14),
        ("clock_tick.wav", 2.50, -14),
        ("freeze_sub.wav", 3.80, -12),  # "second hand seems frozen"
        
        # Shot 02 (6.10s - 12.60s)
        ("saccade_whoosh.wav", 6.20, -16),
        ("blackout_zap.wav", 8.50, -15), # "goes blind for 100ms"
        
        # Shot 03 (12.60s - 19.90s)
        ("saccade_whoosh.wav", 12.80, -16),
        ("blackout_zap.wav", 15.20, -15),
        
        # Shot 04 (19.90s - 26.64s)
        ("rewind_sweep.wav", 20.20, -14), # "paints it backward in time"
        ("clock_tick.wav", 24.00, -14),
        
        # Shot 05 (26.64s - 33.78s)
        ("revelation_chime.wav", 26.80, -13), # "unbroken illusion"
        ("clock_tick.wav", 28.50, -14),
        ("clock_tick.wav", 29.50, -14),
        ("clock_tick.wav", 30.50, -14),
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
    
    print("Mixing Voiceover + Clockwork BGM + Procedural SFX into master audio...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Master soundtrack complete: {output_path}")
    else:
        print(f"Error mixing audio:\n{res.stderr}")

if __name__ == "__main__":
    build_all_audio()
