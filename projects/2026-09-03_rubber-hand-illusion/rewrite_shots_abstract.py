#!/usr/bin/env python3
"""
Complete rewrite of ALL 5 rubber hand illusion shots using ABSTRACT visual language.
NO hands, NO fingers, NO anatomy.
Instead: glowing sensor pads, haptic field rings, waveform binding arcs, biometric reticles.
"""
import os

FRAMES_DIR = os.path.join(os.path.dirname(__file__), "compositions", "frames")

# ─────────────────────────────────────────────────────────────────────────────
# SHOT 01: The Setup — Two sensor pads on either side of a partition
# Real hand = left cyan sensor pad (occluded, ghosted)
# Rubber hand = right amber sensor pad (visible, glowing)
# ─────────────────────────────────────────────────────────────────────────────
SHOT_01 = '''<template>
  <style>
    @font-face { font-family: "Playfair Display"; font-style: normal; font-weight: 400 900; src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM86xQ.woff2) format("woff2"); }
    @font-face { font-family: "Inter"; font-style: normal; font-weight: 100 900; src: url(https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2) format("woff2"); }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #050810; font-family: "Inter", sans-serif; color: #F2F1EC; }

    .bg-env {
      position: absolute; inset: -40px;
      background:
        radial-gradient(circle at 28% 50%, rgba(56,189,248,0.12) 0%, transparent 50%),
        radial-gradient(circle at 72% 50%, rgba(242,210,75,0.14) 0%, transparent 50%),
        linear-gradient(180deg, #07091280 0%, #020407 100%);
    }
    .grid-floor {
      position: absolute; bottom: 0; left: -120px; right: -120px; height: 900px;
      background: linear-gradient(180deg, transparent 0%, #0a0c15 100%);
      transform: perspective(1000px) rotateX(60deg);
      border-top: 1px solid rgba(255,255,255,0.06);
    }
    .grid-lines {
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(56,189,248,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.08) 1px, transparent 1px);
      background-size: 80px 80px;
    }

    /* PARTITION MONOLITH */
    .partition {
      position: absolute; left: 50%; top: 560px; bottom: 800px; width: 3px;
      transform: translateX(-50%);
      background: linear-gradient(180deg, transparent, rgba(255,255,255,0.25) 30%, rgba(255,255,255,0.25) 70%, transparent);
      box-shadow: 0 0 30px rgba(255,255,255,0.1);
    }

    /* SENSOR PAD — left (real, occluded) */
    .sensor-left {
      position: absolute; left: 140px; top: 680px;
      width: 300px; height: 200px;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px;
    }
    .pad-real {
      width: 220px; height: 130px; border-radius: 18px;
      background: rgba(4,12,28,0.92);
      border: 1.5px dashed rgba(56,189,248,0.35);
      box-shadow: 0 0 60px rgba(56,189,248,0.06), inset 0 0 30px rgba(56,189,248,0.04);
      position: relative; display: flex; align-items: center; justify-content: center;
    }
    .pad-real-grid {
      position: absolute; inset: 12px;
      background-image: linear-gradient(rgba(56,189,248,0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(56,189,248,0.12) 1px, transparent 1px);
      background-size: 22px 22px; border-radius: 8px;
    }
    .pad-occlude {
      position: absolute; inset: 0; border-radius: 18px;
      background: rgba(2,6,14,0.84); backdrop-filter: blur(4px);
      display: flex; align-items: center; justify-content: center;
    }
    .occlude-label {
      font-size: 11px; font-weight: 800; letter-spacing: 0.18em; color: #38BDF8;
      text-transform: uppercase; border: 1px solid rgba(56,189,248,0.4);
      padding: 6px 14px; border-radius: 6px; background: rgba(4,10,24,0.95);
    }
    .pad-label { font-size: 11px; font-weight: 700; color: #4A7FA0; letter-spacing: 0.14em; text-transform: uppercase; }

    /* SENSOR PAD — right (rubber, visible) */
    .sensor-right {
      position: absolute; right: 140px; top: 680px;
      width: 300px; height: 200px;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px;
    }
    .pad-rubber {
      width: 220px; height: 130px; border-radius: 18px;
      background: rgba(20,14,4,0.92);
      border: 1.5px solid rgba(242,210,75,0.5);
      box-shadow: 0 0 60px rgba(242,210,75,0.15), inset 0 0 30px rgba(242,210,75,0.06);
      position: relative; display: flex; align-items: center; justify-content: center;
    }
    .pad-rubber-grid {
      position: absolute; inset: 12px;
      background-image: linear-gradient(rgba(242,210,75,0.15) 1px, transparent 1px), linear-gradient(90deg, rgba(242,210,75,0.15) 1px, transparent 1px);
      background-size: 22px 22px; border-radius: 8px;
    }
    .pad-amber-core {
      width: 48px; height: 48px; border-radius: 50%;
      background: radial-gradient(circle, rgba(242,210,75,0.4) 0%, rgba(242,210,75,0.06) 60%, transparent 100%);
      box-shadow: 0 0 30px rgba(242,210,75,0.3);
    }
    .pad-ring {
      position: absolute; inset: -12px; border-radius: 50%;
      border: 1px dashed rgba(242,210,75,0.3);
    }
    .pad-rubber-label { font-size: 11px; font-weight: 800; color: #F2D24B; letter-spacing: 0.14em; text-transform: uppercase; }

    /* RETICLE */
    .scan-reticle {
      position: absolute; right: 136px; top: 668px; width: 312px; height: 224px;
      border: 1px dashed rgba(242,210,75,0.6); border-radius: 20px; opacity: 0; pointer-events: none;
    }
    .rc { position: absolute; width: 14px; height: 14px; border: 2px solid #F2D24B; }
    .rc-tl { top: -1px; left: -1px; border-right: none; border-bottom: none; }
    .rc-tr { top: -1px; right: -1px; border-left: none; border-bottom: none; }
    .rc-bl { bottom: -1px; left: -1px; border-right: none; border-top: none; }
    .rc-br { bottom: -1px; right: -1px; border-left: none; border-top: none; }

    /* HEADER */
    .hdr { position: absolute; top: 340px; left: 90px; right: 90px; display: flex; justify-content: space-between; }
    .hdr-badge { display: flex; align-items: center; gap: 10px; background: rgba(8,12,22,0.9); border: 1px solid rgba(242,210,75,0.3); padding: 9px 16px; border-radius: 8px; backdrop-filter: blur(10px); }
    .hdr-dot { width: 8px; height: 8px; border-radius: 50%; background: #F2D24B; box-shadow: 0 0 8px #F2D24B; }
    .hdr-txt { font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #F2F1EC; }
    .hdr-status { background: rgba(8,12,22,0.9); border: 1px solid rgba(56,189,248,0.35); padding: 9px 16px; border-radius: 8px; font-size: 11px; font-weight: 700; color: #38BDF8; letter-spacing: 0.12em; text-transform: uppercase; }

    /* CAPTION */
    .caption-block { position: absolute; bottom: 480px; left: 90px; right: 90px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 12px; }
    .caption-line { font-family: "Playfair Display", serif; font-size: 42px; font-weight: 700; line-height: 1.25; color: #F2F1EC; text-shadow: 0 4px 24px rgba(0,0,0,0.95); }
    .caption-line .accent { color: #F2D24B; font-style: italic; }
    .caption-sub { font-size: 17px; font-weight: 500; color: #A0A09C; letter-spacing: 0.12em; text-transform: uppercase; }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>

  <div id="root" data-composition-id="shot-01-setup" data-width="1080" data-height="1920" data-duration="8.74">
    <div id="bg" class="bg-env" data-layout-allow-overflow></div>
    <div class="grid-floor" data-layout-allow-overflow><div class="grid-lines"></div></div>

    <div class="hdr" data-layout-allow-overlap>
      <div class="hdr-badge"><div class="hdr-dot"></div><span class="hdr-txt">Botvinick & Cohen Protocol · 1998</span></div>
      <div class="hdr-status">Visual Occlusion: 100%</div>
    </div>

    <div class="partition" data-layout-allow-overlap></div>

    <!-- LEFT: Real touch sensor (hidden) -->
    <div id="sensor-l" class="sensor-left" data-layout-allow-overlap>
      <div class="pad-real">
        <div class="pad-real-grid"></div>
        <div id="occ" class="pad-occlude"><span class="occlude-label">Limb [Occluded]</span></div>
      </div>
      <span class="pad-label">Tactile Input A</span>
    </div>

    <!-- RIGHT: Rubber sensor pad (visible, amber) -->
    <div id="sensor-r" class="sensor-right" data-layout-allow-overlap>
      <div class="pad-rubber">
        <div class="pad-rubber-grid"></div>
        <div class="pad-amber-core"><div class="pad-ring"></div></div>
      </div>
      <span class="pad-rubber-label">Prosthetic Target [Visible]</span>
    </div>

    <!-- Scan reticle on rubber pad -->
    <div id="reticle" class="scan-reticle" data-layout-allow-overlap>
      <div class="rc rc-tl"></div><div class="rc rc-tr"></div>
      <div class="rc rc-bl"></div><div class="rc rc-br"></div>
    </div>

    <div class="caption-block" data-layout-allow-overlap>
      <p id="cap" class="caption-line">You place your left hand behind an opaque screen...</p>
      <span id="sub" class="caption-sub">The Sensory Decoupling Setup</span>
    </div>
  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["shot-01-setup"] = tl;

    const bg = document.getElementById("bg");
    const sensorL = document.getElementById("sensor-l");
    const sensorR = document.getElementById("sensor-r");
    const reticle = document.getElementById("reticle");
    const cap = document.getElementById("cap");
    const sub = document.getElementById("sub");

    gsap.set(reticle, { opacity: 0, scale: 1.12 });
    gsap.set(sensorR, { scale: 0.97 });

    tl.to(bg, { scale: 1.04, duration: 8.74, ease: "none" }, 0);
    tl.to(sensorL, { y: -10, duration: 8.74, ease: "power1.inOut" }, 0);
    tl.to(sensorR, { scale: 1.04, duration: 4, ease: "power2.out" }, 4.2);
    tl.to(reticle, { opacity: 1, scale: 1.0, duration: 0.8, ease: "back.out(1.5)" }, 4.5);
    tl.call(() => {
      cap.innerHTML = 'while an amber <span class="accent">prosthetic sensor rests directly in plain view</span>.';
      sub.innerText = 'Visual Focus: Prosthetic Target';
    }, null, 4.2);
  </script>
</template>'''

