# HyperFrames Video Projects

## ⚠️ MANDATORY — READ BEFORE ANY VIDEO AUTHORING

**Read `./HYPERFRAMES-SOP.md` and `./MINIMAL-STYLE.md` first.**
It is the standard operating procedure distilled from past production lessons:
- **The Simplicity Doctrine (Jack Butcher / Visualize Value / Naval Ravikant)**:
  - Simple black and white (`#000000` / `#FFFFFF`).
  - No visual fuss. No decorative cards, no stock images slapped behind text, no fake gradients.
  - **Pure Primitives Only**: Circles, boxes, straight lines, progress bars, and bold clean typography.
  - Zero complex hand-drawn SVG paths or coordinate rotation bugs.
- **1080×1920 Vertical FHD @ 60 FPS** with **Halfway Safe-Zone Captions (`bottom: 480px`)**.
- **Voice-First Audio (-14 LUFS)**: Master narration upfront (-14.0 LUFS) + Meditative Ambient Piano (-19 dB) + Prominent Tactile SFX (-10 dB).

## Project Structure

Each video is a **self-contained folder** under `projects/`. Shared assets live at the root.

```
explainer-videos/
├── AGENTS.md              ← you are here
├── CLAUDE.md
├── HYPERFRAMES-SOP.md     ← canonical standard operating procedure
├── MINIMAL-STYLE.md       ← shared style guide (Jack Butcher / Naval Simplicity Doctrine)
├── HUMAN-REPRESENTATION-SOP.md ← specialized SOP: human figures & sensory rigs
├── MASTER-STYLE.md        ← master principles & filmmaking standards
├── frame.md               ← shared frame spec
├── package.json           ← shared HyperFrames CLI config
├── reference_clean.wav    ← shared voice clone reference
├── renders/               ← all final renders, organized by project
└── projects/
    ├── _template/         ← COPY THIS to start a new project
    └── 2026-09-15_emotional-redlining/
```

### Creating a New Project (NARRATION-FIRST & SIMPLICITY PARADIGM)

**The golden rule: Script → Audio → Visuals. Never the other way around.**

1. Copy `_template/` → `projects/YYYY-MM-DD_your-topic/`
2. Update `BRIEF.md` with the mental model shot list.
3. **Write the narration script** — 1 punchy, crystalline, philosophical sentence per shot.
4. **Generate TTS audio** per shot (`generate_narration.py`) — conversational temperature (`0.7`), measure exact durations with `ffprobe`.
5. **Generate Audio Mix** (`generate_sound_design.py`):
   - Vocal: -14.0 LUFS upfront and intimate.
   - BGM: Slow breathing ambient piano / analog drone at -19.0 dB.
   - SFX: Prominent tactile drafting clicks, mechanical switch snaps, and line draw friction (-10 dB to -13 dB).
6. **Build Primitive Visual Diagrams** (`compositions/frames/shot-*.html`):
   - Pure black `#000000` canvas.
   - Built exclusively from CSS primitives (circles, boxes, straight lines, progress frames).
   - Minimalist subtitles centered at **`bottom: 480px`**.
7. Run `npm run check` → `npm run render` → verify sync and safe zones.

## Commands

```bash
npm run dev          # start the preview server (long-running — keep alive in background)
npm run check        # lint + runtime + layout + motion + contrast (one command)
npm run render       # render to MP4
npm run publish      # publish and get a shareable link
```

## Key Rules

1. **The Simplicity Litmus Test**: If a visual contains decorative gradients, floating cards, or random stock photos, **it has failed**. Design pure, undeniable mental model diagrams.
2. Every timed element needs `data-start`, `data-duration`, and `data-track-index` with `class="clip"`.
3. Timelines must be paused and registered on `window.__timelines`:
   ```js
   window.__timelines = window.__timelines || {};
   window.__timelines["composition-id"] = gsap.timeline({ paused: true });
   ```
4. Only deterministic logic — no `Date.now()`, no `Math.random()`, no network fetches.
5. **Canvas Standard**: **1080×1920** (FHD 9:16 vertical, 60 FPS).
6. **Optical Safe Zones**: Position captions and core action at **`bottom: 480px` / Y = 325px – 1440px** on 1080×1920 canvas.
7. **Audio Mastering (-14 LUFS)**: Master narration must achieve **-14.0 LUFS to -16.0 LUFS** with `normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7`.
8. **Primitives Only**: Use standard CSS/HTML primitives (circles, rectangles, lines). Avoid complex SVG paths with dynamic rotation origins that glitch in capture workers.
