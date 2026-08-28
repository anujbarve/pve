#!/usr/bin/env python3
"""
Upgrade change blindness worker carrier SVGs to high-quality cinematic forms.
Replaces rough worker SVGs with refined anatomical figures with volumetric depth.
"""
import re
import os

FRAMES_DIR = os.path.join(os.path.dirname(__file__), "compositions", "frames")

# ─── High-quality worker carrier SVG (front, yellow high-vis) ────────────────
WORKER_FRONT_SVG = """<svg viewBox="0 0 140 480" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="wfBodyGrad-SHOT" cx="50%" cy="40%" r="60%" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="#1E2D42"/>
      <stop offset="100%" stop-color="#040810"/>
    </radialGradient>
    <linearGradient id="wfRim-SHOT" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="rgba(242,210,75,0.75)"/>
      <stop offset="100%" stop-color="rgba(242,210,75,0.05)"/>
    </linearGradient>
    <filter id="wfGlow-SHOT">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Head shape — slightly forward-tilted from carrying load -->
  <path d="M58 56 C58 40, 72 34, 82 38 C90 42, 94 54, 90 64 C86 74, 74 76, 66 72 C58 68, 56 62, 58 56 Z"
        fill="url(#wfBodyGrad-SHOT)" stroke="rgba(100,116,139,0.9)" stroke-width="1.4"/>
  <!-- Hard hat / cap -->
  <path d="M52 50 L92 50 C95 50, 96 56, 93 58 L50 56 C48 56, 48 50, 52 50 Z"
        fill="#F2D24B" opacity="0.9"/>
  <!-- Cap brim -->
  <path d="M48 58 L100 58 L98 63 L50 63 Z" fill="#D4A017" opacity="0.8"/>

  <!-- Neck -->
  <path d="M70 72 L67 86 L77 86 Z" fill="#0F172A"/>

  <!-- Collar (jacket V-shape) -->
  <path d="M60 90 L72 115 L82 90 Z" fill="#334155" opacity="0.5"/>

  <!-- Torso: forward lean (load carrying posture) — volumetric jacket -->
  <path d="M44 90 C44 84, 104 82, 108 90
           L114 185 L112 270 C112 278, 38 280, 36 270 L40 185 Z"
        fill="url(#wfBodyGrad-SHOT)" stroke="url(#wfRim-SHOT)" stroke-width="1.8"/>

  <!-- High-visibility diagonal harness straps -->
  <path d="M58 88 L72 185 L82 185 L64 88 Z" fill="#F2D24B" opacity="0.75"/>
  <path d="M98 88 L84 185 L74 185 L90 88 Z" fill="#F2D24B" opacity="0.75"/>
  <!-- Horizontal reflective band across chest -->
  <path d="M38 155 L112 150" stroke="#F2D24B" stroke-width="5" stroke-linecap="round" opacity="0.6"/>

  <!-- Right arm extended outward holding door (power pose) -->
  <path d="M104 96 C118 100, 136 118, 136 148 L130 152 L120 125 L108 112 Z"
        fill="#1E2D42" stroke="rgba(148,163,184,0.8)" stroke-width="1.5"/>
  <!-- Gloved hand grip -->
  <path d="M130 148 C134 152, 138 158, 134 164 C130 170, 124 166, 122 160 C120 154, 124 148, 130 148 Z"
        fill="#0F172A" stroke="#F2D24B" stroke-width="1.2"/>

  <!-- Left arm naturally down and bracing -->
  <path d="M42 96 C32 110, 30 148, 34 175 C36 185, 48 185, 50 172 L54 125 Z"
        fill="#142033" stroke="rgba(100,116,139,0.7)" stroke-width="1.2"/>

  <!-- Legs in stride (mid-step walk pose) -->
  <!-- Left leg forward -->
  <path d="M42 272 L36 430 L56 430 L64 315 L70 315 L80 430 L100 430 L96 272 Z"
        fill="#08111D" stroke="rgba(71,85,105,0.8)" stroke-width="1.5"/>
  <!-- Boot details -->
  <path d="M32 430 L56 430 C60 430, 60 445, 54 448 L28 448 C24 448, 24 430, 32 430 Z"
        fill="#020617" stroke="#F2D24B" stroke-width="1"/>
  <path d="M78 430 L102 430 C106 430, 106 445, 100 448 L74 448 C70 448, 70 430, 78 430 Z"
        fill="#020617" stroke="#F2D24B" stroke-width="1"/>
</svg>"""

