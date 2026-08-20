# Content Style Guide
### "Editorial Dark Mode" — Explainer Reel & Motion Graphics Visual System

This is the reusable design and motion spec for the Editorial Dark Mode series (Broken Windows Theory, The 1% Rule, Miller's Law, and future projects). Treat this as the canonical source of truth for video and motion graphics authoring.

---

## 1. Canvas & Safe Zones (Vertical Reels / Shorts)

- **Native Resolution:** `2160×3840` (4K vertical 9:16) or `1080×1920` (FHD vertical).
- **Background:** `#000000` pure black, edge-to-edge, with subtle background grid (`rgba(242, 241, 236, 0.03)` 120px cells).
- **Platform Safe Zone Clearance:**
  - **Top Unsafe Zone (0 – 600px):** Platform search bars, audio pills, camera buttons, status bars.
  - **Bottom Unsafe Zone (2900 – 3840px):** User handles, captions, sound tickers, right-rail actions (like/comment/share/remix).
  - **The Golden Safe Window:** All core graphics, typography, and subtitle pills MUST live comfortably between **Y = 650px and Y = 2850px**.
- **Layout Rule:** NEVER use `justify-content: space-between` to spread elements from top to bottom of the 3840px canvas. Always use a vertically centered `.frame-container` holding an inner `.safe-zone` wrapper (`max-width: 1840px`).

```css
.frame-container {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 160px;
}

.safe-zone {
  width: 100%;
  max-width: 1840px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
```

---

## 2. Typography Hierarchy

### Primary Typeface — Playfair Display
- **Playfair Display Bold (700 / 900):** The hero concept font.
  - Giant Display / Year figures (`280px – 340px`)
  - Scene Headlines (`110px – 160px`)
  - Stamped theory titles & punchlines
- **Playfair Display Bold Italic:** Used for voice, quotes, and emotional lead-ins (`90px – 120px`).
- **Emphasis rule:** Never use Playfair for dense body text; reserve it for high-impact headlines and quotable statements.

### Secondary Typeface — Inter (Grotesk Sans-Serif)
- **Inter Semi-Bold / Bold (600 / 700):** Kicker badges, category tags, step numbers, and CTA button text (`32px – 54px`, `letter-spacing: 0.12em – 0.24em`, uppercase).
- **Inter Regular / Medium (400 / 500):** Sub-leads, author titles, footnotes, and dynamic subtitle captions (`44px – 60px`).

---

## 3. Color Palette

| Role | Hex Code | Usage |
|---|---|---|
| Background | `#000000` | Full-bleed pure black |
| Primary Text | `#F2F1EC` / `#EAE6DF` | Headlines, punchlines, active text |
| Key Accent | `#F2D24B` (Mustard Gold) | The ONE hero idea/word per frame, active subtitles, glowing badges |
| Warning / Critical Accent | `#D4622B` (Amber Orange) | Critical thresholds, strike-through bars, collapse cards |
| Muted Secondary | `#A0A09C` / `#8A8A8A` | Category kickers, supporting details, inactive states |
| Card Surface | `rgba(242, 241, 236, 0.03)` | Card containers with `2px solid rgba(242, 241, 236, 0.15)` border |

---

## 4. Motion Graphics Architecture (No "Glorified PPT")

Avoid repetitive slide templates across consecutive scenes. Every scene must have a distinct narrative-driven graphic prop:

1. **Frame 1 — Hook / Prop Frame:**
   - Visual SVG Prop (e.g. window pane with animated `stroke-dashoffset` fracture crack lines).
   - Headline with gold italic highlight + curiosity callout card (`What if one crack could change everything?`).
2. **Frame 2 — Archival / Origin Frame:**
   - 3D oversized year digits (`1982`) with floating drift.
   - Dual researcher cards with `rotateY` perspective tilt.
   - Gold-stamped theory seal.
3. **Frame 3 — Mechanism / Insight Frame:**
   - Radar shockwave beacon with concentric pulsating SVG circles + glowing amber center dot.
   - High-contrast broadcast cards (`[ BROADCAST 01 ] "Nobody is watching"`).
4. **Frame 4 — Escalation / Cascade Frame:**
   - Progressive domino staircase (`01` → `02` → `10`) stepping in on vocal cues.
   - Full-width amber critical threshold warning banner (`Then the whole block falls apart`).
5. **Frame 5 — Reframe / Duality Frame:**
   - Struck-through dashed card with red laser bar (`The Physical Glass [ NOT THE PROBLEM ]`).
   - Luminous gold hero card (`THE REAL PHENOMENON: It's about the signal it sends`).
6. **Frame 6 — Manifesto / Closer Frame:**
   - Luxury double-bordered manifesto box with gold quote text.
   - Dual actionable pill buttons (`01 · Fix The Signal`, `02 · Change The Story`).

---

## 5. Smooth Dynamic Captions System

In vertical video reels, subtitles should be anchored directly below the central content block:

```html
<div class="caption-wrapper" data-layout-allow-overlap>
  <div id="f01-pill" class="caption-pill">
    <span id="f01-caption" class="caption-text">You walk past a broken window every day.</span>
  </div>
</div>
```

```css
.caption-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 60px;
}

.caption-pill {
  background: rgba(18, 18, 18, 0.88);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(242, 241, 236, 0.15);
  border-radius: 999px;
  padding: 24px 60px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
  max-width: 1760px;
}

.caption-text {
  font-family: "Inter", sans-serif;
  font-size: 54px;
  font-weight: 600;
  color: #F2F1EC;
  letter-spacing: 0.02em;
  text-align: center;
}

.cap-hl {
  color: #F2D24B;
  font-weight: 800;
}
```

---

## 6. Build Checklist (Before Render)

- [ ] Canvas is vertical (`2160×3840` or `1080×1920`) with full-bleed `#000000` background.
- [ ] No elements in Top Unsafe Zone (0–600px) or Bottom Unsafe Zone (2900–3840px).
- [ ] Visual props and typography are centered inside `.safe-zone`.
- [ ] Subtitle pill sits directly below main content.
- [ ] No fake header/footer bars that collide with platform feed UI.
- [ ] Authentic Assets Only: Zero AI-generated images. Strictly real historical, scientific, archival, or documentary visuals.
- [ ] `npm run check` passes with 0 errors, 0 warnings, and 100% WCAG AA contrast.