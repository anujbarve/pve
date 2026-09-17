# The Simplicity Doctrine: Minimal Black & White Standard
*(Jack Butcher / Visualize Value / Naval Ravikant Philosophy)*

> *"Design is thinking made visual. Strip away the unnecessary so that the necessary may speak."*

---

## 1. The Core Philosophy

No visual fuss. No decorative clutter. No PowerPoint cards. No fake stock photography.

When explaining psychology, human behavior, and philosophical truths, visual noise is the enemy of comprehension. The viewer's mind must not be distracted by complex 3D renders, broken SVG paths, drop shadows, or gradient cards. 

Every shot must be a **singular, undeniable mental model** constructed entirely from **pure geometric primitives**:
- A circle represents unity, a boundary, or a whole.
- A line represents a trajectory, a connection, or a threshold.
- A box represents a state, a routine, or a category.
- Bold typography delivers the truth with crystalline clarity.

---

## 2. Visual Specification

### Color Palette (Strictly Monochromatic)
| Role | Hex | Purpose |
|---|---|---|
| **Canvas Background** | `#000000` | Pure, absolute void. Zero gradients, zero background patterns. |
| **Primary Geometry & Text** | `#FFFFFF` | Razor-sharp crisp lines, active states, and primary headlines. |
| **Secondary Metadata** | `#888890` | Sub-labels, inactive states, metric units, category tags. |
| **Dimmed / Disconnected** | `#444450` | Severed connections, crossed-out states, disabled options. |

*(No accent colors unless explicitly instructed. The power comes from pure contrast.)*

### Typography (Swiss Modern Grotesk)
- **Primary Font Family**: `Inter`, sans-serif.
- **Headlines / Statements**: `font-size: 48px - 64px`, `font-weight: 900`, `letter-spacing: 0.05em - 0.1em`, uppercase.
- **Diagram Labels**: `font-size: 16px - 22px`, `font-weight: 800`, `letter-spacing: 0.18em - 0.25em`, uppercase.
- **Subtitles / Captions**: `font-size: 32px`, `font-weight: 700`, `letter-spacing: -0.01em`, sentence case, centered at **`bottom: 480px`**.

---

## 3. The Primitives-Only Rule (Zero Glitches)

🔒 **NEVER USE COMPLEX HAND-DRAWN SVG PATHS OR WEIRD ROTATION ORIGINS.**
Browser rendering engines and headless capture workers can glitch on complex transform origins. Build every diagram using rock-solid CSS primitives:

1. **Circles**:
   ```css
   .circle {
     width: 480px;
     height: 480px;
     border: 3px solid #FFFFFF;
     border-radius: 50%;
   }
   ```
2. **Frames / State Boxes**:
   ```css
   .box {
     width: 760px;
     height: 120px;
     border: 3px solid #FFFFFF;
     background: #050505;
   }
   ```
3. **Connecting Wires & Circuit Lines**:
   ```css
   .line {
     height: 4px;
     background: #FFFFFF;
     flex: 1;
   }
   ```
4. **Horizontal Capacity & Progress Bars**:
   ```css
   .capacity-bar {
     width: 100%;
     height: 70px;
     border: 4px solid #FFFFFF;
     padding: 6px;
   }
   .capacity-fill {
     height: 100%;
     background: #FFFFFF;
   }
   ```
5. **Circuit Breaks & Disconnections**:
   Instead of rotating a diagonal stick, open a clean gap in the middle of a flexbox line:
   ```css
   .wire-gap { width: 120px; }
   ```
6. **Strikes & Cross-Outs**:
   Use a clean horizontal bar slicing through the text:
   ```css
   .strike-bar {
     position: absolute;
     top: 50%;
     left: -8px;
     right: -8px;
     height: 4px;
     background: #FFFFFF;
   }
   ```

---

## 4. Audio Architecture: Voice-First & Meditative

The audio must match the visual purity: **intimate, grounded, and uncluttered**.

### Layer 1: Foreground Voiceover (-14.0 LUFS)
- **100% Upfront & Intimate**: The vocal is dry, warm, and conversational.
- **Cadence**: Unhurried, stoic, authentic. Zero artificial hype or fake radio-host enthusiasm.
- **Mastering**: Broadcast standard **-14.0 LUFS** with `-1.0 dB` true peak.

### Layer 2: Meditative Ambient Piano / Drone (-19.0 dB)
- **Role**: Provides emotional depth and a calming harmonic cushion without competing with voice frequencies.
- **Sound**: Slow, breathing ambient piano chords (e.g. Ólafur Arnalds / Brian Eno style) and a warm analog sub-drone.
- **Mix Level**: Mixed quietly at **-19.0 dB** relative to narration. Completely leaves the vocal range (500Hz - 4kHz) transparent and clean.

### Layer 3: Prominent Tactile SFX (-10 dB to -13 dB)
- **Role**: Satisfying physical audio feedback when lines draw, concepts resolve, and switches break.
- **Sound Palette**:
  - `tactile_click.wav` (`-10 dB`): Clean drafting pen click on diagram entrances.
  - `switch_snap.wav` (`-8 dB to -10 dB`): Crisp mechanical switch snap on circuit breaker trips and state shifts.
  - `pen_draw.wav` (`-11 dB to -12 dB`): Soft friction scrape when vectors and lines expand.
  - `sub_swell.wav` (`-12 dB to -13 dB`): Warm 50Hz sine swell on major conceptual realizations.
- **Strict Prohibition**: **ZERO chaotic drum beats, zero 8-bit digital bleeps, zero loud techno tracks.**

---

## 5. Mental Model Storyboarding Guide

Every shot must visually prove the sentence being spoken:

| Spoken Concept | Visualize Value Mental Model |
|---|---|
| **Voice in Head vs Reality** | Large circle (`YOUR LIFE`) containing a tiny 0.01% pulsating point (`THE VOICE`). |
| **The Comparison Trap** | Others running in an endless circular loop vs your single straight vector. |
| **Masking / Depletion** | `PHYSICAL ROUTINE: 100% [PRESENT]` vs `EMOTIONAL ENERGY: 0% [EMPTY]`. |
| **Overload / Redlining** | Horizontal progress frame filling past a threshold limit into `100% [REDLINE]`. |
| **Biological Shutdown** | A circuit wire snapping open in the middle (`INPUT` disconnected from `OUTPUT`). |
| **Worth ≠ Productivity** | `[ HUMAN WORTH (∞) ]`  ≠  `[ 24-HOUR OUTPUT ]`. |
| **Ceasefire / Peace** | Two colliding arrows rotating into parallel upward alignment (`PEACE`). |

---

## 6. Verification Checklist

Before rendering any video in this style:
- [ ] **Background**: 100% pitch black `#000000` (no gradients, no grids, no photos).
- [ ] **Geometry**: Built exclusively from pure CSS circles, boxes, straight lines, and progress frames.
- [ ] **Zero Glitches**: No detached SVG transform origins or flying elements.
- [ ] **Safe Zone**: Captions and key text anchored at **`bottom: 480px`**.
- [ ] **Voice Clarity**: Voiceover is 100% crystal clear at **-14.0 LUFS**.
- [ ] **Score**: Meditative ambient piano at **-19.0 dB**.
- [ ] **Tactile Audio**: Mechanical switch snaps and pen clicks are crisp and prominent.
- [ ] **HyperFrames Check**: `npm run check` passes with **0 errors, 0 warnings, 100% WCAG AA contrast**.