# ─── High-quality worker carrier SVG (back carrier) ──────────────────────────
WORKER_BACK_SVG = """<svg viewBox="0 0 140 480" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="wbBodyGrad-SHOT" cx="50%" cy="40%" r="60%" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="#161E2A"/>
      <stop offset="100%" stop-color="#030609"/>
    </radialGradient>
    <linearGradient id="wbRim-SHOT" x1="1" y1="0" x2="0" y2="0" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="rgba(242,210,75,0.6)"/>
      <stop offset="100%" stop-color="rgba(242,210,75,0.04)"/>
    </linearGradient>
  </defs>

  <!-- Head — slightly turned away from viewer -->
  <path d="M58 52 C58 36, 72 30, 82 34 C91 38, 95 52, 91 62 C87 72, 74 75, 66 70 C57 65, 56 58, 58 52 Z"
        fill="url(#wbBodyGrad-SHOT)" stroke="rgba(71,85,105,0.85)" stroke-width="1.4"/>
  <!-- Hard hat -->
  <path d="M52 46 L92 46 C95 46, 96 52, 93 54 L50 52 C47 52, 47 46, 52 46 Z"
        fill="#F2D24B" opacity="0.85"/>
  <path d="M47 54 L100 54 L98 60 L50 60 Z" fill="#D4A017" opacity="0.75"/>

  <!-- Neck -->
  <path d="M70 68 L67 82 L77 82 Z" fill="#0B1220"/>

  <!-- Collar -->
  <path d="M60 86 L72 110 L82 86 Z" fill="#334155" opacity="0.45"/>

  <!-- Torso: from behind, leaning with upper load hold -->
  <path d="M40 86 C40 80, 106 78, 110 88
           L116 182 L114 268 C114 276, 36 278, 34 268 L36 182 Z"
        fill="url(#wbBodyGrad-SHOT)" stroke="url(#wbRim-SHOT)" stroke-width="1.8"/>

  <!-- High-vis harness straps (reverse angle) -->
  <path d="M56 84 L68 180 L78 180 L62 84 Z" fill="#F2D24B" opacity="0.7"/>
  <path d="M96 84 L82 180 L72 180 L88 84 Z" fill="#F2D24B" opacity="0.7"/>
  <!-- Reflective chest band -->
  <path d="M36 150 L114 145" stroke="#F2D24B" stroke-width="5" stroke-linecap="round" opacity="0.55"/>

  <!-- Left arm reaching up holding top of door frame -->
  <path d="M42 92 C30 100, 24 128, 28 162 L44 162 L50 120 Z"
        fill="#1A2535" stroke="rgba(148,163,184,0.75)" stroke-width="1.5"/>
  <!-- Gloved hand -->
  <path d="M26 158 C22 164, 24 172, 30 172 C36 172, 40 164, 38 158 C36 150, 28 150, 26 158 Z"
        fill="#0F172A" stroke="#F2D24B" stroke-width="1.2"/>

  <!-- Right arm down stabilizing -->
  <path d="M106 94 C118 108, 122 148, 116 175 C114 186, 102 186, 100 172 L106 130 Z"
        fill="#111B28" stroke="rgba(100,116,139,0.65)" stroke-width="1.2"/>

  <!-- Legs — opposite stride from front worker -->
  <path d="M40 270 L34 430 L54 430 L62 315 L68 315 L78 430 L100 430 L94 270 Z"
        fill="#060D18" stroke="rgba(71,85,105,0.75)" stroke-width="1.5"/>
  <!-- Boots -->
  <path d="M30 430 L54 430 C58 430, 58 444, 52 447 L26 447 C22 447, 22 430, 30 430 Z"
        fill="#020617" stroke="#F2D24B" stroke-width="1"/>
  <path d="M76 430 L100 430 C104 430, 104 444, 98 447 L72 447 C68 447, 68 430, 76 430 Z"
        fill="#020617" stroke="#F2D24B" stroke-width="1"/>
</svg>"""


def patch_file(filepath, shot_id):
    with open(filepath, 'r') as f:
        content = f.read()

    front_svg = WORKER_FRONT_SVG.replace('-SHOT', f'-{shot_id}')
    back_svg = WORKER_BACK_SVG.replace('-SHOT', f'-{shot_id}')

    # Replace the front worker SVG (first match in worker-carrier-front div)
    # Find the worker-carrier-front SVG block
    content = re.sub(
        r'(<div class="worker-carrier-front">)\s*<svg[^>]*>.*?</svg>',
        r'\1\n            ' + front_svg,
        content,
        count=1,
        flags=re.DOTALL
    )

    # Replace the back worker SVG
    content = re.sub(
        r'(<div class="worker-carrier-back">)\s*<svg[^>]*>.*?</svg>',
        r'\1\n            ' + back_svg,
        content,
        count=1,
        flags=re.DOTALL
    )

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"✅ Patched {os.path.basename(filepath)} (shot_id={shot_id})")


if __name__ == '__main__':
    # Only shot-01-door.html has the workers
    target = os.path.join(FRAMES_DIR, 'shot-01-door.html')
    if os.path.exists(target):
        patch_file(target, 'CB1')
    else:
        print(f"⚠️  Not found: {target}")
    print("\n🎬 Change Blindness worker figures upgraded to cinematic volumetric forms.")
