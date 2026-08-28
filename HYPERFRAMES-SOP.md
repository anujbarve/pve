# HyperFrames Master Video Standard Operating Procedure (SOP)

A comprehensive, production-tested manual for producing elite faceless short-form videos, visual essays, and explainer films.

---

## 🚨 THE CORE NON-NEGOTIABLES

1. **The Anti-PowerPoint Filmmaking Doctrine**: The fundamental unit of production is a **SHOT**, not a "card" or "slide". If 5 consecutive frames can be screenshotted and understood as a slide deck, **the video has failed**. Eliminate the "Card Prison" (floating rounded rectangles in a black void with engineering grids).
2. **Reality-First Hierarchy**: Always open with a visceral human experience or physical event in a full-bleed spatial environment. Conceptual animations and diagrams must emerge *directly from the physical geometry of the objects*, not as isolated UI widgets.
3. **The 3-Layer Audio & Sound Design Architecture**: Audio carries 50% of the video's bandwidth. Every film must feature three synchronized layers: **Foreground Voiceover (-14 LUFS) + Cinematic BGM Score (-22 dB) + Procedural Sound Design SFX (-14 dB to -20 dB)**.
4. **Canvas Standard (1080×1920 @ 60 FPS)**: Vertical 9:16 FHD at 60 FPS with full-bleed environments.
5. **Optical Safe-Zone Captions (`bottom: 480px`)**: Subtitles and core focal action MUST be positioned along the lower third of the 1:1 center square (**`bottom: 480px` / Y = 1350px–1440px**), completely immune to Instagram Reels, TikTok, and YouTube Shorts UI overlays.
6. **Zero Dead Air & Exact Timestamp Sync**: Timings are measured from the TTS engine with millisecond precision before authoring visuals.
7. **Date-Prefixed Folder Naming**: Project folders MUST follow the incrementing date format: `projects/YYYY-MM-DD_topic-name/` (e.g. `2026-08-28_predictive-processing`, `2026-08-29_chronostasis`, `2026-08-30_zeigarnik-effect`).

---

## 0. Project Structure & Naming Standard

Every video project lives in its own self-contained directory under `projects/`:
```
projects/
├── 2026-08-28_predictive-processing/
├── 2026-08-29_chronostasis/
├── 2026-08-30_zeigarnik-effect/
├── 2026-08-31_hyperbolic-discounting/
├── 2026-09-01_extended-mind/
└── 2026-09-02_decision-fatigue/
```
Each folder contains:
- `index.html` (Master timeline orchestrator)
- `generate_narration.py` (TTS synthesis & exact timing measurement)
- `generate_sound_design.py` (Procedural SFX, BGM score, and 3-layer mix)
- `compositions/frames/` (Full-bleed 1080×1920 shot compositions)
- `package.json` & `timings.json`
- `renders/` (Rendered output MP4)

---

## 1. Production Pipeline: Step-by-Step Order

```
┌─────────────────────────────────────────────────────────────┐
│ 1. SCRIPT AUTHORING (Punchy, Visceral, Shot-by-Shot)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. TTS GENERATION & DURATION MEASUREMENT (ffprobe / SRT)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. SOUND DESIGN & BGM SYNTHESIS (SFX Library + Score)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 4. 3-LAYER MASTER AUDIO MIXING (normalize=0, loudnorm=-14)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 5. VISUAL COMPOSITIONS (Full-Bleed HTML / GSAP Camera)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 6. VERIFICATION GATE (npm run check: 0 errors, 0 warnings)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 7. FINAL RENDER & MP4 EXPORT (npm run render)               │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. The 3-Layer Audio & Sound Design Standard

### Layer 1: Foreground Voiceover (Narration)
- **Standard**: 24 kHz mono WAV, mastered to **-14.0 LUFS to -16.0 LUFS** (integrated loudness) and **-1.0 dB true peak**.
- **Timing**: Add **0.3s pre-roll** and **0.4s tail** to each phrase. Measure exact durations with `ffprobe`.
- **Zero Dead Air**: Never hardcode arbitrary scene lengths. The visual timeline duration in `index.html` must match the master audio duration to the hundredth of a second.

### Layer 2: Cinematic Background Music (BGM Score)
- **Role**: Provides continuous emotional texture, harmonic warmth, and pacing so there is never dry, dead silence.
- **Mix Volume**: Mixed at **-22 dB to -24 dB** relative to the master voiceover.
- **Structure**:
  - *Act 1 (The Hook)*: Sparse, warm sub-drone bed (`D-minor` chord: 36.7Hz / 73.4Hz / 110Hz).
  - *Act 2 (The Fracture)*: Subtle 120 BPM heartbeat / sub-pulse kicks in.
  - *Act 3 (The Mechanism)*: Ethereal piano / glass arpeggio sequence enters the mid-range.
  - *Act 4 (The Glitch)*: High-frequency tension string / harmonic overtone.
  - *Act 5 (The Climax)*: Cinematic crescendo swell peaking during the final revelation, followed by a smooth 3-second fade out.

### Layer 3: Procedural Sound Design (SFX)
SFX hits are synchronized to the exact millisecond timestamps of on-screen physical and conceptual transformations:
- **Sub-Bass Impacts (`-14 dB`)**: Deep 90Hz → 32Hz exponential pitch drop on major camera pushes or revelation scenes.
- **Air Whooshes (`-18 dB`)**: Bandpass-filtered noise sweeps on fast camera movements, reach trajectories, or spatial matrix reveals.
- **Resonant Chimes / Shimmers (`-15 dB to -16 dB`)**: Multi-harmonic modal sines (880Hz, 1320Hz, 1760Hz) when phantom objects, predictions, or golden highlights materialize.
- **Digital Glitches / Zaps (`-15 dB`)**: Frequency-modulated chirps with amplitude gating when perceptual mismatches or errors occur.
- **Tactile Snaps / Clicks (`-16 dB to -18 dB`)**: High-frequency mechanical impulses (4.2kHz) on typographic infilling, reticle locks, or vector snaps.
- **Sonar / Radar Pings (`-20 dB`)**: Rhythmic harmonic pulses on expanding forward-model waves.

### Automated FFmpeg Mastering Filter:
```bash
ffmpeg -y \
  -i narration_full.wav \
  -i cinematic_bgm.wav \
  -i sfx_01.wav -i sfx_02.wav ... \
  -filter_complex "\
    [0:a]volume=1.0[voice];\
    [1:a]volume=0.0794[bgm];\
    [2:a]volume=0.1259,adelay=400|400[sfx1];\
    [3:a]volume=0.1585,adelay=4000|4000[sfx2];\
    [voice][bgm][sfx1][sfx2]amix=inputs=4:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[out]" \
  -map "[out]" -ar 24000 -ac 1 master_sound_design.wav
