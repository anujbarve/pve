# HyperFrames Video Projects

## ⚠️ MANDATORY — READ BEFORE ANY VIDEO AUTHORING

**Read `/Users/anujbarve/Documents/gate-research/HYPERFRAMES-SOP.md` first.**
It is the standard operating procedure distilled from past production failures
(pseudo-element animation bugs, wrong canvas size, missing asset renders,
commercial-license traps in TTS models, RAM-blowup voice generation, and more).
It contains the intake questions to ask the user up front ($0 Intake), the
authoring DO/DON'T lists, the transition-seam checklist, the voiceover license
+ chunking rules, and the "done is rendered" verification gate.

## Project Structure

Each video is a **self-contained folder** under `projects/`. No file conflicts
between videos. Shared assets live at the root.

```
explainer-videos/
├── AGENTS.md              ← you are here
├── CLAUDE.md
├── HYPERFRAMES-SOP.md     ← sync pipeline docs (§6)
├── Anuj-style.md          ← shared style guide (Editorial Dark Mode)
├── frame.md               ← shared frame spec
├── package.json           ← shared HyperFrames CLI config
├── reference_clean.wav    ← shared voice clone reference
├── renders/               ← all final renders, organized by project
│   ├── broken-windows/
│   └── occams-razor/
└── projects/
    ├── _template/         ← COPY THIS to start a new project
    │   ├── index.html
    │   ├── BRIEF.md
    │   ├── generate_narration.py
    │   └── compositions/frames/
    ├── broken-windows/
    │   ├── index.html
    │   ├── BRIEF.md
    │   ├── STORYBOARD.md
    │   ├── generate_narration.py
    │   ├── meta.json
    │   └── compositions/frames/
    └── occams-razor/
        ├── index.html
        ├── BRIEF.md
        ├── STORYBOARD.md
        └── compositions/frames/
```

### Creating a New Project (NARRATION-FIRST)

**The golden rule: Script → Audio → Visuals. Never the other way around.**
See `HYPERFRAMES-SOP.md` §6 for the full workflow.

1. Copy `_template/` → `projects/your-topic/`
2. Update `BRIEF.md` with the topic and message
3. **Write the narration script** — one full paragraph per frame
4. **Generate TTS audio** per frame — measure actual durations with ffprobe
5. **Build frame compositions** — animation timing dictated by actual TTS durations
6. **Wire narration as `<audio>` element** in `index.html` so preview plays audio
7. Run `npm run check` → `npm run render` → verify sync

### Working on an Existing Project

```bash
cd projects/your-topic/
npm run dev        # preview (run in background — audio plays in preview)
npm run check      # lint + validate
npm run render     # render to MP4
```

**Preview has audio** — narration is wired as `<audio>` in `index.html`,
so you can verify sync in the preview before rendering.

## Skills — USE THESE FIRST

**Always invoke the relevant skill before writing or modifying compositions.** Skills encode framework-specific patterns (e.g., `window.__timelines` registration, `data-*` attribute semantics, shader-compatible CSS rules) that are NOT in generic web docs.

**Doing anything with HyperFrames?** Start at `/hyperframes` — it routes every request to the right workflow.

The domain skills (`/hyperframes-core`, `/hyperframes-animation`, `/hyperframes-keyframes`, `/hyperframes-creative`, `/hyperframes-cli`, `/media-use`, `/hyperframes-audio`, `/hyperframes-registry`, `/figma`) and the full capability map live inside `/hyperframes`.

## Commands

```bash
npm run dev          # start the preview server (long-running — keep it alive in background)
npm run check        # lint + runtime + layout + motion + contrast (one command)
npm run render       # render to MP4
npm run publish      # publish and get a shareable link
npx hyperframes lint --verbose  # include info-level findings
npx hyperframes docs <topic>    # reference docs in terminal
```

> **`npm run dev` is a long-running server, not a one-shot command.** Always run in background.

## Linting — ALWAYS RUN AFTER CHANGES

After creating or editing any `.html` composition, **always** run:

```bash
npm run check
```

Fix all errors before presenting the result.

## Key Rules

1. Every timed element needs `data-start`, `data-duration`, and `data-track-index`
2. Elements with timing **MUST** have `class="clip"`
3. Timelines must be paused and registered on `window.__timelines`:
   ```js
   window.__timelines = window.__timelines || {};
   window.__timelines["composition-id"] = gsap.timeline({ paused: true });
   ```
4. Videos use `muted` with a separate `<audio>` element for the audio track
5. Sub-compositions use `data-composition-src="compositions/file.html"`
6. Only deterministic logic — no `Date.now()`, no `Math.random()`, no network fetches
7. **Audio sync**: see `HYPERFRAMES-SOP.md` §6 for the full narration sync pipeline
