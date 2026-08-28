#!/usr/bin/env python3
"""
Sound Design & BGM Engine for The Extended Mind Thesis
Generates:
1. Procedural SFX library (sub impacts, whooshes, glitches, chimes, snaps, synapse pulses).
2. Cinematic BGM Score: Ambient analog drone + cybernetic pulse + glass ostinato.
3. 3-Layer Master Mix (-14 LUFS) with exact millisecond synchronization.
"""

import os
import json
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess

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

def synth_sub_impact():
    """Deep 90Hz -> 32Hz exponential pitch drop with harmonic warmth."""
    t = np.linspace(0, 1.8, int(SR * 1.8), False)
    freq = np.geomspace(90, 32, len(t))
    env = np.exp(-t * 3.0)
    sig = np.tanh(np.sin(2 * np.pi * freq * t) * env * 1.6)
    write_wav("sub_impact.wav", sig, peak=0.85)

def synth_whoosh():
    """Bandpass-filtered spatial motion sweep."""
    t = np.linspace(0, 0.7, int(SR * 0.7), False)
    noise = np.random.normal(0, 1, len(t))
    sweep = np.sin(np.pi * t / 0.7) ** 2
    env = np.exp(-((t - 0.35) ** 2) / 0.03)
    sig = np.convolve(noise * env * sweep, np.ones(25) / 25, mode='same')
    write_wav("whoosh.wav", sig, peak=0.8)

def synth_glitch():
    """High-frequency FM chirp with gated noise for mismatch panic."""
    t = np.linspace(0, 0.45, int(SR * 0.45), False)
    mod = np.sin(2 * np.pi * 70 * t)
    carrier = np.sin(2 * np.pi * (520 + 900 * mod) * t)
    gate = (np.sin(2 * np.pi * 40 * t) > 0).astype(float)
    noise = np.random.uniform(-0.4, 0.4, len(t)) * 0.3
    sig = (carrier * gate + noise) * np.exp(-t * 5.5)
    write_wav("glitch.wav", sig, peak=0.75)

def synth_chime():
    """Multi-harmonic modal chime for golden conceptual highlights."""
    t = np.linspace(0, 2.2, int(SR * 2.2), False)
    freqs = [880.0, 1320.0, 1760.0, 2640.0, 3520.0]
    weights = [1.0, 0.65, 0.45, 0.25, 0.15]
    sig = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        sig += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 350.0))
    write_wav("chime.wav", sig, peak=0.85)

def synth_snap():
    """High-frequency tactile mechanical snap (4.2kHz)."""
    t = np.linspace(0, 0.15, int(SR * 0.15), False)
    freq = np.geomspace(4200, 450, len(t))
    env = np.exp(-t * 48)
    sig = np.sin(2 * np.pi * freq * t) * env
    write_wav("snap.wav", sig, peak=0.75)

def synth_pulse_ping():
    """Resonant neural ping with octave harmonic."""
    t = np.linspace(0, 0.65, int(SR * 0.65), False)
    freq = 660.0
    env = np.exp(-t * 7.5)
    sig = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2 * t)) * env
    write_wav("pulse_ping.wav", sig, peak=0.75)

def synth_amputation_zap():
    """Electrical disconnect fizzle / severed filament discharge."""
    t = np.linspace(0, 0.5, int(SR * 0.5), False)
    carrier = np.sin(2 * np.pi * np.geomspace(800, 120, len(t)) * t)
    noise = np.random.uniform(-0.5, 0.5, len(t))
    env = np.exp(-t * 8.0)
    sig = (carrier * 0.6 + noise * 0.4) * env
    write_wav("amputation_zap.wav", sig, peak=0.75)

def synth_bio_synapse():
    """Warm biological synapse resonance pulse."""
    t = np.linspace(0, 1.4, int(SR * 1.4), False)
    f1, f2, f3 = 220.0, 330.0, 440.0
    sig = (
        0.5 * np.sin(2 * np.pi * f1 * t) +
        0.3 * np.sin(2 * np.pi * f2 * t) +
        0.2 * np.sin(2 * np.pi * f3 * t)
    ) * np.exp(-t * 2.8)
    write_wav("bio_synapse.wav", sig, peak=0.8)

