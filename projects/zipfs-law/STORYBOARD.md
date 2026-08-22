---
format: 1080x1920
duration: 59.21s
fps: 60
message: "Zipf's Law isn't just about grammar — it's a universal power law governing language, cities, and wealth. Master the head of the curve."
arc: Hook (Word Frequency Anomaly) → Origin (1935 Harvard Discovery) → Mechanism (1/r Power Law) → Universal Cascade (Cities & Networks) → Reframe (Principle of Least Effort) → Lesson (The Asymmetry Advantage)
audience: vertical-feed scroll audience (Instagram Reels / YouTube Shorts / TikTok)
style: Editorial Dark Mode per Anuj-style.md
assets: Archival photographic assets + SVG graphics + 3D cards + frosted dynamic captions
narration: Pocket-TTS voice clone with dynamic subtitle pill captions
---

# Zipf's Law — The Hidden Power Law Governing Everything (1080p 60s Vertical)

**This explainer reel reveals to the viewer that human language, world city sizes, website traffic, and wealth distribution are all controlled by the exact same mathematical code: Zipf's Law.**

---

## 🎨 Visual Direction & Design Grammar

- **Palette System:**
  - Background: Full-bleed `#000000` pure black with subtle `60px` grid (`rgba(242, 241, 236, 0.03)`).
  - Primary Typography: Crisp off-white `#F2F1EC` / `#EAE6DF`.
  - Hero Accent: Mustard Gold `#F2D24B` (the primary focal highlight in each frame).
  - Warning / Critical Accent: Amber Orange `#D4622B` (for critical thresholds and extreme ranks).
  - Muted Secondary: `#A0A09C` / `#8A8A8A` for kickers, rank labels, and secondary details.
  - Card Surfaces: `rgba(242, 241, 236, 0.03)` with `1px solid rgba(242, 241, 236, 0.15)`.

- **Typography Stack:**
  - **Display / Punchlines:** *Playfair Display Bold (700 / 900)* (55px – 130px) for headlines, hero words, and quote manifesto.
  - **Display Accent:** *Playfair Display Bold Italic* (45px – 60px) for emotional lead-ins and voice emphasis.
  - **Interface / Captions / Data:** *Inter (Grotesk Sans-Serif)* (16px – 22px for kickers/badges; 25px – 28px for dynamic subtitle captions).

- **Optical Safe-Zone Layout Pattern:**
  - Centered strictly between **Y = 325px and Y = 1425px** inside `.frame-container` > `.safe-zone` (`max-width: 920px`, `padding: 0 70px`).
  - Zero collision with top Reels chrome (0–300px) or bottom Reels ticker/actions (1450–1920px).

- **Dynamic Frosted Subtitle Pills:**
  - Subtitle pills anchored directly below the central content block (`margin-top: 20px–30px`).
  - Frosted dark glass: `rgba(18, 18, 18, 0.90)`, `backdrop-filter: blur(20px)`, border `rgba(242, 241, 236, 0.15)`.
  - Synchronized phrase swapping with `<span class="cap-hl">` gold highlights matching vocal cues.

---

## 🎬 Frame-by-Frame Storyboard Breakdown

### Frame 1 — The 7% "THE" Anomaly (Hook)
- **Duration:** 10.76s (Start: 0.00s, Overlap: 0.50s)
- **Source:** `compositions/frames/01-hook.html`
- **Narrative Role:** Hook the audience with an astonishing statistic about everyday human speech.
- **Narration Audio:**
  > *"The most common word in English is the. It accounts for seven percent of everything spoken. Why does this rule govern language?"*

---

### Frame 2 — The Harvard Discovery (Origin)
- **Duration:** 8.76s (Start: 10.26s, Overlap: 0.50s)
- **Source:** `compositions/frames/02-origin.html`
- **Narrative Role:** Ground the phenomenon with historical authority and the original researcher.
- **Narration Audio:**
  > *"In nineteen thirty-five, Harvard linguist George Kingsley Zipf uncovered a bizarre mathematical pattern across millions of texts."*

---

### Frame 3 — The Power Law Formula (Mechanism)
- **Duration:** 12.44s (Start: 18.52s, Overlap: 0.50s)
- **Source:** `compositions/frames/03-mechanism.html`
- **Narrative Role:** Explain the mathematical mechanics of $f(r) \propto 1/r$ with step-down visual waterfall data.
- **Narration Audio:**
  > *"Rank every word by frequency. The second appears half as often. The tenth, one-tenth. An unbroken power law."*

---

### Frame 4 — Cross-Domain Cascade (Universal Invariance)
- **Duration:** 9.48s (Start: 30.46s, Overlap: 0.50s)
- **Source:** `compositions/frames/04-cascade.html`
- **Narrative Role:** Expand beyond linguistics to show universality across city sizes, internet traffic, and wealth.
- **Narration Audio:**
  > *"The same law dictates city populations, website traffic, earthquakes, and wealth. Nature repeats this code."*

---

### Frame 5 — The Principle of Least Effort (Reframe)
- **Duration:** 9.80s (Start: 39.44s, Overlap: 0.50s)
- **Source:** `compositions/frames/05-reframe.html`
- **Narrative Role:** Unpack the cognitive equilibrium: speaker brevity vs. listener clarity.
- **Narration Audio:**
  > *"Why? The Principle of Least Effort. The human brain balances minimal speaker effort against maximum listener clarity."*

---

### Frame 6 — Master The Head of the Curve (Lesson / Closer)
- **Duration:** 10.92s (Start: 48.74s, Overlap: 0.50s, Total: 59.21s)
- **Source:** `compositions/frames/06-lesson.html`
- **Narrative Role:** Deliver the high-status actionable takeaway.
- **Narration Audio:**
  > *"The takeaway? A tiny fraction of inputs controls the vast majority of outcomes. Master the head of the curve, master the game."*

---

## 📊 Technical Verification Summary

- **Standard:** 1080p vertical (`1080×1920`), 60 FPS, 59.21s master duration
- **Linter Check:** `0 errors, 0 warnings`
- **Runtime Execution:** `0 errors, 0 warnings`
- **Layout & Safe Zones:** `0 collisions, fully contained within Y = 325px – 1425px`
- **WCAG Contrast:** `45/45 checks passed (100% WCAG AA)`
- **Audio Sync:** Exact frame-by-frame TTS speech timing via Pocket-TTS
- **Render Output:** `renders/zipfs-law/` (1080p 60 FPS MP4)
