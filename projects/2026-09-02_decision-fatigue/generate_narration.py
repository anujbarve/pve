#!/usr/bin/env python3
"""
Narration and Audio Pipeline for Decision Fatigue (Why Willpower Drains by 9 PM)
Step 1: TTS Synthesis via pocket-tts
Step 2: ffprobe duration measurement
Step 3: Concatenation with padding & loudness mastering (-14 LUFS)
"""

import os
import subprocess
import json

VOICE_REF = "/Users/anujbarve/Documents/gate-research/explainer-videos/reference_clean.wav"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(PROJECT_DIR, ".temp_audio")
os.makedirs(TEMP_DIR, exist_ok=True)

SHOTS = [
    {
        "id": "shot_01",
        "name": "The Nighttime Paralysis",
        "text": "You make disciplined, high-stakes decisions all day at work—yet at nine PM, you stand paralyzed before an open refrigerator."
    },
    {
        "id": "shot_02",
        "name": "The Neural Fuel Tank",
        "text": "Willpower isn't moral strength. Every single choice, from drafting an email to picking a route, consumes the exact same finite pool of prefrontal glucose."
    },
    {
        "id": "shot_03",
        "name": "The Cognitive Downshift",
        "text": "When that biological fuel runs dry, your brain aggressively downshifts into survival mode—abandoning complex trade-offs and defaulting to pure impulse."
    },
    {
        "id": "shot_04",
        "name": "The Default Trap",
        "text": "In landmark court studies, judges granted parole sixty-five percent of the time at dawn, but plummeted to zero before lunch—simply because saying no requires less mental energy."
    },
    {
        "id": "shot_05",
        "name": "The Shield of Routine",
        "text": "The most disciplined minds don’t possess infinite willpower—they ruthlessly eliminate trivial decisions before the day even begins."
    }
]

def get_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def generate_tts():
    print("=== Step 1: Synthesizing TTS Voiceover per Shot ===")
    shot_durations = []
    
    env = os.environ.copy()
    env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    
    for shot in SHOTS:
        raw_path = os.path.join(TEMP_DIR, f"{shot['id']}_raw.wav")
        padded_path = os.path.join(TEMP_DIR, f"{shot['id']}.wav")
        
        print(f"Generating TTS for {shot['id']} ({shot['name']})...")
        cmd_tts = [
            "pocket-tts", "generate",
            "--voice", VOICE_REF,
            "--text", shot["text"],
            "--output-path", raw_path
        ]
        res = subprocess.run(cmd_tts, env=env, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error generating TTS for {shot['id']}: {res.stderr}")
            raise RuntimeError(res.stderr)
        
        # Add 0.3s pre-roll and 0.4s tail pad
        cmd_pad = [
            "ffmpeg", "-y", "-i", raw_path,
            "-af", "adelay=300|300,apad=pad_dur=0.4",
            "-ar", "24000", "-ac", "1",
            padded_path
        ]
        subprocess.run(cmd_pad, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        dur = get_duration(padded_path)
        shot_durations.append({
            "id": shot["id"],
            "name": shot["name"],
            "text": shot["text"],
            "file": padded_path,
            "duration": round(dur, 2)
        })
        print(f"  -> {shot['id']}: {dur:.2f}s")
        
    return shot_durations

def master_narration(shot_durations):
    print("\n=== Step 2: Mastering Voiceover Audio (-14 LUFS) ===")
    inputs = []
    filter_chains = []
    current_time = 0.0
    shot_timings = []
    
    for idx, s in enumerate(shot_durations):
        inputs.extend(["-i", s["file"]])
        delay_ms = int(current_time * 1000)
        filter_chains.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms}[a{idx}]")
        shot_timings.append({
            "id": s["id"],
            "name": s["name"],
            "start": round(current_time, 2),
            "duration": s["duration"]
        })
        current_time += s["duration"]
        
    num_inputs = len(shot_durations)
    mix_sources = "".join([f"[a{i}]" for i in range(num_inputs)])
    filter_complex = f"{';'.join(filter_chains)};{mix_sources}amix=inputs={num_inputs}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[out]"
    
    full_output = os.path.join(TEMP_DIR, "narration_full.wav")
    cmd_master = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", "24000", "-ac", "1",
        full_output
    ]
    subprocess.run(cmd_master, check=True)
    total_dur = get_duration(full_output)
    print(f"Master voiceover created: {full_output} (Total Duration: {total_dur:.2f}s)")
    
    with open(os.path.join(PROJECT_DIR, "timings.json"), "w") as f:
        json.dump({
            "total_duration": round(total_dur, 2),
            "shots": shot_timings
        }, f, indent=2)
        
    return total_dur, shot_timings

if __name__ == "__main__":
    durations = generate_tts()
    master_narration(durations)