def synth_cinematic_bgm():
    """Evolving cinematic ambient drone and cybernetic score."""
    print("Synthesizing Extended Mind cinematic score...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Analog Sub & Deep Pad Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo1 = 1.0 + 0.12 * np.sin(2 * np.pi * 0.08 * t)
    lfo2 = 1.0 + 0.08 * np.sin(2 * np.pi * 0.14 * t + 1.1)
    
    drone = (
        0.48 * np.sin(2 * np.pi * 36.71 * t) +
        0.32 * np.sin(2 * np.pi * 55.00 * t + 0.4) * lfo1 +
        0.28 * np.sin(2 * np.pi * 73.42 * t) +
        0.18 * np.sin(2 * np.pi * 87.31 * t + 0.9) * lfo2
    )
    
    # 2. Cybernetic Pulse (120 BPM = 0.5s period) - Enters at 8.0s
    pulse_t = t % 0.5
    sub_click = np.sin(2 * np.pi * 68 * pulse_t) * np.exp(-pulse_t * 22)
    hi_tick = np.sin(2 * np.pi * 2600 * pulse_t) * np.exp(-pulse_t * 70) * 0.15
    pulse_track = sub_click + hi_tick
    pulse_env = np.clip((t - 7.5) / 5.0, 0, 1.0)
    
    # 3. Ethereal Glass / Ambient Piano Arpeggios (Dm9 chord: D4=293.66, F4=349.23, A4=440.0, C5=523.25, E5=659.25)
    arp_notes = [293.66, 440.0, 523.25, 659.25, 440.0, 349.23]
    note_dur = 0.5
    arp_track = np.zeros_like(t)
    for i, start_time in enumerate(np.arange(0, TOTAL_DURATION, note_dur)):
        if start_time < TOTAL_DURATION:
            freq = arp_notes[i % len(arp_notes)]
            t_n = np.linspace(0, 1.4, int(SR * 1.4), False)
            n_sig = (
                0.65 * np.sin(2 * np.pi * freq * t_n) +
                0.25 * np.sin(2 * np.pi * freq * 2 * t_n) +
                0.10 * np.sin(2 * np.pi * freq * 3 * t_n)
            ) * np.exp(-t_n * 2.9)
            idx_s = int(start_time * SR)
            idx_e = min(len(t), idx_s + len(t_n))
            arp_track[idx_s:idx_e] += n_sig[:idx_e - idx_s] * 0.35
            
    # 4. Cinematic Climax Swell (32s to 40s)
    swell_env = np.clip((t - 31.0) / 7.0, 0, 1.0)
    swell = (
        0.35 * np.sin(2 * np.pi * 220.0 * t) +
        0.25 * np.sin(2 * np.pi * 329.63 * t) +
        0.20 * np.sin(2 * np.pi * 440.0 * t)
    ) * swell_env
    
    bgm = drone + (pulse_track * pulse_env * 0.35) + (arp_track * 0.4) + (swell * 0.5)
    bgm = np.tanh(bgm * 1.2)
    
    # Global Fade In (1.5s) and Fade Out (2.5s)
    fade_in = np.linspace(0, 1, int(SR * 1.5))
    fade_out = np.linspace(1, 0, int(SR * 2.5))
    bgm[:len(fade_in)] *= fade_in
    bgm[-len(fade_out):] *= fade_out
    
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    data = bgm / (np.max(np.abs(bgm)) + 1e-7) * 0.9
    wav_data = (data * 32767).astype(np.int16)
    wavfile.write(bgm_path, SR, wav_data)
    print(f"BGM score rendered: {bgm_path}")
    return bgm_path

def build_sound_design():
    print("=== Step 1: Synthesizing Procedural SFX & Score ===")
    synth_sub_impact()
    synth_whoosh()
    synth_glitch()
    synth_chime()
    synth_snap()
    synth_pulse_ping()
    synth_amputation_zap()
    synth_bio_synapse()
    synth_cinematic_bgm()
    
    print("\n=== Step 2: 3-Layer Master Audio Mix ===")
    narration_path = os.path.join(TEMP_DIR, "narration_full.wav")
    bgm_path = os.path.join(TEMP_DIR, "cinematic_bgm.wav")
    output_path = os.path.join(TEMP_DIR, "master_sound_design.wav")
    
    # SFX Event Placement locked to shot timing:
    sfx_events = [
        # Shot 01 (0.0s - 8.10s): The Phantom Pocket
        ("whoosh.wav", 0.40, -18),
        ("glitch.wav", 3.60, -15),
        ("sub_impact.wav", 4.30, -14),
        
        # Shot 02 (8.10s - 16.36s): The Cognitive Amputation
        ("whoosh.wav", 8.20, -18),
        ("amputation_zap.wav", 10.60, -15),
        ("snap.wav", 12.80, -16),
        
        # Shot 03 (16.36s - 25.90s): The Extended Mind Thesis
        ("chime.wav", 16.50, -15),
        ("pulse_ping.wav", 19.80, -20),
        ("pulse_ping.wav", 21.20, -20),
        ("bio_synapse.wav", 22.80, -16),
        
        # Shot 04 (25.90s - 34.16s): The Silicon Loop
        ("whoosh.wav", 26.00, -18),
        ("pulse_ping.wav", 28.00, -19),
        ("snap.wav", 30.20, -16),
        
        # Shot 05 (34.16s - 42.26s): The Handheld Cyborg
        ("sub_impact.wav", 34.30, -14),
        ("chime.wav", 37.50, -14),
        ("bio_synapse.wav", 39.50, -15),
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
        raise RuntimeError("FFmpeg master audio mix failed")

if __name__ == "__main__":
    build_sound_design()
