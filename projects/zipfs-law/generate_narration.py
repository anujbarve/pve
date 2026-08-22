#!/usr/bin/env python3
"""Generate synced 60s narration audio for Zipf's Law (1080p Vertical Explainer).

Golden Rule: Script -> Audio -> Visuals.
Measures exact TTS durations, applies reveal offsets, and builds master audio track.
"""

import subprocess
import os
import sys

RENDER_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATE_REFS = [
    os.path.abspath(os.path.join(RENDER_DIR, "..", "..", "reference_clean.wav")),
    os.path.abspath(os.path.join(RENDER_DIR, "..", "..", "..", "reference_clean.wav")),
    "/Users/anujbarve/Documents/gate-research/reference_clean.wav",
]
REFERENCE = next((p for p in CANDIDATE_REFS if os.path.exists(p)), CANDIDATE_REFS[-1])
OUTPUT_DIR = os.path.join(RENDER_DIR, ".temp_audio")

FRAMES = [
    {
        "id": "01-hook",
        "text": "The most common word in English is the. It accounts for seven percent of everything spoken. Why does this rule govern language?",
    },
    {
        "id": "02-origin",
        "text": "In nineteen thirty-five, Harvard linguist George Kingsley Zipf uncovered a bizarre mathematical pattern across millions of texts.",
    },
    {
        "id": "03-mechanism",
        "text": "Rank every word by frequency. The second appears half as often. The tenth, one-tenth. An unbroken power law.",
    },
    {
        "id": "04-cascade",
        "text": "The same law dictates city populations, website traffic, earthquakes, and wealth. Nature repeats this code.",
    },
    {
        "id": "05-reframe",
        "text": "Why? The Principle of Least Effort. The human brain balances minimal speaker effort against maximum listener clarity.",
    },
    {
        "id": "06-lesson",
        "text": "The takeaway? A tiny fraction of inputs controls the vast majority of outcomes. Master the head of the curve, master the game.",
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


def generate_frame_audio(frame):
    raw_path = os.path.join(OUTPUT_DIR, f"{frame['id']}_raw.wav")
    cmd = [
        "pocket-tts", "generate",
        "--voice", REFERENCE,
        "--text", frame["text"],
        "--output-path", raw_path,
        "--temperature", "0.1",
    ]
    env = os.environ.copy()
    env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    print(f"  [gen] {frame['id']}: \"{frame['text'][:65]}...\"")
    result = run(cmd, env=env)
    if result.returncode != 0:
        print(f"  [ERR] {frame['id']}: {result.stderr[-300:]}")
        sys.exit(1)

    tts_dur = get_duration(raw_path)
    print(f"  [ok] {frame['id']}: TTS raw = {tts_dur:.2f}s")
    return raw_path, tts_dur


def main():
    print("=" * 60)
    print("Zipf's Law — 1080p 60s Narration Generator")
    print(f"Reference voice: {REFERENCE}")
    print("=" * 60)

    if not os.path.exists(REFERENCE):
        print(f"[ERR] Reference audio file not found at {REFERENCE}")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n[step 1] Generating raw TTS audio for each frame...")
    measurements = []
    current_start = 0.0
    crossfade = 0.5
    reveal_offset = 0.35
    hold_tail = 0.45  # clean breathing space before crossfade

    for frame in FRAMES:
        raw_path, tts_dur = generate_frame_audio(frame)
        frame_dur = round(tts_dur + reveal_offset + hold_tail, 2)
        measurements.append({
            "id": frame["id"],
            "raw_path": raw_path,
            "tts_dur": tts_dur,
            "reveal_offset": reveal_offset,
            "duration": frame_dur,
            "start": round(current_start, 2),
            "text": frame["text"]
        })
        current_start += (frame_dur - crossfade)

    total_duration = round(current_start + crossfade, 2)

    print("\n[step 2] Building precise master timeline audio...")
    inputs = []
    filter_parts = []
    for i, m in enumerate(measurements):
        inputs.extend(["-i", m["raw_path"]])
        delay_ms = int((m["start"] + m["reveal_offset"]) * 1000)
        filter_parts.append(f"[{i}]adelay={delay_ms}|{delay_ms}[d{i}]")

    mix_inputs = "".join(f"[d{i}]" for i in range(len(measurements)))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={len(measurements)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[out]"
    )
    filter_str = ";".join(filter_parts)
    narration_path = os.path.join(OUTPUT_DIR, "narration_full.wav")

    result = run([
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[out]",
        "-ar", "24000", "-ac", "1",
        narration_path
    ])
    if result.returncode != 0:
        print(f"[ERR] mix: {result.stderr[-500:]}")
        sys.exit(1)

    actual_master_dur = get_duration(narration_path)
    print(f"\n[ok] Master Narration: {actual_master_dur:.2f}s (Mastered at -14 LUFS)")

    print("\n=== TIMELINE CONFIGURATION SUMMARY ===")
    for m in measurements:
        print(f"  {m['id']}: start={m['start']:.2f}s, duration={m['duration']:.2f}s (TTS speech={m['tts_dur']:.2f}s)")
    print(f"  Root Duration: {actual_master_dur:.2f}s")


if __name__ == "__main__":
    main()