```
*(CRITICAL: `normalize=0` prevents FFmpeg `amix` from dividing audio by N inputs, and `loudnorm` locks broadcast loudness).*

---

## 3. The Anti-PowerPoint Filmmaking Doctrine

### What Fails the Anti-PowerPoint Test:
- Floating white/grey cards inside a black void.
- Faint engineering SaaS grids (`linear-gradient(rgba(255,255,255,0.03)...)`).
- Multiple redundant explanation layers (Voiceover says it + Headline repeats it + Diagram draws it + Pill captions it + Badge brands it).
- Fake corporate telemetry badges (`ACT-99`, `BANDWIDTH DIRECTIVE`, `COGNITIVE OVERRIDE`).
- Static photographs sitting passively inside rounded rectangles.

### The Shot-Based Standard:
Every shot must define:
1. **SUBJECT**: The central physical object, hand, text, or phenomenon.
2. **ENVIRONMENT**: Full-bleed spatial atmosphere (warm desk, ambient study, printed paper, spatial grid) filling the entire 1080×1920 canvas.
3. **ACTION**: A physical occurrence (reaching blindly, missing, freezing, sweeping, coalescing).
4. **CAMERA**: Physical lens dynamics (macro tracking, parallax angle shifts, push-ins, pull-backs).
5. **LIGHT**: Directional rim lighting, shadow contrast, depth of field.
6. **TRANSFORMATION**: Real-time visual evolution (empty air materializing a phantom wireframe, error vector connecting objects, expectation beam painting typos).
7. **PURPOSE**: Communicates the core insight before any typography is read.

---

## 4. Optical Safe Zones & Subtitles (`bottom: 480px`)

### The 1080×1920 Geometry:
- **Top Unsafe Zone (0 – 300px)**: Platform search bars, status icons, audio pills.
- **Bottom Unsafe Zone (1450 – 1920px)**: User handle, description text, audio marquee, like/comment/share buttons.
- **Center 1:1 Focal Square (Y = 420px to 1500px)**: The primary visual stage.
- **Subtitles Placement**: Anchored at **`bottom: 480px` (Y ≈ 1350px–1440px)**, sitting on the lower third of the center square.

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

.caption-sub {
  font-family: "Inter", sans-serif;
  font-size: 18px;
  font-weight: 500;
  color: #A0A09C;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
```

---

## 5. Technical Authoring DO's & DON'Ts

### DO:
- Give every timed element `data-start`, `data-duration`, `data-track-index`, and `class="clip"`.
- Pause and register all timelines on `window.__timelines`:
  ```js
  window.__timelines = window.__timelines || {};
  window.__timelines["composition-id"] = gsap.timeline({ paused: true });
  ```
- Animate transform properties (`x`, `y`, `scale`, `rotation`, `opacity`) instead of layout properties (`left`, `top`, `width`) to ensure sub-pixel motion.
- Set initial element states in GSAP using `gsap.set()` rather than mixing CSS `transform` rules in `<style>`.
- Mark intentional layering with `data-layout-allow-overlap` and background containers with `data-layout-allow-overflow`.

### DON'T:
- **NO AI-Generated Images**: Use authentic historical, archival, or scientific media (e.g. Wikimedia Commons, Library of Congress, museum archives, scientific micrographs).
- **NO CSS Pseudo-elements (`::before`/`::after`) as GSAP targets**: Always target real DOM elements.
- **NO Non-deterministic Logic**: Never use `Date.now()`, `Math.random()`, or network fetches in compositions.
- **NO Fabricated Numbers**: Never invent unverified percentages or metrics to decorate a scene.

---

## 6. Verification Gate — DONE IS RENDERED

Before declaring any video complete:
- [ ] **Linter & Motion Check**: `npm run check` passes with **0 errors, 0 warnings, and 100% WCAG AA contrast**.
- [ ] **Audio Loudness**: Master soundtrack meets **-14.0 LUFS to -16.0 LUFS** with zero clipping.
- [ ] **Sound Design Check**: Background music sits warmly at `-22 dB`; SFX hits land on the exact visual transformation frames.
- [ ] **Safe-Zone Check**: Captions are anchored at `bottom: 480px`, clear of all platform UI chrome.
- [ ] **Filmmaking Litmus Test**: The video operates as a continuous shot-by-shot film, not a PowerPoint slide deck.
- [ ] **Render Verification**: `npm run render` completes successfully and the final MP4 plays back cleanly.
