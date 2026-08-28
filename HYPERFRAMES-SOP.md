# HyperFrames Video SOP — The Filmmaking Standard (Do's & Don'ts)

Standard operating procedure for producing high-retention, cinematic explainer films
and visual essays in HyperFrames. Distilled from real production lessons.

> [!CAUTION]
> ### 🚨 THE 5 NON-NEGOTIABLES (NEVER FORGET)
> 1. **Filmmaking First (Anti-PowerPoint Doctrine)**: The fundamental unit of production is a **SHOT**, NOT a card or slide. If 5 consecutive frames can be screenshotted and understood as a slide deck, **the video has failed**. Avoid the "Card Prison" (floating rounded boxes in a black void with engineering grids).
> 2. **Reality-First Visual Hierarchy**: Always open with a visceral human experience or physical event in a believable environment. Conceptual graphics and diagrams must emerge *directly from the physical geometry of the scene*, not as isolated UI widgets.
> 3. **1080×1920 Vertical Canvas @ 60 FPS**: Standard is **1080×1920** (FHD 9:16 vertical), 60 FPS. Full-bleed spatial environments across the entire canvas.
> 4. **Optical Safe Zone & Halfway Captions**: Captions and key focal action MUST sit near the lower third of the center 1:1 square (**`bottom: 480px` / Y = 1350px–1440px**). Never push text to the bottom edge where platform chrome (Reels/TikTok/Shorts UI) will cover it.
> 5. **Audio Mastering (-14 LUFS) & Zero Dead Air**: Master voiceover to **-14.0 LUFS to -16.0 LUFS** using `normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7`. Measure exact TTS durations with `ffprobe` to ensure zero dead air pauses.

