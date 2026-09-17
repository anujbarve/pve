#!/usr/bin/env python3
import subprocess
import os
import sys

BASE_DIR = "/Users/anujbarve/Documents/explainer-videos"
PROJECT_DIR = os.path.join(BASE_DIR, "projects/anytype-cuts")
CLIPS_DIR = os.path.join(PROJECT_DIR, "clips")
INPUT_VIDEO = os.path.join(BASE_DIR, "anytype.mp4")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "anytype_enhanced.mp4")

# Defined cutaway intervals and corresponding clip paths
# (start_time, end_time, clip_filename)
CUTS = [
    (0.0, 15.0, "clip1_intro.mp4"),
    (68.0, 92.0, "clip2_comparison.mp4"),
    (98.0, 125.0, "clip3_security.mp4"),
    (558.0, 572.0, "clip4_sync.mp4"),
    (625.0, 641.0, "clip5_outro.mp4"),
]

def main():
    print("=== Starting Anytype Video Enhancement & Merge ===")
    
    # 1. Verify all clips exist
    for _, _, clip in CUTS:
        clip_path = os.path.join(CLIPS_DIR, clip)
        if not os.path.exists(clip_path):
            print(f"Error: Required clip not found: {clip_path}")
            sys.exit(1)
        print(f"✓ Found clip: {clip}")

    # Build complex ffmpeg filter graph
    # Total inputs:
    # [0:v] = anytype.mp4 video stream
    # [0:a] = anytype.mp4 original audio stream (untouched!)
    # [1:v] = clip1_intro.mp4
    # [2:v] = clip2_comparison.mp4
    # [3:v] = clip3_security.mp4
    # [4:v] = clip4_sync.mp4
    # [5:v] = clip5_outro.mp4
    
    # Target resolution: 2940x1912 (matching original screen recording)
    # Target fps: 60
    
    # Segments to cut from input video:
    # seg0: 15.0 to 68.0
    # seg1: 92.0 to 98.0
    # seg2: 125.0 to 558.0
    # seg3: 572.0 to 625.0
    # seg4: 641.0 to 643.392
    
    filter_parts = []
    
    # Scale helper for 16:9 clips to fit into 2940x1912 with black pillar/letterbox
    scale_filter = "scale=2940:1912:force_original_aspect_ratio=decrease,pad=2940:1912:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=60"
    
    # Prepare scaled clips
    filter_parts.append(f"[1:v]{scale_filter}[c1];")
    filter_parts.append(f"[2:v]{scale_filter}[c2];")
    filter_parts.append(f"[3:v]{scale_filter}[c3];")
    filter_parts.append(f"[4:v]{scale_filter}[c4];")
    filter_parts.append(f"[5:v]{scale_filter}[c5];")
    
    # Prepare trimmed segments from original screen recording [0:v]
    filter_parts.append(f"[0:v]trim=start=15.0:end=68.0,setpts=PTS-STARTPTS,fps=60[s1];")
    filter_parts.append(f"[0:v]trim=start=92.0:end=98.0,setpts=PTS-STARTPTS,fps=60[s2];")
    filter_parts.append(f"[0:v]trim=start=125.0:end=558.0,setpts=PTS-STARTPTS,fps=60[s3];")
    filter_parts.append(f"[0:v]trim=start=572.0:end=625.0,setpts=PTS-STARTPTS,fps=60[s4];")
    filter_parts.append(f"[0:v]trim=start=641.0:end=643.392,setpts=PTS-STARTPTS,fps=60[s5];")
    
    # Concat in exact sequential order:
    # [c1] -> [s1] -> [c2] -> [s2] -> [c3] -> [s3] -> [c4] -> [s4] -> [c5] -> [s5]
    filter_parts.append("[c1][s1][c2][s2][c3][s3][c4][s4][c5][s5]concat=n=10:v=1:a=0[outv]")
    
    filter_complex = "".join(filter_parts)
    
    cmd = [
        "ffmpeg", "-y",
        "-i", INPUT_VIDEO,
        "-i", os.path.join(CLIPS_DIR, "clip1_intro.mp4"),
        "-i", os.path.join(CLIPS_DIR, "clip2_comparison.mp4"),
        "-i", os.path.join(CLIPS_DIR, "clip3_security.mp4"),
        "-i", os.path.join(CLIPS_DIR, "clip4_sync.mp4"),
        "-i", os.path.join(CLIPS_DIR, "clip5_outro.mp4"),
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        OUTPUT_VIDEO
    ]
    
    print("\nExecuting ffmpeg assembly pipeline...")
    print("Command:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"\n✨ Video enhancement successfully rendered to: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    main()
