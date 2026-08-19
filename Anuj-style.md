# Content Style Guide
### "Editorial Dark Mode" — reel/carousel visual system

This is the reusable spec for the visual identity seen across the Miller's Law series, One Percent Rule reel, and future pieces. Treat this as the source of truth when designing new frames.

---

## 1. Canvas & Format

- **Aspect ratio:** 9:16 (vertical, Reels/Shorts native) — e.g. `1080x1920`, video export at `1920x1080`→ letterboxed or native vertical depending on platform
- **Background:** `#000000` pure black, edge to edge, always
- **Safe margins:** keep text ~80–100px in from left/right edges; don't let type touch the frame edge
- **One idea per frame.** Never stack two punchlines on one screen.

---

## 2. Typography

### Primary typeface — Playfair Display
- **Playfair Display Bold** — the "big idea" font. Used for:
  - Headlines / titles ("The One Percent Rule")
  - The punchline or key term on any given slide ("Miller's Law", "That's chunking.")
  - The final "quotable" takeaway line at the end
- **Playfair Display Bold Italic** — used for setup/emotional lines that lead into the punch ("Your brain doesn't have a '7-item' memory.") — italic = "voice," upright bold = "the fact"
- Never use Playfair for long body copy — it's a display face, only for short punchy lines (≤ 8–10 words per line)

### Secondary typeface — clean grotesk sans-serif
- (Matches Inter / Helvetica Neue / SF Pro territory)
- Used for:
  - Setup/context lines ("You've probably heard")
  - Supporting/explainer text ("is more interesting than that.")
  - Small captions, labels, the signature line
- Regular or Medium weight — never bold, so it stays visually subordinate to the Playfair lines
- This is the "narrator's voice" font — quieter, more neutral

### Hierarchy rule of thumb
1. Sans-serif regular = setup / narration
2. Playfair Bold Italic = transitional or emphatic line
3. Playfair Bold (largest size on the frame) = the one thing you want remembered
4. Sans-serif small/gray = footnotes, captions, source credit, signature

---

## 3. Color Palette

| Role | Hex (approx) | Usage |
|---|---|---|
| Background | `#000000` | Always full-bleed black |
| Primary text | `#F2F1EC` (off-white, not pure white) | Setup lines, body/explainer text |
| Accent / key term | `#F2D24B` (warm mustard yellow) | The ONE thing per frame you want to pop — never more than 1–2 accent elements per screen |
| Muted / secondary | `#8A8A8A` (mid-gray) | Signature text, dividers, de-emphasized words in progressive reveals |

**Rule:** Yellow is scarce. It marks the single most important word, number, or phrase on screen. If everything is yellow, nothing is.

---

## 4. Layout Patterns (Page Types)

Every frame in the series falls into one of these templates:

### A. Title/Hook Frame
- Large mixed-weight title (e.g. "The **One Percent Rule**")
- Small sans-serif word above ("The") and below ("Rule") the bold Playfair centerpiece — creates scale contrast on one line-group
- Supporting image(s) layered behind/beside at low opacity or partial-frame crop (historical photo, diagram thumbnail) — always secondary to type
- Subtle animated background texture (thin jagged lines) for movement in video

### B. Setup → Punch Frame
- Top: sans-serif line, left- or right-aligned (asymmetric, never centered)
- Below: Playfair Bold Italic line continuing the thought
- Below that: Playfair Bold (yellow) — the term/concept, largest text on the frame
- Optional: sans-serif closer line beneath in white ("is more interesting than that.")

### C. Data-as-Graphic Frame
- A number, sequence, or stat rendered AS the visual — huge Playfair Bold, yellow, often with em-dashes or slashes as separators (e.g. `7—2—9—4—1—8—6—3`, `729 / 418 / 63`)
- No chart/graph needed — the typography of the number IS the diagram
- Small sans-serif caption above or below for context

### D. Reference/Proof Frame
- Embeds an external diagram or image (hand-drawn sketch, chart, screenshot) in a bordered card, drop-shadowed, slightly rotated or offset — never edge-to-edge
- Caption in sans-serif below or beside, continuing the sentence started on the previous frame ("is not a little bit of...")
- Attribution preserved if visible (e.g. "JamesClear.com") — keep sources honest

### E. Closing/Lesson Frame
- Vertically centered block, tightly stacked
- White Playfair Italic setup ("The bigger lesson:")
- Yellow Playfair Bold payoff, largest text of the whole sequence ("Organize information better.")
- Thin horizontal rule lines above and below the block for isolation/emphasis
- This is the frame most likely to be screenshotted — make it stand alone

---

## 5. Recurring UI/Brand Elements

- **Top-right swipe arrow:** small black pill with a white right-arrow (→), consistent position across every frame — signals "more" / next slide
- **Bottom-left signature:** `anujb.sh` in small gray sans-serif, paired with a thin horizontal rule extending right — quiet, consistent, never resized
- **Divider rules:** 1px light-gray horizontal lines used to separate sections within a frame or mark a "breath" before the next beat — not decorative, always load-bearing (signals a shift in thought)
- **Progressive text reveal (video only):** within one line, words fade from gray → white/yellow as they're "spoken," creating emphasis without cutting to a new frame

---

## 6. Copywriting Rules (so design and words stay in sync)

- **One claim per frame.** If a frame needs a comma to explain itself, split it.
- **Hook → Myth-bust → Reframe → Bigger Lesson** is the default arc. Every piece should be reducible to this shape.
- Address the viewer directly ("You've probably heard...") — conversational, teacher-to-friend, not academic
- End on a reframed principle, not a summary — the last frame should feel quotable on its own, out of context
- Keep sentence fragments short enough to read in under 2 seconds at a glance

---

## 7. Quick Build Checklist (per frame)

- [ ] Black background, no exceptions
- [ ] One dominant idea, ≤ 2 text blocks
- [ ] Playfair Bold for the "keep this" phrase, sans-serif for everything else
- [ ] Yellow used on ONE element max
- [ ] Asymmetric alignment (avoid dead-centering unless it's the closing frame)
- [ ] Swipe arrow (top-right) + signature (bottom-left) present, unless it's a full-bleed hook/title frame
- [ ] Text has breathing room — no block touches frame edges