Sections: [0. Intake](#0-intake--ask-first) · [1. Setup](#1-setup) ·
[2. The Anti-PowerPoint Filmmaking Doctrine](#2-the-anti-powerpoint-filmmaking-doctrine) ·
[3. Authoring Do's](#3-authoring-dos) · [4. Authoring Don'ts](#4-authoring-donts) ·
[5. Camera, Safe Zones & Motion Architecture](#5-camera-safe-zones--motion-architecture) ·
[6. Audio & Narration Workflow](#6-audio--narration-workflow) ·
[7. Verification Gate](#7-verification-gate--done-is-rendered).

---

## 0. Intake — ASK FIRST

Before touching any file, confirm the requirements:
1. **Topic & Narrative Arc**: What is the core mystery, human experience, and revelation?
2. **Deliverable Format**: 1080×1920 vertical (9:16), 60 FPS, ~45–60s runtime.
3. **Voiceover**: Voice clone reference or TTS preset. Mastered to -14 LUFS.
4. **Visual Sourcing**: Authentic archival, documentary, or physical spatial environments. Zero synthetic/AI artifacts.

---

## 1. Setup

- Check `package.json` scripts:
  - `npm run dev` → preview server (**run in background**).
  - `npm run check` → lint + runtime + layout + motion + contrast in one shot.
  - `npm run render` → MP4 export.
  - `npm run publish` → shareable link.
- Structure: `index.html` (master timeline), `compositions/frames/` (sub-compositions), `meta.json`, `.temp_audio/`.

---

## 2. The Anti-PowerPoint Filmmaking Doctrine

### The Card Prison Fallacy:
Never build a video by placing a photo in a box on the left, a diagram in a box on the right, a giant headline underneath, and a caption pill at the bottom. That is a **McKinsey dashboard**, not a film.

### The Shot Specification:
Every shot must define:
1. **SUBJECT**: What physical object, person, or phenomenon is in focus?
2. **ENVIRONMENT**: What full-bleed atmosphere (warm table, study, laboratory, street) fills the 1080×1920 canvas?
3. **ACTION**: What physical event occurs (reaching, missing, stopping, breaking, revealing)?
4. **CAMERA**: How does the lens move (macro tracking, push-in, parallax pan, pull-back)?
5. **LIGHT**: Directional rim lighting, shadow contrast, depth of field.
6. **TRANSFORMATION**: How does the scene physically or conceptually evolve over time?
7. **PURPOSE**: What does the viewer experience before reading any text?

---

## 3. Authoring DO's

- **Every timed element** needs `data-start`, `data-duration`, and `data-track-index`.
- Elements with timing **MUST** have `class="clip"`.
- **Register and pause every timeline** on `window.__timelines`:
  ```js
  window.__timelines = window.__timelines || {};
  window.__timelines["composition-id"] = gsap.timeline({ paused: true });
  ```
- **Full-Bleed 1080×1920 Canvas**: Let environments and lighting fill the entire frame.
- **Dynamic Transforms on GSAP Targets**: Never mix static CSS `transform` (like `scale` or `translate`) on elements animated by GSAP. Set initial states dynamically via `gsap.set()`.
- **Sub-Pixel Smooth Motion**: Always animate CSS transforms (`x`, `y`, `scale`, `rotation`, `opacity`) instead of layout properties (`left`, `top`, `width`) to prevent integer-pixel snapping.
- **Allow Intentional Overlaps**: Mark layering with `data-layout-allow-overlap` and background environments with `data-layout-allow-overflow`.

---

## 4. Authoring DON'Ts

1. **NO "Card inside Card" Dashboard UI**: No fake tech telemetry badges (`ACT-99`, `BANDWIDTH DIRECTIVE`), no floating UI windows.
2. **NO Repetitive Engineering Grids in a Black Void**: Avoid making every scene look like an AI SaaS landing page. Use real atmospheric gradients, materials, and lighting.
3. **NO Redundant Explanation Layers**: Do not have Voiceover + Headline + Diagram + Caption pill all repeating the identical phrase simultaneously.
4. **NO Captions at the Extreme Bottom**: Do not place text below Y = 1450px where platform chrome (Reels/Shorts/TikTok description and buttons) will obstruct it.
5. **NO Unverified / Fabricated Statistics**: Never invent fake percentages or metrics just to make an infographic look scientific.
6. **NO AI-Generated Images**: Strictly use authentic historical, scientific, or public domain archives (e.g. Wikimedia Commons, Library of Congress, museum archives, scientific micrographs).
7. **NO CSS pseudo-elements (`::before`/`::after`) as GSAP targets**: Target real DOM elements.
8. **NO Un-normalized Audio Mixing**: Never mix with default `amix` without `normalize=0`.

---

## 5. Camera, Safe Zones & Motion Architecture

### 5.1 Vertical Feed Safe Zones (9:16 Canvas · 1080×1920)
- **Top Unsafe Zone (0 – 300px)**: Platform search bars, audio pills, camera buttons.
- **Bottom Unsafe Zone (1450 – 1920px)**: User handle, caption text, sound tickers, right-side action buttons.
- **Center 1:1 Focal Square (Y = 420px to 1500px)**: The primary visual action zone.
- **Subtitles Placement**: Position subtitles at **`bottom: 480px` (Y ≈ 1350px–1440px)**, landing right on the lower third of the center square.

```css
.film-caption-block {
  position: absolute;
  bottom: 480px;
  left: 100px;
  right: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}

.caption-line {
  font-family: "Playfair Display", serif;
  font-size: 44px;
  font-weight: 700;
  line-height: 1.25;
  color: #F2F1EC;
  text-shadow: 0 4px 24px rgba(0, 0, 0, 0.9);
}

.caption-line .accent {
  color: #F2D24B;
  font-style: italic;
}
```

---

## 6. Audio & Narration Workflow

**THE GOLDEN RULE: Script → Audio → Visuals.**

1. **Write concise, visceral narration script** (1 short punchy sentence per shot).
2. **Generate & measure TTS audio**:
   ```bash
   pocket-tts generate --voice reference_clean.wav --text "..." --output-path out.wav
   ```
3. **Measure exact clip duration with `ffprobe`** and pad 0.3s pre-roll + 0.4s tail.
4. **Master audio to -14 LUFS**:
   ```bash
   ffmpeg -y -i clip1.wav -i clip2.wav ... -filter_complex "amix=inputs=N:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7" -ar 24000 -ac 1 narration_full.wav
   ```
5. **Sync master timeline duration** in `index.html` to the exact hundredth of a second.

---

## 7. Verification Gate — DONE IS RENDERED

Before presenting the result:
- [ ] `npm run check` passes with **0 errors, 0 warnings (100% WCAG AA contrast passing)**.
- [ ] Captions and visual focal points live within the **Optical Safe Zone** (`bottom: 480px` / Y = 325px–1440px).
- [ ] Voiceover is mastered at **-14.0 LUFS to -16.0 LUFS** with zero dead air.
- [ ] The composition is designed as a **continuous film of dynamic shots**, not a PowerPoint presentation.
- [ ] `npm run render` outputs a verified, playable MP4 file.
