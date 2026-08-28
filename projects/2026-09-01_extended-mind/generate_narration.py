#!/usr/bin/env python3
"""
Narration and Audio Pipeline for The Extended Mind Thesis
Step 1: TTS Synthesis via pocket-tts
Step 2: ffprobe duration measurement
Step 3: Concatenation with padding & loudness mastering (-14 LUFS)
"""

import os
import subprocess
import json

VOICE_REF = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "reference_clean.wav"))
TEMP_DIR = os.path.join(os.path.dirname(__file__), ".temp_audio")
os.makedirs(TEMP_DIR, exist_ok=True)

SHOTS = [
    {
        "id": "shot-01-panic",
        "name": "The Phantom Pocket",
        "text": "You reach into your pocket, and it is empty. For ten seconds, a spike of physical panic grips your chest."
    },
    {
        "id": "shot-02-amputation",
        "name": "The Cognitive Amputation",
        "text": "You don't just feel like you lost a gadget. You feel as though thirty percent of your memory and navigation was instantly amputated."
    },
    {
        "id": "shot-03-extended-mind",
        "name": "The Extended Mind Thesis",
        "text": "This is the Extended Mind Thesis. When an external tool reliably stores and recalls data, it functions as literal biology."
    },
    {
        "id": "shot-04-neural-loop",
        "name": "The Silicon Loop",
        "text": "Your biological neurons and silicon circuits operate in a continuous loop, thinking together across the boundary of your skin."
    },
    {
        "id": "shot-05-cyborg-reality",
        "name": "The Handheld Cyborg",
        "text": "You didn't need neural implants to become a cyborg. You became one the moment you offloaded your mind into your hand."
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
        subprocess.run(cmd_tts, check=True, env=env)
        
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
            "text": s["text"],
            "start": round(current_time, 2),
            "duration": s["duration"]
        })
        current_time = round(current_time + s["duration"], 2)
        
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
    
    timings_data = {
        "total_duration": round(total_dur, 2),
        "shots": shot_timings
    }
    
    with open(os.path.join(os.path.dirname(__file__), "timings.json"), "w") as f:
        json.dump(timings_data, f, indent=2)
        
    return total_dur, shot_timings

if __name__ == "__main__":
    durations = generate_tts()
    master_narration(durations)
