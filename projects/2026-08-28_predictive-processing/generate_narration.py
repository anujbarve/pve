#!/usr/bin/env python3
import subprocess
import os
import sys

RENDER_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE = os.path.join(os.path.dirname(RENDER_DIR), "..", "..", "reference_clean.wav")
OUTPUT_DIR = os.path.join(RENDER_DIR, ".temp_audio")

SHOTS = [
    {
        "id": "shot-01-reach",
        "text": "Reach for your cup without looking. Your fingers close on empty air. For a split second, your world glitches.",
    },
    {
        "id": "shot-02-fracture",
        "text": "The cup was moved two inches to the left. But your brain didn't wait for your eyes. It rendered a phantom object.",
    },
    {
        "id": "shot-03-projection",
        "text": "We think our senses feed us reality. But your brain isn't a camera. It is a prediction engine projecting a simulation outward.",
    },
    {
        "id": "shot-04-typo",
        "text": "This is why you miss typos in your own writing. If your expectation is strong enough, your brain literally paints over the mistake.",
    },
    {
        "id": "shot-05-calibration",
        "text": "You never experience the world as it is. You experience your brain's prediction of the world, calibrated by the surprises.",
    },
]

def run(cmd, **kwargs):
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    return result

def get_duration(path):
    dur_result = run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", path
    ])
    return float(dur_result.stdout.strip())

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    current_start = 0.0
    for shot in SHOTS:
        raw_path = os.path.join(OUTPUT_DIR, f"{shot['id']}_raw.wav")
        synced_path = os.path.join(OUTPUT_DIR, f"{shot['id']}.wav")
        
        cmd = [
            "pocket-tts", "generate",
            "--voice", REFERENCE,
            "--text", shot["text"],
            "--output-path", raw_path,
            "--temperature", "0.1",
        ]
        env = os.environ.copy()
        env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        run(cmd, env=env)
        
        tts_dur = get_duration(raw_path)
        shot_dur = round(0.3 + tts_dur + 0.4, 2)
        
        shot["start"] = current_start
        shot["duration"] = shot_dur
        current_start = round(current_start + shot_dur, 2)
        
        run([
            "ffmpeg", "-y", "-i", raw_path,
            "-af", "adelay=300|300,apad=pad_dur=0.4",
            "-t", str(shot_dur),
            "-ar", "24000", "-ac", "1",
            synced_path
        ])
        print(f"{shot['id']}: start={shot['start']:.2f}, dur={shot['duration']:.2f}, text={shot['text'][:35]}...")

    TOTAL_DURATION = current_start
    print(f"\nTotal Film Duration: {TOTAL_DURATION:.2f}s")
    
    with open('timings.txt', 'w') as f:
        f.write(f"{TOTAL_DURATION}\n")
        for st in SHOTS:
            f.write(f"{st['id']},{st['start']},{st['duration']}\n")

    inputs = []
    filter_parts = []
    for i, shot in enumerate(SHOTS):
        clip_path = os.path.join(OUTPUT_DIR, f"{shot['id']}.wav")
        inputs.extend(["-i", clip_path])
        delay_ms = int(shot["start"] * 1000)
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[d{i}]")

    mix_inputs = "".join(f"[d{i}]" for i in range(len(SHOTS)))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={len(SHOTS)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[out]"
    )

    narration_path = os.path.join(OUTPUT_DIR, "narration_full.wav")
    run([
        "ffmpeg", "-y", *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[out]",
        "-t", str(TOTAL_DURATION),
        "-ar", "24000", "-ac", "1",
        narration_path
    ])
    print(f"Master narration audio created: {narration_path}")

if __name__ == "__main__":
    main()
