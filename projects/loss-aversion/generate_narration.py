#!/usr/bin/env python3
"""Generate narration audio for Loss Aversion — synced to visual reveals.

Key insight: TTS speaks slower than expected. Frame durations must match actual
speech pace, not estimated word counts. Every line of on-screen text is narrated.
Short reveal offsets so speech starts almost immediately.
"""

import subprocess
import os
import sys

RENDER_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE = os.path.abspath(os.path.join(RENDER_DIR, "..", "..", "..", "reference_clean.wav"))
OUTPUT_DIR = os.path.join(RENDER_DIR, ".temp_audio")

# Initial frame structure
FRAMES = [
    {
        "id": "01-hook",
        "start": 0.0,
        "duration": 8.5,
        "reveal_offset": 0.5,
        "text": "Losing a hundred dollars hurts twice as much as finding a hundred dollars feels good.",
    },
    {
        "id": "02-origin",
        "start": 8.0,
        "duration": 10.5,
        "reveal_offset": 0.5,
        "text": "In nineteen seventy-nine, psychologists Daniel Kahneman and Amos Tversky uncovered a strange truth about human nature.",
    },
    {
        "id": "03-mechanism",
        "start": 18.0,
        "duration": 10.5,
        "reveal_offset": 0.5,
        "text": "We aren't wired to maximize gains. We are hardwired to protect against defeat. The pain of losing is twice as strong.",
    },
    {
        "id": "04-cascade",
        "start": 28.0,
        "duration": 11.0,
        "reveal_offset": 0.5,
        "text": "This fear traps us. Holding onto losing bets. Staying in comfortable ruts. Passing up big opportunities just to avoid loss.",
    },
    {
        "id": "05-reframe",
        "start": 38.5,
        "duration": 9.0,
        "reveal_offset": 0.5,
        "text": "It was never about avoiding mistakes. The biggest risk is the life you miss while playing not to lose.",
    },
    {
        "id": "06-lesson",
        "start": 47.0,
        "duration": 11.5,
        "reveal_offset": 0.5,
        "text": "The real lesson? Stop protecting what you have at the expense of what you could become. Take the asymmetry. Play to win.",
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
    dead_air = frame["duration"] - offset - tts_dur
    print(f"  [ok] {frame['id']}: TTS={tts_dur:.2f}s, offset={offset:.1f}s, total={actual_dur:.2f}s")
    return raw_path, tts_dur


def main():
    print("=" * 60)
    print("Loss Aversion — Narration Generator")
    print("=" * 60)

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
    filter_parts.append(f"{mix_inputs}amix=inputs={len(measurements)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[out]")
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
