#!/usr/bin/env python3
"""
Narration and Audio Pipeline for The Zeigarnik Effect (The Unclosed Mental Tab)
Step 1: TTS Synthesis via pocket-tts with KMP_DUPLICATE_LIB_OK=TRUE
Step 2: ffprobe duration measurement
Step 3: Concatenation with padding & loudness mastering (-14 LUFS)
"""

import os
import subprocess
import json

# Ensure OpenMP runtime runs smoothly
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

VOICE_REF = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "reference_clean.wav"))
TEMP_DIR = os.path.join(os.path.dirname(__file__), ".temp_audio")
os.makedirs(TEMP_DIR, exist_ok=True)

SHOTS = [
    {
        "id": "shot_01",
        "name": "The Midnight Loop",
        "text": "You lie in bed trying to sleep, but your brain is obsessively replaying a single unfinished email from three P M."
    },
    {
        "id": "shot_02",
        "name": "The Asymmetry",
        "text": "You completely forgot the ten tasks you finished today, yet this one open loop refuses to let you rest."
    },
    {
        "id": "shot_03",
        "name": "The Berlin Waiter",
        "text": "In 1927, psychologist Bluma Zeigarnik noticed Berlin waiters remembered unpaid orders with flawless precision, but forgot them the instant the bill was settled."
    },
    {
        "id": "shot_04",
        "name": "The Open Mental Tab",
        "text": "Your brain treats an unfinished goal like an open mental tab, burning active working memory until the loop is resolved."
    },
    {
        "id": "shot_05",
        "name": "The Cognitive Closure",
        "text": "You do not have to finish the work to sleep. Simply writing down the next concrete step tricks your mind into closing the tab."
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
        subprocess.run(cmd_tts, check=True, env=dict(os.environ, KMP_DUPLICATE_LIB_OK="TRUE"))
        
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
    
    with open(os.path.join(os.path.dirname(__file__), "timings.json"), "w") as f:
        json.dump({
            "total_duration": round(total_dur, 2),
            "shots": shot_timings
        }, f, indent=2)
        
    return total_dur, shot_timings

if __name__ == "__main__":
    durations = generate_tts()
    master_narration(durations)
