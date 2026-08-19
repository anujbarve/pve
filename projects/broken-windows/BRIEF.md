---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "A broken window isn't just damage — it's a signal. Ignore the small stuff, and the big stuff follows."
destination: shorts
aspect: 1080x1920
language: en
audience: vertical-feed scroll audience (Reels/Shorts)
length: 35s
angle: concept
narration: yes
---

## Intent

Broken Windows Theory reel in the "Editorial Dark Mode" series. Hook → Origin → Mechanism → Example → Reframe → Bigger Lesson arc. Core reframe: a broken window isn't just damage — it's a social signal that invites more disorder. The real lesson extends to life: small things you ignore tell people what you'll tolerate. Conversational, teacher-to-friend, quotable ending.

## Assets

None — faceless, typographic visuals. Voice clone narration (same reference as Occam's Razor).

## Customizations

- Anuj-style.md (Editorial Dark Mode) is the design spec: full-bleed `#000000`, Playfair Display Bold key lines / Inter narration body, `#F2D24B` mustard accent (max 1 per frame), `#F2F1EC` off-white primary, `#8A8A8A` muted.
- Recurring UI: top-right swipe arrow (black pill, white →), bottom-left `anujb.sh` signature + thin rule, load-bearing 1px divider rules, progressive word reveals (gray → white/yellow).
- Asymmetric layout; dead-centering only on closing frame (06-lesson) and reframe (05-reframe).
- 6 frames, ~35s total, with synced narration audio.

## Sync Strategy

Audio-visual sync is handled by `generate_narration.py`:
- Each frame has a `reveal_offset` — the timestamp (in seconds into the frame) when the text starts appearing.
- TTS audio is delayed by that offset using `adelay`, so speech starts exactly when text appears.
- Each frame's audio is trimmed/padded to fit within its duration.
- All frame audio is mixed onto a master timeline at their correct start positions using `amix`.
