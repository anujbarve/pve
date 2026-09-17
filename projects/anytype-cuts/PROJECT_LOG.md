# Production & Pipeline Documentation: Anytype Video Enhancement

**Date:** September 17, 2026  
**Source File:** `anytype.mp4` (2940×1912 @ 60 FPS, 10m 43.39s / 643.392s)  
**Output File:** `anytype_enhanced.mp4` (2940×1912 @ 60 FPS, 100% audio sync preserved)  
**Methodology:** Jack Butcher / Visualize Value Minimalist B&W Standard + HyperFrames Modular Rendering + FFmpeg Lossless Stream Assembly

---

## 1. Executive Summary & Objective

Rendering a full 10-minute 60 FPS video end-to-end within heavy headless browser capture frameworks can take hours or days and risks memory thrashing. 

To solve this, we implemented a **modular cutaway & splice architecture**:
1. Transcribe the audio stream with millisecond accuracy.
2. Identify high-leverage conceptual moments suitable for animated mental models and comparison matrices.
3. Author and render lightweight, isolated HTML/GSAP clips in seconds using HyperFrames.
4. Execute an automated multi-input FFmpeg pipeline that splices the rendered animations directly into the raw desktop screen recording while maintaining continuous audio.

---

## 2. Audio Extraction & MLX Whisper Transcription

- **Extracted Audio:** `projects/anytype-cuts/audio_16k.wav` (16kHz mono PCM).
- **Engine:** `mlx-whisper` on Apple Silicon Metal GPU.
- **Output Artifacts:**
  - `projects/anytype-cuts/transcript.json`: Full segment & word-level timing data.
  - `projects/anytype-cuts/TRANSCRIPTION.md`: Human-readable timestamped transcript.

---

## 3. Motion Clip Design & Render Specifications

Each motion clip was authored in pure HTML/CSS/GSAP following the **Simplicity Doctrine**:
- Monochromatic palette (`#000000` absolute void, `#FFFFFF` crisp geometry, `#888890` metadata).
- Pure CSS geometric primitives (no complex SVG transform glitches).
- 60 FPS deterministic GSAP timelines.

### Delivered Visual Clips:
| Clip ID | Target Time Range | Duration | Composition Source | Theme & Mental Model |
|---|---|---|---|---|
| **Clip 1** | `00:00.00 – 00:15.00` | 15.0s | `clips/clip1_intro/index.html` | **The Second Brain in the AI Era**: Input Overload → Working Memory Bottleneck → Anytype Solution |
| **Clip 2** | `01:08.00 – 01:32.00` | 24.0s | `clips/clip2_comparison/index.html` | **3-Way Comparison Matrix**: Obsidian (Markdown / Plugin Sync) vs Notion (Cloud Lock-in) vs Anytype (P2P Mesh) |
| **Clip 3** | `01:38.00 – 02:05.00` | 27.0s | `clips/clip3_security/index.html` | **Cryptographic Sovereignty**: Client Private Keys ⇄ Encrypted Mesh with Strikethrough Third-Party Cloud Servers |
| **Clip 4** | `09:18.00 – 09:32.00` | 14.0s | `clips/clip4_sync/index.html` | **Local Mesh Handshake**: Desktop ⇄ Android direct local network handshake (&lt;10ms latency, zero cloud) |
| **Clip 5** | `10:25.00 – 10:41.00` | 16.0s | `clips/clip5_outro/index.html` | **The Verdict**: 01 Local-First • 02 Object Graph • 03 Peer-to-Peer Protocol |

*All 5 clips rendered in parallel/sequence via `npx hyperframes render` in under 45 seconds total.*

---

## 4. FFmpeg Video Assembly Pipeline

We built `projects/anytype-cuts/merge_video.py` to automate the complete sequence assembly:

```
[c1: 00:00-00:15] ──> [s1: 00:15-01:08] ──> [c2: 01:08-01:32] ──> [s2: 01:32-01:38]
──> [c3: 01:38-02:05] ──> [s3: 02:05-09:18] ──> [c4: 09:18-09:32] ──> [s4: 09:32-10:25]
──> [c5: 10:25-10:41] ──> [s5: 10:41-10:43]
```

### FFmpeg Filter Graph:
- **Aspect Ratio Standardization:** `scale=2940:1912:force_original_aspect_ratio=decrease,pad=2940:1912:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=60`
- **Video Splicing:** 10-node concatenation (`concat=n=10:v=1:a=0`)
- **Audio Integrity:** `-c:a copy` from original stream `0:a` (zero re-encoding loss or drift).
- **Result:** `anytype_enhanced.mp4` (299 MB, 2940×1912 @ 60 FPS).

---

## 5. Metadata, Packaging & Distribution

1. **High-CTR YouTube Titles:**
   - *Why I Left Notion & Obsidian for Anytype (The P2P Second Brain)*
   - *The Ultimate Local-First Second Brain: Anytype in the Age of AI*
   - *Anytype: Your Data, Your Keys, No Cloud Servers*

2. **In-Depth YouTube Description:** Complete technical overview, schema breakdown, and formatted timestamps.

3. **High-Impact Thumbnail Text Options:**
   - `NOTION IS DEAD.`
   - `0 SERVERS. 100% PRIVATE.`
   - `THE OBSIDIAN KILLER?`
   - `10,000 NOTES. ZERO LAG.`
   - `YOUR KEYS. YOUR DATA.`