# ─────────────────────────────────────────────────────────────────────────────
# SHOT 02: Synchronous Tactile Binding — two signal waveforms lock in phase
# ─────────────────────────────────────────────────────────────────────────────
SHOT_02 = '''<template>
  <style>
    @font-face { font-family: "Playfair Display"; font-style: normal; font-weight: 400 900; src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM86xQ.woff2) format("woff2"); }
    @font-face { font-family: "Inter"; font-style: normal; font-weight: 100 900; src: url(https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2) format("woff2"); }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #040810; font-family: "Inter", sans-serif; color: #F2F1EC; }

    .bg-env {
      position: absolute; inset: -40px;
      background:
        radial-gradient(circle at 50% 45%, rgba(242,210,75,0.18) 0%, transparent 55%),
        radial-gradient(circle at 20% 70%, rgba(56,189,248,0.14) 0%, transparent 45%),
        linear-gradient(180deg, #080c18 0%, #020407 100%);
    }
    .dot-grid {
      position: absolute; inset: 0; opacity: 0.12;
      background-image: radial-gradient(rgba(242,210,75,0.4) 1px, transparent 1px);
      background-size: 40px 40px;
    }

    /* WAVEFORM OSCILLOSCOPE STAGE */
    .osc-stage {
      position: absolute; left: 90px; right: 90px; top: 500px; height: 620px;
      background: rgba(4,8,18,0.88); border: 1px solid rgba(255,255,255,0.1);
      border-radius: 24px; overflow: hidden;
      box-shadow: 0 30px 80px rgba(0,0,0,0.85), inset 0 0 40px rgba(0,0,0,0.6);
    }
    .osc-grid {
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
      background-size: 60px 60px;
    }
    .osc-header {
      position: absolute; top: 20px; left: 30px; right: 30px;
      display: flex; justify-content: space-between; align-items: center;
    }
    .osc-label { font-size: 11px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; }
    .osc-label-a { color: #38BDF8; }
    .osc-label-b { color: #F2D24B; }
    .phase-lock-badge {
      font-size: 11px; font-weight: 800; letter-spacing: 0.14em; color: #F2F1EC;
      background: rgba(242,210,75,0.15); border: 1px solid rgba(242,210,75,0.4);
      padding: 6px 14px; border-radius: 20px;
    }
    /* SVG waveforms */
    .osc-svg { position: absolute; inset: 0; width: 100%; height: 100%; }

    /* Binding bridge arc */
    .binding-arc {
      position: absolute; left: 60px; right: 60px; height: 100%;
      pointer-events: none;
    }

    /* Sync counter */
    .sync-counter {
      position: absolute; bottom: 400px; left: 50%; transform: translateX(-50%);
      display: flex; flex-direction: column; align-items: center; gap: 8px;
    }
    .sync-val { font-size: 72px; font-weight: 900; color: #F2D24B; letter-spacing: -0.02em; }
    .sync-unit { font-size: 14px; font-weight: 600; color: #A0A09C; letter-spacing: 0.14em; text-transform: uppercase; }

    .hdr { position: absolute; top: 340px; left: 90px; right: 90px; display: flex; justify-content: space-between; }
    .hdr-badge { display: flex; align-items: center; gap: 10px; background: rgba(8,12,22,0.9); border: 1px solid rgba(242,210,75,0.35); padding: 9px 16px; border-radius: 8px; }
    .hdr-dot { width: 8px; height: 8px; border-radius: 50%; background: #F2D24B; box-shadow: 0 0 8px #F2D24B; }
    .hdr-txt { font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #F2F1EC; }
    .delay-badge { background: rgba(8,12,22,0.9); border: 1px solid rgba(56,189,248,0.35); padding: 9px 16px; border-radius: 8px; font-size: 11px; font-weight: 700; color: #38BDF8; letter-spacing: 0.12em; text-transform: uppercase; }

    .caption-block { position: absolute; bottom: 480px; left: 90px; right: 90px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 12px; }
    .caption-line { font-family: "Playfair Display", serif; font-size: 42px; font-weight: 700; line-height: 1.25; color: #F2F1EC; text-shadow: 0 4px 24px rgba(0,0,0,0.95); }
    .caption-line .accent { color: #F2D24B; font-style: italic; }
    .caption-sub { font-size: 17px; font-weight: 500; color: #A0A09C; letter-spacing: 0.12em; text-transform: uppercase; }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>

  <div id="root" data-composition-id="shot-02-sync" data-width="1080" data-height="1920" data-duration="9.86">
    <div id="bg" class="bg-env" data-layout-allow-overflow></div>
    <div class="dot-grid" data-layout-allow-overflow></div>

    <div class="hdr" data-layout-allow-overlap>
      <div class="hdr-badge"><div class="hdr-dot"></div><span class="hdr-txt">Crossmodal Tactile Binding</span></div>
      <div class="delay-badge">Δt Phase Offset: 0ms</div>
    </div>

    <!-- Oscilloscope Stage -->
    <div id="osc" class="osc-stage" data-layout-allow-overlap>
      <div class="osc-grid"></div>
      <div class="osc-header">
        <span class="osc-label osc-label-a">Signal A — Tactile Input (Real)</span>
        <span id="phase-badge" class="phase-lock-badge">Acquiring...</span>
        <span class="osc-label osc-label-b">Signal B — Prosthetic (Rubber)</span>
      </div>
      <svg id="osc-svg" class="osc-svg" viewBox="0 0 900 620" preserveAspectRatio="none">
        <!-- Signal A: cyan sine wave (upper half) -->
        <path id="waveA" d="M0 200 Q56 120 112 200 Q168 280 224 200 Q280 120 336 200 Q392 280 448 200 Q504 120 560 200 Q616 280 672 200 Q728 120 784 200 Q840 280 900 200"
          stroke="#38BDF8" stroke-width="2.5" fill="none" opacity="0.9"/>
        <!-- Signal B: amber sine wave (lower half) — starts offset -->
        <path id="waveB" d="M0 420 Q56 340 112 420 Q168 500 224 420 Q280 340 336 420 Q392 500 448 420 Q504 340 560 420 Q616 500 672 420 Q728 340 784 420 Q840 500 900 420"
          stroke="#F2D24B" stroke-width="2.5" fill="none" opacity="0"/>
        <!-- Binding bridge lines (vertical connection bars) — hidden initially -->
        <line id="bridge1" x1="112" y1="200" x2="112" y2="420" stroke="rgba(255,255,255,0.2)" stroke-width="1" stroke-dasharray="4 4" opacity="0"/>
        <line id="bridge2" x1="336" y1="200" x2="336" y2="420" stroke="rgba(255,255,255,0.2)" stroke-width="1" stroke-dasharray="4 4" opacity="0"/>
        <line id="bridge3" x1="560" y1="200" x2="560" y2="420" stroke="rgba(255,255,255,0.2)" stroke-width="1" stroke-dasharray="4 4" opacity="0"/>
        <line id="bridge4" x1="784" y1="200" x2="784" y2="420" stroke="rgba(255,255,255,0.2)" stroke-width="1" stroke-dasharray="4 4" opacity="0"/>
        <!-- Phase lock golden arc connecting the two signals -->
        <path id="lock-arc" d="M0 310 Q450 230 900 310" stroke="rgba(242,210,75,0.5)" stroke-width="1.5" fill="none" stroke-dasharray="6 4" opacity="0"/>
      </svg>
    </div>

    <!-- Sync counter -->
    <div class="sync-counter" data-layout-allow-overlap>
      <span id="sync-val" class="sync-val">0</span>
      <span class="sync-unit">ms Phase Offset</span>
    </div>

    <div class="caption-block" data-layout-allow-overlap>
      <p id="cap" class="caption-line">Both sensor pads are brushed in <span class="accent">exact millisecond phase sync</span>.</p>
      <span id="sub" class="caption-sub">Crossmodal Tactile Binding Protocol</span>
    </div>
  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["shot-02-sync"] = tl;

    const bg = document.getElementById("bg");
    const waveB = document.getElementById("waveB");
    const bridge1 = document.getElementById("bridge1");
    const bridge2 = document.getElementById("bridge2");
    const bridge3 = document.getElementById("bridge3");
    const bridge4 = document.getElementById("bridge4");
    const lockArc = document.getElementById("lock-arc");
    const phaseBadge = document.getElementById("phase-badge");
    const syncVal = document.getElementById("sync-val");
    const cap = document.getElementById("cap");
    const sub = document.getElementById("sub");

    tl.to(bg, { scale: 1.04, duration: 9.86, ease: "none" }, 0);
    // Wave B fades in as sync begins
    tl.to(waveB, { opacity: 0.9, duration: 1.5, ease: "power2.in" }, 1.5);
    // Bridge connections appear
    tl.to([bridge1, bridge2, bridge3, bridge4], { opacity: 1, duration: 0.8, stagger: 0.15 }, 3.0);
    // Lock arc appears
    tl.to(lockArc, { opacity: 1, duration: 1.0 }, 3.8);
    // Phase offset counter counts down to 0
    tl.call(() => {
      let val = 120;
      const interval = setInterval(() => {
        val = Math.max(0, val - 8);
        syncVal.textContent = val;
        if (val === 0) { clearInterval(interval); phaseBadge.textContent = "PHASE LOCKED ✓"; }
      }, 80);
    }, null, 2.2);
    tl.call(() => {
      cap.innerHTML = 'Neural binding arcs fire. <span class="accent">The brain begins rewriting body ownership.</span>';
      sub.innerText = 'Cortical Remapping Initiated';
    }, null, 5.5);
  </script>
</template>'''

