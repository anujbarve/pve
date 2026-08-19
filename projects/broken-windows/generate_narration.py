#!/usr/bin/env python3
"""Generate narration audio for Broken Windows Theory — synced to visual reveals.

Key insight: TTS speaks slower than expected. Frame durations must match actual
speech pace, not estimated word counts. Every line of on-screen text is narrated.
Short reveal offsets so speech starts almost immediately.
"""

import subprocess
import os
import sys

RENDER_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE = os.path.join(os.path.dirname(RENDER_DIR), "..", "..", "reference_clean.wav")
OUTPUT_DIR = os.path.join(RENDER_DIR, ".temp_audio")

# Frame timings — extended to fit natural TTS pace
FRAMES = [
    {
        "id": "01-hook",
        "start": 0.0,
        "duration": 7.5,
        "reveal_offset": 0.5,
        "text": "You walk past a broken window every day. You never think twice about it.",
    },
    {
        "id": "02-origin",
        "start": 7.0,
        "duration": 11.0,
        "reveal_offset": 0.5,
        "text": "In nineteen eighty-two, two criminologists noticed something. Wilson and Kelling. They called it the Broken Windows Theory.",
    },
    {
        "id": "03-mechanism",
        "start": 17.5,
        "duration": 7.5,
        "reveal_offset": 0.5,
        "text": "A broken window isn't just damage. It's a signal that says nobody is watching.",
    },
    {
        "id": "04-cascade",
        "start": 24.5,
        "duration": 10.0,
        "reveal_offset": 0.5,
        "text": "One broken window turns into two. Then ten. Then the whole block falls apart.",
    },
    {
        "id": "05-reframe",
        "start": 34.0,
        "duration": 7.0,
        "reveal_offset": 0.5,
        "text": "It was never about the window. It's about the signal it sends.",
    },
    {
        "id": "06-lesson",
        "start": 40.5,
        "duration": 11.0,
        "reveal_offset": 0.5,
        "text": "The bigger lesson. The small things you ignore are telling everyone what you'll tolerate. Fix the signal. Change the story.",
    },
]

TOTAL_DURATION = 51.5


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
    print(f"  [ok] {frame['id']}: TTS={tts_dur:.1f}s, offset={offset:.1f}s, dead_air={max(0,dead_air):.1f}s / {frame['duration']:.1f}s")
    return synced_path


def build_narration_track():
    """Mix all frame audio onto master timeline at correct positions."""
    print("\n[build] Building narration track...")

    inputs = []
    filter_parts = []
    for i, frame in enumerate(FRAMES):
        clip_path = os.path.join(OUTPUT_DIR, f"{frame['id']}.wav")
        inputs.extend(["-i", clip_path])
        delay_ms = int(frame["start"] * 1000)
        filter_parts.append(f"[{i}]adelay={delay_ms}|{delay_ms}[d{i}]")

    mix_inputs = "".join(f"[d{i}]" for i in range(len(FRAMES)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(FRAMES)}:duration=longest:dropout_transition=0[out]")

    filter_str = ";".join(filter_parts)
    narration_path = os.path.join(OUTPUT_DIR, "narration_full.wav")

    result = run([
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[out]",
        "-t", str(TOTAL_DURATION),
        "-ar", "24000", "-ac", "1",
        narration_path
    ])
    if result.returncode != 0:
        print(f"[ERR] mix: {result.stderr[-500:]}")
        sys.exit(1)

    total = get_duration(narration_path)
    print(f"[ok] Narration track: {total:.1f}s (target: {TOTAL_DURATION:.1f}s)")
    return narration_path


def mux_video_audio(video_path, audio_path, output_path):
    """Combine silent video with narration audio into final MP4."""
    print("\n[mux] Combining video + audio...")
    result = run([
        "ffmpeg", "-y",
        "-i", video_path, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", output_path
    ])
    if result.returncode != 0:
        print(f"[ERR] ffmpeg mux: {result.stderr[-300:]}")
        sys.exit(1)
    print(f"[done] Final video: {output_path}")


def main():
    print("=" * 60)
    print("Broken Windows Theory — Narration Generator (Final)")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n[step 1] Generating synced frame audio...")
    for frame in FRAMES:
        generate_frame_audio(frame)

    print("\n[step 2] Building narration track...")
    narration_path = build_narration_track()

    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        output_path = os.path.join(RENDER_DIR, "renders", "broken_windows_with_audio.mp4")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        mux_video_audio(video_path, narration_path, output_path)
    else:
        print("\n[info] No video path. Run: python generate_narration.py <video.mp4>")

    print("\n" + "=" * 60)
    print("DONE!")
    print(f"  Narration: {narration_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
