# HyperFrames Video Projects

## ⚠️ MANDATORY — READ BEFORE ANY VIDEO AUTHORING

**Read `./HYPERFRAMES-SOP.md` first.**
It is the standard operating procedure distilled from past production failures:
- The **Anti-PowerPoint Filmmaking Doctrine** (Shots > Cards; eliminate the "Card Prison").
- The **Reality-First Entry Point** (Human experience before abstract diagrams).
- **1080×1920 Vertical FHD @ 60 FPS** with **Halfway Safe-Zone Captions (`bottom: 480px`)**.
- **Audio Mastering Standard (-14 LUFS)** with `normalize=0` and exact TTS duration sync.

## Project Structure

Each video is a **self-contained folder** under `projects/`. Shared assets live at the root.

```
explainer-videos/
├── AGENTS.md              ← you are here
├── CLAUDE.md
├── HYPERFRAMES-SOP.md     ← canonical standard operating procedure
├── MASTER-STYLE.md        ← universal master filmmaking prompt & principles
├── Anuj-style.md          ← shared style guide (Editorial Dark Mode)
├── frame.md               ← shared frame spec
├── package.json           ← shared HyperFrames CLI config
├── reference_clean.wav    ← shared voice clone reference
├── renders/               ← all final renders, organized by project
└── projects/
    ├── _template/         ← COPY THIS to start a new project
    └── predictive-processing/
```

### Creating a New Project (NARRATION-FIRST & FILMMAKING PARADIGM)

**The golden rule: Script → Audio → Visuals. Never the other way around.**

1. Copy `_template/` → `projects/your-topic/`
2. Update `BRIEF.md` with the narrative shot list.
3. **Write the narration script** — 1 punchy, visceral sentence per shot.
4. **Generate TTS audio** per shot (`generate_narration.py`) — measure exact durations with `ffprobe`.
5. **Build full-bleed shot compositions** (`compositions/frames/shot-*.html`):
   - Full-bleed 1080×1920 spatial environment (no floating cards inside a black void).
   - Dynamic camera movement (macro tracking, parallax, push-ins).
   - Conceptual animations emerge *directly from the physical objects*.
   - Minimalist cinematic subtitles at **`bottom: 480px`** (immune to platform chrome).
6. **Wire narration as `<audio>` element** in `index.html` matching master audio length.
7. Run `npm run check` → `npm run render` → verify sync and safe zones.

## Commands

```bash
npm run dev          # start the preview server (long-running — keep alive in background)
npm run check        # lint + runtime + layout + motion + contrast (one command)
npm run render       # render to MP4
npm run publish      # publish and get a shareable link
```

## Key Rules

1. **Anti-PowerPoint Litmus Test**: If 5 consecutive frames can be understood as a slide deck, **it has failed**. Design continuous cinematic shots, not slides.
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
8. **NO AI-Generated Images**: Strictly use authentic historical, scientific, or public domain archives.