# ─────────────────────────────────────────────────────────────────────────────
# SHOT 03: Body Ownership Adoption — amber pad "hijacks" the neural map
# ─────────────────────────────────────────────────────────────────────────────
SHOT_03 = '''<template>
  <style>
    @font-face { font-family: "Playfair Display"; font-style: normal; font-weight: 400 900; src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM86xQ.woff2) format("woff2"); }
    @font-face { font-family: "Inter"; font-style: normal; font-weight: 100 900; src: url(https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2) format("woff2"); }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #050910; font-family: "Inter", sans-serif; color: #F2F1EC; }

    .bg-env {
      position: absolute; inset: -40px;
      background:
        radial-gradient(circle at 50% 48%, rgba(242,210,75,0.22) 0%, transparent 55%),
        linear-gradient(180deg, #080c18 0%, #020407 100%);
    }

    /* Body schema map — abstract neural topographic contour */
    .schema-map {
      position: absolute; left: 50%; top: 420px; transform: translateX(-50%);
      width: 700px; height: 720px;
    }
    .schema-svg { width: 100%; height: 100%; }

    /* Thermal/proprioceptive drift meter */
    .drift-panel {
      position: absolute; right: 80px; top: 520px; width: 200px;
      background: rgba(4,8,18,0.9); border: 1px solid rgba(242,210,75,0.3);
      border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 16px;
    }
    .drift-label { font-size: 10px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #A0A09C; }
    .drift-bar-wrap { width: 100%; height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; }
    .drift-bar { height: 100%; width: 0%; border-radius: 4px; background: #F2D24B; box-shadow: 0 0 8px #F2D24B; }
    .drift-val { font-size: 18px; font-weight: 800; color: #F2D24B; }

    .hdr { position: absolute; top: 340px; left: 90px; right: 90px; display: flex; justify-content: space-between; }
    .hdr-badge { display: flex; align-items: center; gap: 10px; background: rgba(8,12,22,0.9); border: 1px solid rgba(242,210,75,0.35); padding: 9px 16px; border-radius: 8px; }
    .hdr-dot { width: 8px; height: 8px; border-radius: 50%; background: #F2D24B; box-shadow: 0 0 8px #F2D24B; animation: pulse 1.2s ease-in-out infinite; }
    @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }
    .hdr-txt { font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #F2F1EC; }
    .hdr-status { background: rgba(8,12,22,0.9); border: 1px solid rgba(56,189,248,0.35); padding: 9px 16px; border-radius: 8px; font-size: 11px; font-weight: 700; color: #38BDF8; letter-spacing: 0.12em; text-transform: uppercase; }

    .caption-block { position: absolute; bottom: 480px; left: 90px; right: 90px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 12px; }
    .caption-line { font-family: "Playfair Display", serif; font-size: 42px; font-weight: 700; line-height: 1.25; color: #F2F1EC; text-shadow: 0 4px 24px rgba(0,0,0,0.95); }
    .caption-line .accent { color: #F2D24B; font-style: italic; }
    .caption-sub { font-size: 17px; font-weight: 500; color: #A0A09C; letter-spacing: 0.12em; text-transform: uppercase; }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>

  <div id="root" data-composition-id="shot-03-adoption" data-width="1080" data-height="1920" data-duration="9.86">
    <div id="bg" class="bg-env" data-layout-allow-overflow></div>

    <div class="hdr" data-layout-allow-overlap>
      <div class="hdr-badge"><div class="hdr-dot"></div><span class="hdr-txt">Body Ownership Plasticity · t+60s</span></div>
      <div class="hdr-status">Cortical Remap: Active</div>
    </div>

    <!-- Abstract topographic neural body schema map -->
    <div class="schema-map" data-layout-allow-overlap>
      <svg class="schema-svg" viewBox="0 0 700 720" fill="none">
        <!-- Topographic contour rings (abstract body map concept) -->
        <ellipse cx="350" cy="360" rx="320" ry="300" stroke="rgba(56,189,248,0.08)" stroke-width="1.5"/>
        <ellipse cx="350" cy="360" rx="260" ry="240" stroke="rgba(56,189,248,0.12)" stroke-width="1.5"/>
        <ellipse cx="350" cy="360" rx="200" ry="180" stroke="rgba(56,189,248,0.18)" stroke-width="1.5"/>
        <ellipse cx="350" cy="360" rx="140" ry="125" stroke="rgba(56,189,248,0.26)" stroke-width="1.5"/>
        <ellipse cx="350" cy="360" rx="82" ry="72" stroke="rgba(56,189,248,0.4)" stroke-width="2"/>
        <!-- Central ownership node — starts cyan, converts to amber -->
        <circle id="core-node" cx="350" cy="360" r="30" fill="rgba(56,189,248,0.15)" stroke="#38BDF8" stroke-width="2"/>
        <!-- Amber takeover rings expanding from core -->
        <circle id="amber-ring1" cx="350" cy="360" r="55" fill="none" stroke="rgba(242,210,75,0.0)" stroke-width="2"/>
        <circle id="amber-ring2" cx="350" cy="360" r="90" fill="none" stroke="rgba(242,210,75,0.0)" stroke-width="2"/>
        <circle id="amber-ring3" cx="350" cy="360" r="140" fill="none" stroke="rgba(242,210,75,0.0)" stroke-width="2"/>
        <!-- Ownership label -->
        <text id="ownership-label" x="350" y="367" text-anchor="middle" font-family="Inter" font-size="13" font-weight="800" letter-spacing="0.15em" fill="#38BDF8" opacity="0.8">SELF</text>
        <!-- Drift vector arrow -->
        <path id="drift-arrow" d="M350 360 L560 280" stroke="rgba(242,210,75,0.0)" stroke-width="2" marker-end="url(#arr)"/>
        <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#F2D24B"/></marker></defs>
        <!-- Prosthetic pad node (amber) at drift target -->
        <circle id="target-pad" cx="560" cy="270" r="22" fill="rgba(242,210,75,0.08)" stroke="rgba(242,210,75,0.0)" stroke-width="2"/>
        <text id="pad-label-txt" x="560" y="277" text-anchor="middle" font-family="Inter" font-size="10" font-weight="800" letter-spacing="0.1em" fill="rgba(242,210,75,0.0)">PROSTHETIC</text>
      </svg>
    </div>

    <!-- Drift metrics panel -->
    <div class="drift-panel" data-layout-allow-overlap>
      <span class="drift-label">Proprioceptive Drift</span>
      <span id="drift-num" class="drift-val">0.0 cm</span>
      <div class="drift-bar-wrap"><div id="drift-bar" class="drift-bar"></div></div>
      <span class="drift-label">Thermal Response</span>
      <span id="therm-num" class="drift-val">+0.0°C</span>
      <div class="drift-bar-wrap"><div id="therm-bar" class="drift-bar" style="background:#38BDF8;box-shadow:0 0 8px #38BDF8;"></div></div>
    </div>

    <div class="caption-block" data-layout-allow-overlap>
      <p id="cap" class="caption-line">After 60 seconds of sync, <span class="accent">the brain reassigns ownership</span> to the prosthetic.</p>
      <span id="sub" class="caption-sub">Body Schema Plasticity</span>
    </div>
  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["shot-03-adoption"] = tl;

    const bg = document.getElementById("bg");
    const coreNode = document.getElementById("core-node");
    const ring1 = document.getElementById("amber-ring1");
    const ring2 = document.getElementById("amber-ring2");
    const ring3 = document.getElementById("amber-ring3");
    const driftArrow = document.getElementById("drift-arrow");
    const targetPad = document.getElementById("target-pad");
    const padLabelTxt = document.getElementById("pad-label-txt");
    const ownershipLabel = document.getElementById("ownership-label");
    const driftNum = document.getElementById("drift-num");
    const thermNum = document.getElementById("therm-num");
    const driftBar = document.getElementById("drift-bar");
    const thermBar = document.getElementById("therm-bar");
    const cap = document.getElementById("cap");
    const sub = document.getElementById("sub");

    tl.to(bg, { scale: 1.04, duration: 9.86, ease: "none" }, 0);
    // Core node turns amber
    tl.to(coreNode, { attr: { fill: "rgba(242,210,75,0.2)", stroke: "#F2D24B" }, duration: 1.5, ease: "power2.inOut" }, 1.5);
    // Amber rings expand
    tl.to(ring1, { attr: { stroke: "rgba(242,210,75,0.5)" }, duration: 1.0 }, 2.2);
    tl.to(ring2, { attr: { stroke: "rgba(242,210,75,0.35)" }, duration: 1.0 }, 2.6);
    tl.to(ring3, { attr: { stroke: "rgba(242,210,75,0.2)" }, duration: 1.0 }, 3.0);
    // Drift arrow and target appear
    tl.to(driftArrow, { attr: { stroke: "rgba(242,210,75,0.7)" }, duration: 0.8 }, 3.5);
    tl.to(targetPad, { attr: { stroke: "rgba(242,210,75,0.7)", fill: "rgba(242,210,75,0.15)" }, duration: 0.8 }, 3.5);
    tl.to(padLabelTxt, { attr: { fill: "rgba(242,210,75,0.85)" }, duration: 0.6 }, 3.8);
    // Ownership label changes
    tl.call(() => { ownershipLabel.textContent = "PROSTHETIC"; ownershipLabel.setAttribute("fill", "#F2D24B"); }, null, 4.2);
    // Drift counters animate
    tl.call(() => {
      let drift = 0, therm = 0;
      const iv = setInterval(() => {
        drift = Math.min(6.8, drift + 0.3); therm = Math.max(-0.7, therm - 0.05);
        driftNum.textContent = drift.toFixed(1) + " cm";
        thermNum.textContent = therm.toFixed(1) + "°C";
        driftBar.style.width = (drift / 6.8 * 100) + "%";
        thermBar.style.width = (Math.abs(therm) / 0.7 * 100) + "%";
        if (drift >= 6.8) clearInterval(iv);
      }, 100);
    }, null, 3.8);
  </script>
</template>'''

