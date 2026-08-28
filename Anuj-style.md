# Content Style Guide
### "Editorial Dark Mode" — The Filmmaking Visual System

This is the design and motion specification for cinematic explainer films and visual essays. Treat this as the canonical source of truth for all video authoring.

---

## 1. Canvas & Optical Safe Zones (Vertical Reels / Shorts)

- **Native Standard Resolution:** `1080×1920` (FHD vertical 9:16, 60 FPS).
- **Environment:** Full-bleed spatial environment occupying the entire 1080×1920 frame. No black voids containing tiny floating cards.
- **Platform Safe Zone Clearance:**
  - **Top Unsafe Zone (0 – 300px):** Platform search bars, audio pills, camera buttons.
  - **Bottom Unsafe Zone (1450 – 1920px):** User handles, captions, sound tickers, right-rail actions (like/comment/share/remix).
  - **Center 1:1 Focal Square (Y = 420px to 1500px):** The primary visual stage.
  - **Captions Anchor:** Subtitles must sit at **`bottom: 480px` (Y ≈ 1350px–1440px)**, directly along the lower third of the center square (immune to all platform UI overlays).

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

## 2. Typography Hierarchy

### Primary Typeface — Playfair Display
- **Playfair Display Bold (700 / 900):** Hero cinematic statements and display titles (`55px – 76px`).
- **Playfair Display Bold Italic:** Accents, voice emphasis, and evocative phrase anchors.

### Secondary Typeface — Inter (Grotesk Sans-Serif)
- **Inter Semi-Bold / Bold (600 / 700):** Spatial labels, HUD coordinate markers (`13px – 16px`, `letter-spacing: 0.15em – 0.25em`, uppercase).
- **Inter Regular / Medium (400 / 500):** Sub-leads and secondary subtitles (`18px – 22px`).

---

## 3. Color Palette

| Role | Hex Code | Usage |
|---|---|---|
| Deep Space / Shadow | `#080808` / `#0D0D0D` | Cinematic atmosphere and ambient gradient bases |
| Primary Text | `#F2F1EC` | Main dialogue, titles, clear text |
| Key Accent | `#F2D24B` (Warm Gold) | Phantom predictions, expectation beams, hero emphasis |
| Warning / Error Accent | `#D4622B` (Amber Orange) | Error vectors, discrepancy reticles, critical surprises |
| Muted Secondary | `#A0A09C` | Contextual subtitles, inactive coordinate lines |

---

## 4. The Anti-PowerPoint Motion Architecture

1. **Shot 01 — The Human Experience Entry Point:**
   - Full-bleed physical or environmental event (e.g. reaching for an object, closing a book, walking past an obstacle).
   - Metaphor: A phantom expectation or wireframe emerges directly from the physical point of interaction.
2. **Shot 02 — The Spatial Fracture / Mismatch:**
   - Lens push-in or parallax pan revealing the discrepancy between reality and prediction.
   - An active vector or light sweep measures the error signal.
3. **Shot 03 — The Internal Projection Engine:**
   - Seamless camera push into the spatial matrix (3D ray-traced grid, expanding wave cones).
   - Metaphor: Shows that the brain projects reality outward rather than passively receiving it.
4. **Shot 04 — The Physical Glitch (Typo / Blind Spot):**
   - Macro focus on a physical medium (e.g. printed paper, textured surface) with a visible flaw.
   - The brain's expectation light sweep actively paints over the flaw in real time.
5. **Shot 05 — The Synthesis / Calibration:**
   - Wide cinematic pull-back coalescing all simulation rays into tangible physical reality.
   - Minimalist, integrated manifesto title embedded directly into the environment.

---

## 5. Build Checklist (Before Render)

- [ ] Canvas is standard vertical `1080×1920` @ 60 FPS with full-bleed atmospheric lighting.
- [ ] **No Card Prisons**: Environments fill the frame; objects and animations live in real space, not in floating boxes.
- [ ] Subtitles sit at **`bottom: 480px`** (lower third of 1:1 center square), safe from platform UI.
- [ ] Master voiceover is mastered at **-14.0 LUFS to -16.0 LUFS** with `normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7`.
- [ ] `npm run check` passes with **0 errors, 0 warnings, and 100% WCAG AA contrast**.