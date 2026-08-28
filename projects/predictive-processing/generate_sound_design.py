#!/usr/bin/env python3
import os
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess
from generate_cinematic_bgm import synth_cinematic_bgm

SR = 44100
SFX_DIR = os.path.join(os.path.dirname(__file__), ".sfx_library")
os.makedirs(SFX_DIR, exist_ok=True)

def write_wav(filename, data):
    data = data / (np.max(np.abs(data)) + 1e-7) * 0.75
    wav_data = (data * 32767).astype(np.int16)
    wavfile.write(os.path.join(SFX_DIR, filename), SR, wav_data)

def synth_sub_impact():
    t = np.linspace(0, 1.5, int(SR * 1.5), False)
    freq = np.geomspace(90, 32, len(t))
    env = np.exp(-t * 3.5)
    sig = np.tanh(np.sin(2 * np.pi * freq * t) * env * 1.5)
    write_wav("sub_impact.wav", sig)

def synth_whoosh():
    t = np.linspace(0, 0.8, int(SR * 0.8), False)
    noise = np.random.normal(0, 1, len(t))
    sweep = np.sin(np.pi * t / 0.8) ** 2
    env = np.exp(-((t - 0.4) ** 2) / 0.04)
    sig = np.convolve(noise * env * sweep, np.ones(30) / 30, mode='same')
    write_wav("whoosh.wav", sig)

def synth_glitch():
    t = np.linspace(0, 0.4, int(SR * 0.4), False)
    mod = np.sin(2 * np.pi * 60 * t)
    carrier = np.sin(2 * np.pi * (440 + 800 * mod) * t)
    gate = (np.sin(2 * np.pi * 35 * t) > 0).astype(float)
    noise = np.random.uniform(-0.5, 0.5, len(t)) * 0.3
    sig = (carrier * gate + noise) * np.exp(-t * 6)
    write_wav("glitch.wav", sig)

def synth_chime():
    t = np.linspace(0, 2.0, int(SR * 2.0), False)
    freqs = [880, 1320, 1760, 2640, 3520]
    weights = [1.0, 0.6, 0.4, 0.25, 0.15]
    sig = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        sig += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 350.0))
    write_wav("chime.wav", sig)

def synth_snap_click():
    t = np.linspace(0, 0.15, int(SR * 0.15), False)
    freq = np.geomspace(4200, 400, len(t))
    env = np.exp(-t * 45)
    sig = np.sin(2 * np.pi * freq * t) * env
    write_wav("snap.wav", sig)

def synth_pulse_ping():
    t = np.linspace(0, 0.6, int(SR * 0.6), False)
    freq = 660
    env = np.exp(-t * 8)
    sig = (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)) * env
    write_wav("pulse_ping.wav", sig)

def build_sfx_library():
    print("Synthesizing procedural SFX library...")
    synth_sub_impact()
    synth_whoosh()
    synth_glitch()
    synth_chime()
    synth_snap_click()
    synth_pulse_ping()
    synth_cinematic_bgm()
    print("SFX & BGM library ready.")

def mix_master_sound_design():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    narration_path = os.path.join(project_dir, ".temp_audio", "narration_full.wav")
    bgm_path = os.path.join(project_dir, ".temp_audio", "cinematic_bgm.wav")
    output_path = os.path.join(project_dir, ".temp_audio", "master_sound_design.wav")
    
    # SFX events: (filename, start_time_seconds, volume_gain_db)
    sfx_events = [
        # Shot 01: The Blind Reach
        ("whoosh.wav", 0.40, -18),
        ("chime.wav", 4.00, -16),
        ("glitch.wav", 7.40, -15),
        
        # Shot 02: The Spatial Fracture
        ("sub_impact.wav", 10.90, -14),
        ("snap.wav", 12.20, -16),
        
        # Shot 03: The Projection Engine
        ("whoosh.wav", 19.56, -18),
        ("pulse_ping.wav", 20.40, -20),
        ("pulse_ping.wav", 21.50, -20),
        ("pulse_ping.wav", 22.60, -20),
        
        # Shot 04: The Typo Glitch
        ("snap.wav", 29.50, -18),
        ("chime.wav", 33.80, -15),
        
        # Shot 05: The Calibration & Manifesto
        ("sub_impact.wav", 38.56, -14),
        ("chime.wav", 43.10, -14),
    ]
    
    # Inputs:
    # 0: Narration
    # 1: BGM
    # 2..N: SFX files
    inputs = ["-i", narration_path, "-i", bgm_path]
    filter_parts = []
    
    # Voiceover input (clean and present)
    filter_parts.append("[0:a]volume=1.0[voice]")
    
    # BGM input at -22dB
    bgm_gain = 10 ** (-22.0 / 20.0)
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
    
    # Master mix with normalize=0 and loudnorm mastering
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
    
    print("Mixing Voiceover + Cinematic BGM Score + Procedural SFX...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Master soundtrack created: {output_path}")
    else:
        print(f"Error mixing audio:\n{res.stderr}")

if __name__ == "__main__":
    build_sfx_library()
    mix_master_sound_design()