# ─────────────────────────────────────────────────────────────────────────────
# SHOT 04: The Hammer Strike — threat signal hits prosthetic, panic waveform
# ─────────────────────────────────────────────────────────────────────────────
SHOT_04 = '''<template>
  <style>
    @font-face { font-family: "Playfair Display"; font-style: normal; font-weight: 400 900; src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM86xQ.woff2) format("woff2"); }
    @font-face { font-family: "Inter"; font-style: normal; font-weight: 100 900; src: url(https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2) format("woff2"); }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #050810; font-family: "Inter", sans-serif; color: #F2F1EC; }

    .bg-env {
      position: absolute; inset: -40px;
      background:
        radial-gradient(circle at 50% 50%, rgba(212,98,43,0.0) 0%, transparent 55%),
        linear-gradient(180deg, #080c18 0%, #020407 100%);
    }
    .bg-env.alarmed {
      background: radial-gradient(circle at 50% 48%, rgba(220,38,38,0.28) 0%, transparent 55%), linear-gradient(180deg, #12060808 0%, #020407 100%);
    }

    /* Sensor pad target — receives the threat impact */
    .impact-stage {
      position: absolute; left: 50%; top: 530px; transform: translateX(-50%);
      width: 580px; height: 440px;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 32px;
    }

    /* The amber prosthetic sensor pad */
    .target-sensor {
      width: 280px; height: 160px; border-radius: 20px;
      background: rgba(20,14,4,0.94); border: 2px solid rgba(242,210,75,0.5);
      box-shadow: 0 0 80px rgba(242,210,75,0.2); position: relative;
      display: flex; align-items: center; justify-content: center;
    }
    .target-inner-grid {
      position: absolute; inset: 14px;
      background-image: linear-gradient(rgba(242,210,75,0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(242,210,75,0.12) 1px, transparent 1px);
      background-size: 24px 24px; border-radius: 8px;
    }
    .pad-center-orb {
      width: 52px; height: 52px; border-radius: 50%;
      background: radial-gradient(circle, rgba(242,210,75,0.5) 0%, rgba(242,210,75,0.08) 60%, transparent 100%);
      box-shadow: 0 0 30px rgba(242,210,75,0.4);
    }

    /* IMPACT SHOCKWAVE rings */
    .shockwave { position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); pointer-events: none; }
    .sw-ring {
      position: absolute; border-radius: 50%;
      border: 2px solid rgba(220,38,38,0); left: 50%; top: 50%; transform: translate(-50%,-50%);
    }

    /* THREAT INDICATOR — descending velocity bar */
    .threat-bar-wrap {
      position: absolute; left: 90px; top: 500px; width: 60px; height: 500px;
      background: rgba(4,8,18,0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 30px;
      overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end;
    }
    .threat-fill { width: 100%; height: 0%; background: linear-gradient(180deg, #DC2626 0%, #F2D24B 100%); border-radius: 30px; }
    .threat-label { position: absolute; left: 90px; top: 995px; font-size: 10px; font-weight: 700; color: #DC2626; letter-spacing: 0.12em; text-transform: uppercase; writing-mode: vertical-rl; text-orientation: mixed; }

    /* ECG/GSR biometric panel */
    .biometric-panel {
      position: absolute; right: 70px; top: 500px; width: 210px;
      background: rgba(4,8,18,0.9); border: 1px solid rgba(220,38,38,0.3);
      border-radius: 16px; padding: 18px; display: flex; flex-direction: column; gap: 14px;
    }
    .bio-label { font-size: 10px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #A0A09C; }
    .bio-val { font-size: 22px; font-weight: 800; color: #F2F1EC; }
    .bio-val.alarm { color: #DC2626; }
    .bio-bar-wrap { width: 100%; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; }
    .bio-bar { height: 100%; border-radius: 3px; transition: width 0.1s; }

    /* IMPACT TEXT FLASH */
    .impact-flash {
      position: absolute; left: 50%; top: 680px; transform: translateX(-50%);
      font-size: 96px; font-weight: 900; color: #DC2626; letter-spacing: -0.02em;
      opacity: 0; text-shadow: 0 0 60px rgba(220,38,38,0.8);
    }

    .hdr { position: absolute; top: 340px; left: 90px; right: 90px; display: flex; justify-content: space-between; }
    .hdr-badge { display: flex; align-items: center; gap: 10px; background: rgba(8,12,22,0.9); border: 1px solid rgba(220,38,38,0.5); padding: 9px 16px; border-radius: 8px; }
    .hdr-dot { width: 8px; height: 8px; border-radius: 50%; background: #DC2626; box-shadow: 0 0 8px #DC2626; }
    .hdr-txt { font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #F2F1EC; }
    .hdr-status { background: rgba(8,12,22,0.9); border: 1px solid rgba(220,38,38,0.4); padding: 9px 16px; border-radius: 8px; font-size: 11px; font-weight: 700; color: #DC2626; letter-spacing: 0.12em; text-transform: uppercase; }

    .caption-block { position: absolute; bottom: 480px; left: 90px; right: 90px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 12px; }
    .caption-line { font-family: "Playfair Display", serif; font-size: 42px; font-weight: 700; line-height: 1.25; color: #F2F1EC; text-shadow: 0 4px 24px rgba(0,0,0,0.95); }
    .caption-line .accent { color: #DC2626; font-style: italic; }
    .caption-sub { font-size: 17px; font-weight: 500; color: #A0A09C; letter-spacing: 0.12em; text-transform: uppercase; }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>

  <div id="root" data-composition-id="shot-04-strike" data-width="1080" data-height="1920" data-duration="11.46">
    <div id="bg" class="bg-env" data-layout-allow-overflow></div>

    <div class="hdr" data-layout-allow-overlap>
      <div class="hdr-badge"><div class="hdr-dot"></div><span class="hdr-txt">Threat Stimulus Inbound</span></div>
      <div id="alarm-status" class="hdr-status">ECG: Nominal</div>
    </div>

    <!-- Threat velocity bar -->
    <div class="threat-bar-wrap" data-layout-allow-overlap>
      <div id="threat-fill" class="threat-fill"></div>
    </div>
    <span class="threat-label" data-layout-allow-overlap>IMPACT VELOCITY</span>

    <!-- Biometric panel -->
    <div class="biometric-panel" data-layout-allow-overlap>
      <span class="bio-label">Heart Rate</span>
      <span id="ecg-val" class="bio-val">72 BPM</span>
      <div class="bio-bar-wrap"><div id="ecg-bar" class="bio-bar" style="width:55%;background:#38BDF8;"></div></div>
      <span class="bio-label">Galvanic Skin Response</span>
      <span id="gsr-val" class="bio-val">1.2 μS</span>
      <div class="bio-bar-wrap"><div id="gsr-bar" class="bio-bar" style="width:18%;background:#38BDF8;"></div></div>
      <span class="bio-label">Adrenaline Index</span>
      <span id="adr-val" class="bio-val">Low</span>
      <div class="bio-bar-wrap"><div id="adr-bar" class="bio-bar" style="width:10%;background:#38BDF8;"></div></div>
    </div>

    <!-- Impact stage -->
    <div class="impact-stage" data-layout-allow-overlap>
      <div id="target" class="target-sensor">
        <div class="target-inner-grid"></div>
        <div id="orb" class="pad-center-orb"></div>
        <!-- Shockwave rings -->
        <div class="shockwave">
          <div id="sw1" class="sw-ring" style="width:80px;height:80px;"></div>
          <div id="sw2" class="sw-ring" style="width:160px;height:160px;"></div>
          <div id="sw3" class="sw-ring" style="width:280px;height:280px;"></div>
          <div id="sw4" class="sw-ring" style="width:440px;height:440px;"></div>
        </div>
      </div>
    </div>

    <!-- Impact flash text -->
    <div id="impact-flash" class="impact-flash" data-layout-allow-overlap>IMPACT</div>

    <div class="caption-block" data-layout-allow-overlap>
      <p id="cap" class="caption-line">A hammer strikes the prosthetic sensor...</p>
      <span id="sub" class="caption-sub">Threat Stimulus Delivered</span>
    </div>
  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["shot-04-strike"] = tl;

    const bg = document.getElementById("bg");
    const threatFill = document.getElementById("threat-fill");
    const target = document.getElementById("target");
    const orb = document.getElementById("orb");
    const [sw1,sw2,sw3,sw4] = ["sw1","sw2","sw3","sw4"].map(id=>document.getElementById(id));
    const impactFlash = document.getElementById("impact-flash");
    const ecgVal = document.getElementById("ecg-val");
    const gsrVal = document.getElementById("gsr-val");
    const adrVal = document.getElementById("adr-val");
    const ecgBar = document.getElementById("ecg-bar");
    const gsrBar = document.getElementById("gsr-bar");
    const adrBar = document.getElementById("adr-bar");
    const alarmStatus = document.getElementById("alarm-status");
    const cap = document.getElementById("cap");
    const sub = document.getElementById("sub");

    // Threat bar charges up
    tl.to(threatFill, { height: "100%", duration: 3.5, ease: "power1.in" }, 0.5);
    tl.to(bg, { scale: 1.04, duration: 4.5, ease: "none" }, 0);

    // IMPACT at 4.2s
    tl.to(orb, { scale: 2.5, opacity: 0, duration: 0.2, ease: "power4.out" }, 4.2);
    tl.to(target, { boxShadow: "0 0 200px rgba(220,38,38,0.9)", borderColor: "#DC2626", duration: 0.15 }, 4.2);
    tl.to(bg, { background: "radial-gradient(circle at 50% 48%, rgba(220,38,38,0.3) 0%, transparent 55%), linear-gradient(180deg, #080c18 0%, #020407 100%)", duration: 0.15 }, 4.2);
    // Shockwave rings expand
    [sw1,sw2,sw3,sw4].forEach((sw, i) => {
      tl.fromTo(sw, { scale: 0.3, opacity: 1, borderColor: "rgba(220,38,38,0.9)" },
        { scale: 1, opacity: 0, duration: 0.8, ease: "power2.out", borderColor: "rgba(220,38,38,0.0)" }, 4.2 + i * 0.1);
    });
    tl.to(impactFlash, { opacity: 1, duration: 0.1 }, 4.2);
    tl.to(impactFlash, { opacity: 0, duration: 0.4 }, 4.5);

    // Biometrics spike
    tl.call(() => {
      alarmStatus.textContent = "ECG: AUTONOMIC SPIKE";
      let bpm = 72, gsr = 1.2;
      const iv = setInterval(() => {
        bpm = Math.min(146, bpm + 5); gsr = Math.min(6.24, gsr + 0.3);
        ecgVal.textContent = bpm + " BPM"; ecgVal.className = bpm > 100 ? "bio-val alarm" : "bio-val";
        gsrVal.textContent = gsr.toFixed(1) + " μS"; gsrVal.className = gsr > 3 ? "bio-val alarm" : "bio-val";
        ecgBar.style.width = (bpm / 180 * 100) + "%"; ecgBar.style.background = bpm > 100 ? "#DC2626" : "#38BDF8";
        gsrBar.style.width = (gsr / 8 * 100) + "%"; gsrBar.style.background = gsr > 3 ? "#DC2626" : "#38BDF8";
        adrVal.textContent = bpm > 120 ? "CRITICAL" : bpm > 100 ? "HIGH" : "Elevated"; adrVal.className = bpm > 120 ? "bio-val alarm" : "bio-val";
        adrBar.style.width = Math.min(100, (bpm-72)/74*100) + "%"; adrBar.style.background = bpm > 110 ? "#DC2626" : "#F2D24B";
        if (bpm >= 146) clearInterval(iv);
      }, 80);
    }, null, 4.2);

    tl.call(() => {
      cap.innerHTML = '...and <span class="accent">your nervous system screams</span> in genuine terror.';
      sub.innerText = 'Autonomic Fight-or-Flight Response';
    }, null, 5.0);

    tl.to(bg, { scale: 1.06, duration: 6.0, ease: "power1.out" }, 4.5);
  </script>
</template>'''

