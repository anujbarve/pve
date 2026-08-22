#!/usr/bin/env python3
"""Template narration generator — update FRAMES and TOTAL_DURATION for your project.

See HYPERFRAMES-SOP.md §6 for the full sync pipeline.
"""

import subprocess
import os
import sys

RENDER_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE = os.path.join(os.path.dirname(RENDER_DIR), "..", "..", "reference_clean.wav")
OUTPUT_DIR = os.path.join(RENDER_DIR, ".temp_audio")

# === UPDATE THESE FOR YOUR PROJECT ===
FRAMES = [
    {
        "id": "01-example",
        "start": 0.0,
        "duration": 6.0,
        "reveal_offset": 0.5,
        "text": "Your narration text for this frame.",
    },
    # Add more frames...
]

TOTAL_DURATION = 6.0  # Sum of all frame durations (accounting for overlaps)
# === END UPDATE ===


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
    print(f"  [gen] {frame['id']}: \"{frame['text'][:60]}...\"")
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
    print("\n[build] Building narration track...")
    inputs = []
    filter_parts = []
    for i, frame in enumerate(FRAMES):
        clip_path = os.path.join(OUTPUT_DIR, f"{frame['id']}.wav")
        inputs.extend(["-i", clip_path])
        delay_ms = int(frame["start"] * 1000)
    mix_inputs = "".join(f"[d{i}]" for i in range(len(FRAMES)))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={len(FRAMES)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[out]"
    )

    narration_path = os.path.join(OUTPUT_DIR, "narration_full.wav")
    result = run([
        "ffmpeg", "-y", *inputs,
        "-filter_complex", ";".join(filter_parts),
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
    print("Project — Narration Generator")
    print("=" * 60)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n[step 1] Generating synced frame audio...")
    for frame in FRAMES:
        generate_frame_audio(frame)

    print("\n[step 2] Building narration track...")
    narration_path = build_narration_track()

    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        output_path = os.path.join(RENDER_DIR, "renders", "final_with_audio.mp4")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        mux_video_audio(video_path, narration_path, output_path)
    else:
        print("\n[info] No video path. Run: python generate_narration.py <video.mp4>")

    print("\n" + "=" * 60)
    print("DONE!")


if __name__ == "__main__":
    main()
