#!/usr/bin/env python3
"""Generate narration audio for Zipf's Law — synced to visual reveals.

Key insight: TTS speaks slower than expected. Frame durations must match actual
speech pace, not estimated word counts. Every line of on-screen text is narrated.
Short reveal offsets so speech starts almost immediately.
"""

import subprocess
import os
import sys

RENDER_DIR = os.path.dirname(os.path.abspath(__file__))
# Check location of reference_clean.wav
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
        "start": 0.0,
        "duration": 9.5,
        "reveal_offset": 0.5,
        "text": "The most common word in English is 'the'. It makes up seven percent of everything you speak. The second word appears half as often. The third, one-third. Why does this rule govern every language on Earth?",
    },
    {
        "id": "02-origin",
        "start": 9.0,
        "duration": 9.5,
        "reveal_offset": 0.5,
        "text": "In nineteen thirty-five, Harvard linguist George Kingsley Zipf uncovered a bizarre mathematical pattern hidden across millions of written texts.",
    },
    {
        "id": "03-mechanism",
        "start": 18.0,
        "duration": 11.5,
        "reveal_offset": 0.5,
        "text": "Rank every word by frequency. The second word appears half as often as the first. The tenth, one-tenth. The ten-thousandth, one-ten-thousandth. An unbroken power law.",
    },
    {
        "id": "04-cascade",
        "start": 29.0,
        "duration": 12.0,
        "reveal_offset": 0.5,
        "text": "It gets weirder. The exact same law dictates the population of world cities, visits to websites, earthquake severity, and the distribution of wealth. Nature repeats this code everywhere.",
    },
    {
        "id": "05-reframe",
        "start": 40.5,
        "duration": 10.5,
        "reveal_offset": 0.5,
        "text": "Why does this happen? The Principle of Least Effort. The human brain constantly balances the speaker's desire to use few words against the listener's demand for clarity.",
    },
    {
        "id": "06-lesson",
        "start": 50.5,
        "duration": 9.5,
        "reveal_offset": 0.5,
        "text": "The real takeaway? A tiny fraction of inputs controls the vast majority of outcomes. Master the head of the curve. Master the game.",
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
    """Generate TTS audio for a single frame, synced to visual reveal."""
    raw_path = os.path.join(OUTPUT_DIR, f"{frame['id']}_raw.wav")
    synced_path = os.path.join(OUTPUT_DIR, f"{frame['id']}.wav")

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
    offset = frame["reveal_offset"]
    max_speech = frame["duration"] - offset

    if tts_dur > max_speech:
        print(f"  [TRIM] {frame['id']}: {tts_dur:.1f}s -> {max_speech:.1f}s")
        run([
            "ffmpeg", "-y", "-i", raw_path,
            "-t", str(max_speech),
            "-af", f"adelay={int(offset * 1000)}|{int(offset * 1000)}",
            "-ar", "24000", "-ac", "1",
            synced_path
        ])
    else:
        pad_end = max(0, frame["duration"] - offset - tts_dur)
        run([
            "ffmpeg", "-y", "-i", raw_path,
            "-af", f"adelay={int(offset * 1000)}|{int(offset * 1000)},apad=pad_dur={pad_end:.3f}",
            "-t", str(frame["duration"]),
            "-ar", "24000", "-ac", "1",
            synced_path
        ])

    actual_dur = get_duration(synced_path)
    print(f"  [ok] {frame['id']}: TTS={tts_dur:.2f}s, offset={offset:.1f}s, total={actual_dur:.2f}s")
    return raw_path, tts_dur


def main():
    print("=" * 60)
    print("Zipf's Law — Narration Generator")
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

    for frame in FRAMES:
        raw_path, tts_dur = generate_frame_audio(frame)
        offset = 0.5
        hold_buffer = 1.6
        frame_dur = max(tts_dur + offset + hold_buffer, 6.5)
        measurements.append({
            "id": frame["id"],
            "raw_path": raw_path,
            "tts_dur": tts_dur,
            "reveal_offset": offset,
            "duration": frame_dur,
            "start": current_start,
            "text": frame["text"]
        })
        current_start += (frame_dur - crossfade)

    total_duration = current_start + crossfade

    print("\n[step 2] Building precise master timeline audio...")
    inputs = []
    filter_parts = []
    for i, m in enumerate(measurements):
        inputs.extend(["-i", m["raw_path"]])
        delay_ms = int((m["start"] + m["reveal_offset"]) * 1000)
        filter_parts.append(f"[{i}]adelay={delay_ms}|{delay_ms}[d{i}]")

    mix_inputs = "".join(f"[d{i}]" for i in range(len(measurements)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(measurements)}:duration=longest:dropout_transition=0[out]")
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
    print(f"\n[ok] Master Narration: {actual_master_dur:.2f}s")
    print(f"Total Composition Duration needed: {actual_master_dur:.2f}s")

    print("\n=== TIMELINE CONFIGURATION SUMMARY ===")
    for m in measurements:
        print(f"  {m['id']}: start={m['start']:.2f}s, duration={m['duration']:.2f}s (TTS speech={m['tts_dur']:.2f}s)")
    print(f"  Root Duration: {actual_master_dur:.2f}s")


if __name__ == "__main__":
    main()
