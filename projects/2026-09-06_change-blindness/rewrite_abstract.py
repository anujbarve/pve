#!/usr/bin/env python3
"""
Complete rewrite of Change Blindness shots using ABSTRACT visual language.
NO stick figures, NO silhouettes, NO human anatomy.
Instead: color-coded identity aura orbs, geometric avatar tokens, data flows.
"""
import os

FRAMES_DIR = os.path.join(os.path.dirname(__file__), "compositions", "frames")

# ─────────────────────────────────────────────────────────────────────────────
# SHOT 01: The Door Experiment — identity tokens swap behind a passing barrier
# Person A = Cyan orb identity token. Stranger B = Amber orb identity token.
# The door = an opaque vertical slab sweeping across.
# ─────────────────────────────────────────────────────────────────────────────
SHOT_01 = '''<template>
  <style>
    @font-face { font-family: "Playfair Display"; font-style: normal; font-weight: 400 900; src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM86xQ.woff2) format("woff2"); }
    @font-face { font-family: "Inter"; font-style: normal; font-weight: 100 900; src: url(https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2) format("woff2"); }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #08090C; font-family: "Inter", sans-serif; color: #F2F1EC; }

    .bg-env {
      position: absolute; inset: -40px;
      background:
        radial-gradient(circle at 28% 55%, rgba(56,189,248,0.1) 0%, transparent 45%),
        radial-gradient(circle at 72% 55%, rgba(242,210,75,0.08) 0%, transparent 45%),
        linear-gradient(180deg, #0d1117 0%, #050609 100%);
    }
    .floor {
      position: absolute; bottom: 0; left: -120px; right: -120px; height: 860px;
      background: linear-gradient(180deg, transparent 0%, #0b0d14 100%);
      transform: perspective(1000px) rotateX(60deg);
      border-top: 1px solid rgba(255,255,255,0.06);
    }
    .floor-grid {
      position: absolute; inset: 0;
      background-image: linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
      background-size: 90px 90px;
    }

    /* INTERACTION STAGE */
    .stage { position: absolute; left: 90px; right: 90px; top: 560px; height: 600px; }

    /* IDENTITY TOKEN — circular orb with label */
    .identity-token {
      position: absolute; bottom: 0;
      display: flex; flex-direction: column; align-items: center; gap: 16px;
    }
    .token-orb {
      width: 110px; height: 110px; border-radius: 50%;
      position: relative; display: flex; align-items: center; justify-content: center;
    }
    .orb-core {
      width: 70px; height: 70px; border-radius: 50%;
    }
    .orb-ring1 { position: absolute; inset: -8px; border-radius: 50%; border: 1.5px solid; opacity: 0.5; }
    .orb-ring2 { position: absolute; inset: -20px; border-radius: 50%; border: 1px solid; opacity: 0.25; }
    .token-id {
      font-size: 12px; font-weight: 800; letter-spacing: 0.18em; text-transform: uppercase;
      padding: 6px 14px; border-radius: 6px; border: 1px solid;
    }

    /* Token A — Cyan (direction giver) */
    .token-a .orb-core { background: radial-gradient(circle, rgba(56,189,248,0.5) 0%, rgba(56,189,248,0.1) 60%, transparent 100%); box-shadow: 0 0 40px rgba(56,189,248,0.35); }
    .token-a .orb-ring1 { border-color: #38BDF8; }
    .token-a .orb-ring2 { border-color: #38BDF8; }
    .token-a .token-id { color: #38BDF8; border-color: rgba(56,189,248,0.4); background: rgba(4,12,28,0.9); }

    /* Token B1 — Amber/Gold (Stranger A, gets swapped out) */
    .token-b1 .orb-core { background: radial-gradient(circle, rgba(242,210,75,0.5) 0%, rgba(242,210,75,0.1) 60%, transparent 100%); box-shadow: 0 0 40px rgba(242,210,75,0.3); }
    .token-b1 .orb-ring1 { border-color: #F2D24B; }
    .token-b1 .orb-ring2 { border-color: #F2D24B; }
    .token-b1 .token-id { color: #F2D24B; border-color: rgba(242,210,75,0.4); background: rgba(16,12,4,0.9); }

    /* Token B2 — Red/Orange (Stranger B, totally different) */
    .token-b2 .orb-core { background: radial-gradient(circle, rgba(212,98,43,0.55) 0%, rgba(212,98,43,0.1) 60%, transparent 100%); box-shadow: 0 0 40px rgba(212,98,43,0.35); }
    .token-b2 .orb-ring1 { border-color: #D4622B; }
    .token-b2 .orb-ring2 { border-color: #D4622B; }
    .token-b2 .token-id { color: #D4622B; border-color: rgba(212,98,43,0.4); background: rgba(16,6,2,0.9); }

    /* CONVERSATION BEAM */
    .convo-beam {
      position: absolute; top: 200px; left: 150px; right: 150px; height: 4px;
      background: linear-gradient(90deg, #38BDF8 0%, rgba(56,189,248,0.3) 50%, #F2D24B 100%);
      box-shadow: 0 0 16px rgba(56,189,248,0.5);
    }
    .convo-pulse {
      position: absolute; top: -10px; left: 15%; width: 24px; height: 24px;
      border-radius: 50%; background: #38BDF8; box-shadow: 0 0 16px #38BDF8;
    }

    /* THE DOOR — opaque slab sweeping across */
    .door-slab {
      position: absolute; top: 0; bottom: 0; width: 200px;
      background: linear-gradient(90deg, #1a1e28 0%, #252a38 50%, #1a1e28 100%);
      border-left: 2px solid rgba(255,255,255,0.12); border-right: 2px solid rgba(255,255,255,0.12);
      box-shadow: 0 0 80px rgba(0,0,0,0.95);
      left: -250px; z-index: 10;
    }
    .door-label {
      position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
      writing-mode: vertical-rl; font-size: 11px; font-weight: 700; letter-spacing: 0.2em;
      color: rgba(255,255,255,0.2); text-transform: uppercase;
    }

    /* STUDY BADGE */
    .study-badge {
      position: absolute; top: 340px; left: 90px;
      background: rgba(10,14,22,0.9); border: 1px solid rgba(255,255,255,0.12);
      padding: 10px 18px; border-radius: 8px;
    }
    .badge-eyebrow { font-size: 10px; letter-spacing: 0.15em; color: #A0A09C; text-transform: uppercase; }
    .badge-title { font-size: 15px; font-weight: 700; color: #F2D24B; }

    .caption-block { position: absolute; bottom: 480px; left: 90px; right: 90px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 12px; }
    .caption-line { font-family: "Playfair Display", serif; font-size: 42px; font-weight: 700; line-height: 1.25; color: #F2F1EC; text-shadow: 0 4px 24px rgba(0,0,0,0.95); }
    .caption-line .accent { color: #F2D24B; font-style: italic; }
    .caption-sub { font-size: 17px; font-weight: 500; color: #A0A09C; letter-spacing: 0.12em; text-transform: uppercase; }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>

  <div id="root" data-composition-id="shot-01-door" data-width="1080" data-height="1920" data-duration="9.62">
    <div id="bg" class="bg-env" data-layout-allow-overflow></div>
    <div class="floor" data-layout-allow-overflow><div class="floor-grid"></div></div>

    <div class="study-badge" data-layout-allow-overlap>
      <div class="badge-eyebrow">Field Experiment</div>
      <div class="badge-title">Simons & Levin (1998)</div>
    </div>

    <div class="stage" data-layout-allow-overlap>
      <!-- Token A: Cyan (Direction Giver) — left -->
      <div id="token-a" class="identity-token token-a" style="left: 60px;">
        <div class="token-orb">
          <div class="orb-core"></div>
          <div class="orb-ring1"></div>
          <div class="orb-ring2"></div>
        </div>
        <span class="token-id">Identity A</span>
      </div>

      <!-- Conversation beam -->
      <div id="convo" class="convo-beam" data-layout-allow-overlap>
        <div id="pulse" class="convo-pulse"></div>
      </div>

      <!-- Token B1: Amber (Stranger A, original) — right -->
      <div id="token-b1" class="identity-token token-b1" style="right: 60px;">
        <div class="token-orb">
          <div class="orb-core"></div>
          <div class="orb-ring1"></div>
          <div class="orb-ring2"></div>
        </div>
        <span class="token-id">Stranger A</span>
      </div>

      <!-- Token B2: Red/Orange (Stranger B, replacement) — right, hidden initially -->
      <div id="token-b2" class="identity-token token-b2" style="right: 60px; opacity: 0;">
        <div class="token-orb">
          <div class="orb-core"></div>
          <div class="orb-ring1"></div>
          <div class="orb-ring2"></div>
        </div>
        <span class="token-id">Stranger B</span>
      </div>

      <!-- THE DOOR sweeping through -->
      <div id="door" class="door-slab" data-layout-allow-overlap>
        <span class="door-label">Loading Door</span>
      </div>
    </div>

    <div class="caption-block" data-layout-allow-overlap>
      <p id="cap" class="caption-line">You're giving directions to a stranger on the sidewalk...</p>
      <span id="sub" class="caption-sub">The Real-World Experiment</span>
    </div>
  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["shot-01-door"] = tl;

    const bg = document.getElementById("bg");
    const door = document.getElementById("door");
    const tokenB1 = document.getElementById("token-b1");
    const tokenB2 = document.getElementById("token-b2");
    const pulse = document.getElementById("pulse");
    const cap = document.getElementById("cap");
    const sub = document.getElementById("sub");

    gsap.set(door, { left: -250 });
    tl.to(bg, { scale: 1.04, duration: 9.62, ease: "none" }, 0);
    // Conversation pulse
    tl.to(pulse, { x: 580, duration: 2.0, repeat: 3, ease: "linear" }, 0);

    // Door sweeps across at 4.4s
    tl.to(door, { left: 1200, duration: 3.0, ease: "power1.inOut" }, 4.4);

    // Swap behind door at 6.0s
    tl.call(() => {
      cap.innerHTML = 'when a door passes — <span class="accent">swapping them with a total stranger</span>.';
      sub.innerText = 'The Swap (Simons & Levin 1998)';
    }, null, 5.0);
    tl.to(tokenB1, { opacity: 0, duration: 0.05 }, 6.0);
    tl.to(tokenB2, { opacity: 1, duration: 0.05 }, 6.0);
  </script>
</template>'''

# ─────────────────────────────────────────────────────────────────────────────
# SHOTS 02-05: Keep existing content (already abstract enough) but patch
# the profile-svg in shot-02 to be cleaner abstract head icons
# ─────────────────────────────────────────────────────────────────────────────

shots = {
    'shot-01-door.html': SHOT_01,
}

for filename, content in shots.items():
    path = os.path.join(FRAMES_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ Written: {filename}")

print("\n🎬 Change Blindness shot-01 rewritten with abstract identity orbs — no stick figures.")
