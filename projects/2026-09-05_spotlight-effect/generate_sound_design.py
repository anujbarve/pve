#!/usr/bin/env python3
"""
Sound Design & BGM Engine for The Spotlight Effect (Nobody is Looking at You)
Generates:
1. Procedural SFX: cafe ambiance, spotlight hum, sub-drops, ocular laser locks, study stamps, 180-deg reverse sweeps, power-downs, and golden liberation chimes.
2. Cinematic BGM: Multi-act minimalist documentary score with D-minor pad, anxious heartbeat pulse, glass ostinato, and golden D-major crescendo.
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
    
    # 1. Cafe Ambient Room Tone & Sub Acoustic Bed
    t = np.linspace(0, 3.5, int(SR * 3.5), False)
    room = 0.4 * np.sin(2 * np.pi * 50.0 * t) + 0.2 * np.sin(2 * np.pi * 100.0 * t)
    noise = np.random.normal(0, 0.08, len(t))
    env = np.exp(-t * 0.4)
    write_wav("cafe_ambient.wav", (room + noise) * env, peak=0.75)
    
    # 2. 10,000-Watt Spotlight Electric Buzz & High Filament Whine
    t = np.linspace(0, 3.0, int(SR * 3.0), False)
    buzz = 0.5 * np.sin(2 * np.pi * 60.0 * t) + 0.3 * np.sin(2 * np.pi * 120.0 * t) + 0.2 * np.sin(2 * np.pi * 180.0 * t)
    whine = 0.15 * np.sin(2 * np.pi * 3200.0 * t) * (1.0 + 0.2 * np.sin(2 * np.pi * 8.0 * t))
    env = np.exp(-t * 0.7)
    write_wav("spotlight_hum.wav", (buzz + whine) * env, peak=0.80)
    
    # 3. Heavy Sub-Bass Impact (Spotlight slam / visceral chest heat)
    t = np.linspace(0, 2.5, int(SR * 2.5), False)
    freq = np.geomspace(110, 28, len(t))
    sub = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2.0)
    punch = np.sin(2 * np.pi * 75 * t[:int(SR*0.06)]) * np.exp(-t[:int(SR*0.06)] * 80)
    full_punch = np.zeros_like(t)
    full_punch[:len(punch)] = punch * 0.8
    write_wav("sub_impact.wav", np.tanh(sub * 1.5) + full_punch, peak=0.90)
    
    # 4. Gaze Laser Lock / Ocular Reticle Zap
    t = np.linspace(0, 0.25, int(SR * 0.25), False)
    freq = np.geomspace(2400, 450, len(t))
    sweep = np.sin(2 * np.pi * freq * t) * np.exp(-t * 22)
    fm = np.sin(2 * np.pi * (1800 + 400 * np.sin(2 * np.pi * 60 * t)) * t) * np.exp(-t * 30) * 0.5
    write_wav("laser_lock.wav", sweep + fm, peak=0.80)
    
    # 5. Heartbeat Anxiety Spike (Cardiovascular pulse)
    t = np.linspace(0, 1.2, int(SR * 1.2), False)
    thump1 = np.sin(2 * np.pi * 48 * t) * np.exp(-t * 14)
    thump2 = np.zeros_like(t)
    offset = int(SR * 0.22)
    t2 = t[:-offset]
    thump2[offset:] = (np.sin(2 * np.pi * 52 * t2) * np.exp(-t2 * 16)) * 0.8
    write_wav("heartbeat_spike.wav", np.tanh((thump1 + thump2) * 1.3), peak=0.85)
    
    # 6. Experimental Stamp / Data Lock (Cornell Study)
    t = np.linspace(0, 1.5, int(SR * 1.5), False)
    crack = np.sin(2 * np.pi * 1400 * t) * np.exp(-t * 70) * 0.7
    thud = np.sin(2 * np.pi * 90 * t) * np.exp(-t * 15)
    sub = np.sin(2 * np.pi * 42 * t) * np.exp(-t * 4.0) * 0.6
    write_wav("study_stamp.wav", crack + thud + sub, peak=0.85)
    
    # 7. Stat Plummet / Shrink Resonant Whoosh (50% -> 23%)
    t = np.linspace(0, 1.4, int(SR * 1.4), False)
    noise = np.random.normal(0, 1, len(t))
    sweep_freq = np.geomspace(2800, 150, len(t))
    sig = noise * np.sin(2 * np.pi * sweep_freq * t)
    env = np.sin(np.pi * (t / 1.4) ** 0.75)
    write_wav("stat_shrink_whoosh.wav", sig * env, peak=0.75)
    
    # 8. 180-Degree Gaze Vector Reverse Sweep (Spatial Doppler shift)
    t = np.linspace(0, 1.8, int(SR * 1.8), False)
    freq = np.geomspace(1200, 220, len(t))
    sweep = np.sin(2 * np.pi * freq * t) * np.sin(np.pi * (t / 1.8))
    phase_whir = np.sin(2 * np.pi * 380 * t + np.sin(2 * np.pi * 4 * t) * 3) * np.exp(-t * 1.8) * 0.4
    write_wav("reverse_sweep.wav", sweep + phase_whir, peak=0.80)
    
    # 9. Anxiety Bubble Ambient Shimmer (Personal inward sphere)
    t = np.linspace(0, 2.5, int(SR * 2.5), False)
    freqs = [440.0, 554.37, 659.25, 830.61]
    weights = [0.6, 0.4, 0.3, 0.2]
    shimmer = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        shimmer += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 300.0))
    write_wav("bubble_pop_ambient.wav", shimmer, peak=0.80)
    
    # 10. Studio Spotlight Heavy Power-Down Switch (Theatrical Blackout)
    t = np.linspace(0, 2.2, int(SR * 2.2), False)
    lever_click = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 120) * 0.8
    body = np.sin(2 * np.pi * 220 * t) * np.exp(-t * 35) * 0.6
    powerdown = np.sin(2 * np.pi * np.geomspace(600, 40, len(t)) * t) * np.exp(-t * 1.6) * 0.7
    write_wav("power_down.wav", lever_click + body + powerdown, peak=0.85)
    
    # 11. Golden Liberation Chime (D-Major 9th crystalline clarity)
    t = np.linspace(0, 3.5, int(SR * 3.5), False)
    freqs = [587.33, 739.99, 880.00, 1108.73, 1479.98, 2217.46] # D-Major 9th
    weights = [0.7, 0.55, 0.45, 0.35, 0.25, 0.15]
    chime = np.zeros_like(t)
    for f, w in zip(freqs, weights):
        chime += w * np.sin(2 * np.pi * f * t) * np.exp(-t * (f / 450.0))
    write_wav("golden_liberation_chime.wav", chime, peak=0.85)

def synth_cinematic_bgm():
    print("Synthesizing custom cinematic score for The Spotlight Effect...")
    t = np.linspace(0, TOTAL_DURATION, int(SR * TOTAL_DURATION), False)
    
    # 1. Analog Sub & Deep Cinematic Drone (D-minor: D1=36.71Hz, A1=55Hz, D2=73.42Hz, F2=87.31Hz)
    lfo = 1.0 + 0.12 * np.sin(2 * np.pi * 0.08 * t)
    drone = (
        0.45 * np.sin(2 * np.pi * 36.71 * t) +
        0.30 * np.sin(2 * np.pi * 55.00 * t + 0.4) +
        0.25 * np.sin(2 * np.pi * 73.42 * t) * lfo +
        0.18 * np.sin(2 * np.pi * 87.31 * t + 0.8)
    )
    
    # 2. Subtle Heartbeat / Anxiety Pulse (110 BPM = 0.545s period)
    pulse_period = 0.545
    pulse_t = t % pulse_period
    heart_sub = np.sin(2 * np.pi * 54 * pulse_t) * np.exp(-pulse_t * 18)
    heart_click = np.sin(2 * np.pi * 105 * pulse_t) * np.exp(-pulse_t * 38) * 0.35
    heartbeat = heart_sub + heart_click
    
    # Fade heartbeat in at 9.0s, keep rolling through Act 4
    heart_env = np.clip((t - 9.0) / 3.0, 0, 1.0) * np.clip((38.0 - t) / 2.5, 0, 1.0)
    
    # 3. Minimalist Glass / Celesta Ostinato (D4=293.66, F4=349.23, A4=440.00, C5=523.25, E5=659.25)
    ostinato_notes = [293.66, 440.0, 349.23, 523.25, 659.25, 440.0, 349.23, 293.66]
    note_dur = 0.545
    glass_track = np.zeros_like(t)
    for i, start_time in enumerate(np.arange(0, TOTAL_DURATION, note_dur)):
        if start_time < TOTAL_DURATION:
            freq = ostinato_notes[i % len(ostinato_notes)]
            t_n = np.linspace(0, 1.0, int(SR * 1.0), False)
            n_sig = (0.75 * np.sin(2 * np.pi * freq * t_n) + 0.25 * np.sin(2 * np.pi * freq * 2 * t_n)) * np.exp(-t_n * 2.8)
            idx_s = int(start_time * SR)
            idx_e = min(len(t), idx_s + len(t_n))
            glass_track[idx_s:idx_e] += n_sig[:idx_e - idx_s] * 0.32
            
    # Glass track enters smoothly at 16.0s
    glass_env = np.clip((t - 16.0) / 3.5, 0, 1.0)
    
    # 4. Cinematic Tension Strings & Swell (Act 4 -> Act 5, 27s to end)
    swell_env = np.clip((t - 27.0) / 8.0, 0, 1.0)
    strings = (
        0.28 * np.sin(2 * np.pi * 220.0 * t) +
        0.22 * np.sin(2 * np.pi * 329.63 * t + 0.3) +
        0.18 * np.sin(2 * np.pi * 440.0 * t + 0.6)
    ) * swell_env
    
    # 5. Golden Climax Harmonic Bed (Act 5 payoff, 37s to end, D-Major resolution!)
    climax_env = np.clip((t - 37.5) / 2.5, 0, 1.0)
    climax_bed = (
        0.40 * np.sin(2 * np.pi * 146.83 * t) + # D3
        0.32 * np.sin(2 * np.pi * 220.00 * t) + # A3
        0.28 * np.sin(2 * np.pi * 293.66 * t) + # D4
        0.24 * np.sin(2 * np.pi * 370.00 * t)   # F#4 (Major resolution!)
    ) * climax_env
    
    bgm = drone + (heartbeat * heart_env * 0.30) + (glass_track * glass_env * 0.38) + strings + climax_bed
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
    # Shot 1: 0.00s - 9.62s ("The 10,000-Watt Stain")
    # Shot 2: 9.62s - 17.64s ("The Hallucinated Audience")
    # Shot 3: 17.64s - 28.70s ("The Barry Manilow Test")
    # Shot 4: 28.70s - 37.84s ("The Inward Vectors")
    # Shot 5: 37.84s - 46.42s ("The Blackout of Judgment")
    sfx_events = [
        # Shot 1: The 10,000-Watt Stain
        ("cafe_ambient.wav", 0.10, -18),
        ("spotlight_hum.wav", 4.20, -16),         # "feeling a blinding ten-thousand-watt spotlight"
        ("sub_impact.wav", 5.60, -14),            # "burning directly into your chest"
        
        # Shot 2: The Hallucinated Audience
        ("laser_lock.wav", 10.40, -15),           # "every pair of eyes in the room"
        ("heartbeat_spike.wav", 12.60, -16),
        ("laser_lock.wav", 14.20, -16),           # "silently dissecting your embarrassment"
        
        # Shot 3: The Barry Manilow Test
        ("study_stamp.wav", 18.20, -14),          # "In landmark Cornell experiments"
        ("stat_shrink_whoosh.wav", 23.40, -15),   # "predicted fifty percent... yet barely twenty-three percent"
        ("sub_impact.wav", 25.20, -15),
        
        # Shot 4: The Inward Vectors
        ("reverse_sweep.wav", 29.20, -15),        # "The truth is nobody is watching you"
        ("bubble_pop_ambient.wav", 32.50, -16),   # "trapped in their own private anxiety bubble"
        ("reverse_sweep.wav", 35.00, -17),
        
        # Shot 5: The Blackout of Judgment
        ("power_down.wav", 38.40, -14),           # "When you realize the spotlight is only an internal projection"
        ("golden_liberation_chime.wav", 41.50, -14) # "the audience was never there"
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
