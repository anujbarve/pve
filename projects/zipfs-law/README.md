# Zipf's Law — Editorial Dark Mode Explainer Reel (1080p 60s Vertical)

This project contains the complete source code, audio pipeline, authentic historical/scientific visual assets, and motion compositions for the 1080p 60s vertical explainer video on **Zipf's Law**.

## Quick Start & Commands

```bash
# From this directory:
npm run dev        # Launch preview server in background
npm run check      # Run lint, runtime, layout, and contrast checks (1 shot)
npm run render     # Render 1080p 60 FPS vertical MP4
```

## Directory Structure

```
zipfs-law/
├── assets/                          ← High-res authentic visual assets
│   ├── 01_codex.jpg                 ← Ancient manuscript with mathematical distribution
│   ├── 02_scholar.jpg               ← George Kingsley Zipf at 1935 Harvard desk
│   ├── 04_cities.jpg                ← Metropolis population & data grid
│   └── 05_brain.jpg                 ← Cognitive equilibrium scale
├── compositions/frames/             ← Standalone sub-compositions per scene
│   ├── 01-hook.html                 ← Hook: The 7% "THE" frequency anomaly
│   ├── 02-origin.html               ← Origin: 1935 Harvard discovery & scholar card
│   ├── 03-mechanism.html            ← Mechanism: 1/r step-down waterfall bar cascade
│   ├── 04-cascade.html              ← Cascade: Cross-domain city & web traffic
│   ├── 05-reframe.html              ← Reframe: Principle of Least Effort duality
│   └── 06-lesson.html               ← Lesson: Luxury manifesto & vital-few CTAs
├── .temp_audio/                     ← Generated Pocket-TTS audio & master mix
│   ├── narration_full.wav           ← 59.21s master mixed track
│   └── [frame_id]_raw.wav           ← Per-frame audio captures
├── generate_narration.py            ← TTS generator & duration calculator
├── index.html                       ← Master composition & crossfade timeline
├── meta.json                        ← Project metadata
├── package.json                     ← NPM scripts for HyperFrames CLI
├── BRIEF.md                         ← Project brief & core specs
├── STORYBOARD.md                    ← Full frame-by-frame direction & choreography
└── narration_script.md              ← Word-by-word narration & timestamp breakdown
```

## Key Specs

- **Resolution:** `1080×1920` (FHD 9:16 portrait)
- **Framerate:** `60 FPS`
- **Duration:** `59.21s` (~60s explainer reel format)
- **Design System:** Editorial Dark Mode (`#000000` ground, `#F2F1EC` primary text, `#F2D24B` mustard gold hero accent, Playfair Display + Inter)
- **Platform Safe Zone:** Strict vertical centering within $Y = 325\text{px} - 1425\text{px}$ (max-width: 920px)