# ─────────────────────────────────────────────────────────────────────────────
# SHOT 05: The Fragility of Self — neural identity is a real-time prediction
# ─────────────────────────────────────────────────────────────────────────────
SHOT_05 = '''<template>
  <style>
    @font-face { font-family: "Playfair Display"; font-style: normal; font-weight: 400 900; src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM86xQ.woff2) format("woff2"); }
    @font-face { font-family: "Inter"; font-style: normal; font-weight: 100 900; src: url(https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2) format("woff2"); }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #030609; font-family: "Inter", sans-serif; color: #F2F1EC; }

    .bg-env {
      position: absolute; inset: -40px;
      background:
        radial-gradient(circle at 50% 48%, rgba(242,210,75,0.3) 0%, rgba(56,189,248,0.08) 40%, transparent 70%),
        linear-gradient(180deg, #060a14 0%, #020407 100%);
    }

    /* Expanding harmonic rings of identity */
    .harmonic-rings {
      position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
      width: 1000px; height: 1000px; pointer-events: none;
    }

    /* Neural particle matrix — abstract self representation */
    .particle-grid {
      position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
      width: 640px; height: 640px;
    }

    /* Manifesto text */
    .manifesto-wrap {
      position: absolute; left: 90px; right: 90px; top: 440px;
      display: flex; flex-direction: column; align-items: center; gap: 24px; text-align: center;
    }
    .manifesto-eyebrow { font-size: 12px; font-weight: 700; color: #A0A09C; letter-spacing: 0.25em; text-transform: uppercase; }
    .manifesto-title {
      font-family: "Playfair Display", serif; font-size: 72px; font-weight: 900;
      line-height: 1.1; color: #F2D24B;
      text-shadow: 0 0 80px rgba(242,210,75,0.5), 0 4px 24px rgba(0,0,0,0.95);
    }
    .manifesto-sub { font-size: 18px; font-weight: 500; color: #F2F1EC; line-height: 1.6; opacity: 0; }
    .manifesto-sub .accent { color: #F2D24B; font-style: italic; }

    .caption-block { position: absolute; bottom: 480px; left: 90px; right: 90px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 12px; }
    .caption-line { font-family: "Playfair Display", serif; font-size: 42px; font-weight: 700; line-height: 1.25; color: #F2F1EC; text-shadow: 0 4px 24px rgba(0,0,0,0.95); }
    .caption-line .accent { color: #F2D24B; font-style: italic; }
    .caption-sub { font-size: 17px; font-weight: 500; color: #A0A09C; letter-spacing: 0.12em; text-transform: uppercase; }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>

  <div id="root" data-composition-id="shot-05-plasticity" data-width="1080" data-height="1920" data-duration="8.82">
    <div id="bg" class="bg-env" data-layout-allow-overflow></div>

    <!-- Expanding harmonic identity rings -->
    <div class="harmonic-rings" data-layout-allow-overflow>
      <svg width="1000" height="1000" viewBox="0 0 1000 1000" fill="none">
        <circle id="r1" cx="500" cy="500" r="60" stroke="rgba(242,210,75,0.6)" stroke-width="1.5" opacity="0"/>
        <circle id="r2" cx="500" cy="500" r="130" stroke="rgba(242,210,75,0.45)" stroke-width="1" opacity="0"/>
        <circle id="r3" cx="500" cy="500" r="210" stroke="rgba(242,210,75,0.3)" stroke-width="1" opacity="0"/>
        <circle id="r4" cx="500" cy="500" r="300" stroke="rgba(56,189,248,0.2)" stroke-width="1" opacity="0"/>
        <circle id="r5" cx="500" cy="500" r="400" stroke="rgba(56,189,248,0.12)" stroke-width="1" opacity="0"/>
        <circle id="r6" cx="500" cy="500" r="480" stroke="rgba(56,189,248,0.07)" stroke-width="1" opacity="0"/>
        <!-- Central identity node -->
        <circle id="id-core" cx="500" cy="500" r="28"
          fill="rgba(242,210,75,0.3)" stroke="#F2D24B" stroke-width="2" opacity="0"/>
        <text id="core-txt" x="500" y="506" text-anchor="middle" font-family="Inter"
          font-size="11" font-weight="800" letter-spacing="0.12em" fill="#F2D24B" opacity="0">SELF</text>
      </svg>
    </div>

    <!-- Manifesto -->
    <div id="manifesto" class="manifesto-wrap" data-layout-allow-overlap>
      <span class="manifesto-eyebrow" id="eyebrow" style="opacity:0">The Rubber Hand Illusion reveals</span>
      <div class="manifesto-title" id="manifesto-title" style="opacity:0">YOUR BODY<br/>IS A PREDICTION</div>
      <p class="manifesto-sub" id="manifesto-sub">
        Physical selfhood is not fixed biology —<br/>
        it is a <span class="accent">continuous real-time inference</span><br/>
        that can be hijacked in 60 seconds.
      </p>
    </div>

    <div class="caption-block" data-layout-allow-overlap>
      <p id="cap" class="caption-line">The self is not fixed. It is a <span class="accent">real-time prediction</span> your brain updates every second.</p>
      <span id="sub" class="caption-sub">Body Ownership Plasticity</span>
    </div>
  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["shot-05-plasticity"] = tl;

    const bg = document.getElementById("bg");
    const rings = ["r1","r2","r3","r4","r5","r6"].map(id=>document.getElementById(id));
    const idCore = document.getElementById("id-core");
    const coreTxt = document.getElementById("core-txt");
    const eyebrow = document.getElementById("eyebrow");
    const title = document.getElementById("manifesto-title");
    const mSub = document.getElementById("manifesto-sub");

    tl.to(bg, { scale: 1.08, duration: 8.82, ease: "power1.inOut" }, 0);
    // Rings appear sequentially
    rings.forEach((r, i) => tl.to(r, { opacity: 1, duration: 1.0, ease: "power2.out" }, 0.4 + i * 0.3));
    // Core identity node
    tl.to([idCore, coreTxt], { opacity: 1, duration: 0.8, ease: "power2.out" }, 0.6);
    // Manifesto elements reveal
    tl.to(eyebrow, { opacity: 1, duration: 0.6, ease: "power2.out" }, 2.5);
    tl.to(title, { opacity: 1, duration: 0.8, ease: "power2.out" }, 3.0);
    tl.to(mSub, { opacity: 1, duration: 1.0, ease: "power2.out" }, 3.8);
    // Rings pulse out gently
    rings.forEach((r, i) => tl.to(r, { scale: 1.12, opacity: 0.5, duration: 3, ease: "sine.inOut", yoyo: true, repeat: 1 }, 4.0 + i * 0.1));
  </script>
</template>'''

# ─────────────────────────────────────────────────────────────────────────────
# WRITE ALL 5 SHOTS
# ─────────────────────────────────────────────────────────────────────────────
shots = {
    'shot-01-setup.html': SHOT_01,
    'shot-02-sync.html': SHOT_02,
    'shot-03-adoption.html': SHOT_03,
    'shot-04-strike.html': SHOT_04,
    'shot-05-plasticity.html': SHOT_05,
}

for filename, content in shots.items():
    path = os.path.join(FRAMES_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ Written: {filename}")

print("\n🎬 All 5 shots rewritten with abstract visual language — zero anatomy.")
