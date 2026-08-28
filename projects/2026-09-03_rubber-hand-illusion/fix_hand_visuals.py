#!/usr/bin/env python3
"""
Fix rubber hand visuals across all 5 shots.
Replaces thin stroke-only finger outlines with volumetric filled hand forms
using gradient fills, subsurface scatter glow, and cinematic depth shading.
"""
import re
import os

FRAMES_DIR = os.path.join(os.path.dirname(__file__), "compositions", "frames")

# ─── Volumetric Neural Hand SVG (left/real hand — cyan neural mesh) ──────────
REAL_HAND_SVG = """<svg class="hand-svg-container" viewBox="0 0 260 420" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Palm body gradient: dark core with cyan edge glow -->
    <radialGradient id="palmGradR-SHOT" cx="50%" cy="60%" r="55%" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="rgba(2,8,18,0.95)"/>
      <stop offset="60%" stop-color="rgba(8,28,52,0.88)"/>
      <stop offset="100%" stop-color="rgba(32,96,140,0.6)"/>
    </radialGradient>
    <radialGradient id="sssR-SHOT" cx="50%" cy="50%" r="55%" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="rgba(56,189,248,0.0)"/>
      <stop offset="70%" stop-color="rgba(56,189,248,0.05)"/>
      <stop offset="100%" stop-color="rgba(56,189,248,0.22)"/>
    </radialGradient>
    <filter id="glowR-SHOT" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Wrist cylinder base -->
  <path d="M82 410 C78 380 76 360 80 338 L140 338 C144 360 142 380 138 410 Z"
        fill="url(#palmGradR-SHOT)" stroke="rgba(56,189,248,0.5)" stroke-width="1.5"/>

  <!-- Main palm body — full volumetric closed shape -->
  <path d="M68 338
           C48 305 42 265 46 220
           C50 185 62 168 80 160
           C85 148 94 140 105 138
           C116 140 124 148 128 160
           C146 166 158 184 164 220
           C168 265 162 305 142 338 Z"
        fill="url(#palmGradR-SHOT)" stroke="rgba(56,189,248,0.7)" stroke-width="1.8"/>

  <!-- Subsurface scatter inner glow layer -->
  <path d="M68 338
           C48 305 42 265 46 220
           C50 185 62 168 80 160
           C85 148 94 140 105 138
           C116 140 124 148 128 160
           C146 166 158 184 164 220
           C168 265 162 305 142 338 Z"
        fill="url(#sssR-SHOT)"/>

  <!-- Thumb — filled volumetric, not just an outline -->
  <path d="M68 240 C52 226 38 208 28 182 C22 162 26 148 38 148
           C50 148 58 164 62 186 C66 208 68 225 70 240 Z"
        fill="url(#palmGradR-SHOT)" stroke="rgba(56,189,248,0.65)" stroke-width="1.5"/>

  <!-- Index finger — volumetric filled finger shape -->
  <path d="M76 160 C72 138 70 112 72 84 C74 68 82 58 92 58
           C102 58 108 68 108 84 C108 112 106 138 102 160 Z"
        fill="url(#palmGradR-SHOT)" stroke="rgba(56,189,248,0.7)" stroke-width="1.5"/>

  <!-- Middle finger — tallest, widest -->
  <path d="M102 158 C100 130 100 100 102 68 C104 50 112 40 122 40
           C132 40 138 50 138 68 C138 100 136 130 132 158 Z"
        fill="url(#palmGradR-SHOT)" stroke="rgba(56,189,248,0.8)" stroke-width="1.8"/>

  <!-- Ring finger -->
  <path d="M132 160 C130 136 130 110 132 84 C134 68 142 58 152 58
           C162 58 166 68 166 84 C164 110 162 136 160 160 Z"
        fill="url(#palmGradR-SHOT)" stroke="rgba(56,189,248,0.7)" stroke-width="1.5"/>

  <!-- Little finger — slightly shorter -->
  <path d="M160 170 C160 150 162 128 165 106 C167 92 174 84 182 84
           C190 84 194 92 192 106 C190 128 188 150 186 170 Z"
        fill="url(#palmGradR-SHOT)" stroke="rgba(56,189,248,0.6)" stroke-width="1.4"/>

  <!-- Neural tractography mesh lines radiating from palm center -->
  <path d="M105 338 Q92 250 88 90" stroke="rgba(56,189,248,0.45)" stroke-width="1" stroke-dasharray="4 6"/>
  <path d="M105 338 Q110 240 122 55" stroke="rgba(56,189,248,0.55)" stroke-width="1.2" stroke-dasharray="4 6"/>
  <path d="M105 338 Q128 250 148 90" stroke="rgba(56,189,248,0.45)" stroke-width="1" stroke-dasharray="4 6"/>
  <path d="M105 338 Q78 265 45 185" stroke="rgba(56,189,248,0.45)" stroke-width="1" stroke-dasharray="4 6"/>
  <path d="M105 338 Q168 270 180 110" stroke="rgba(56,189,248,0.35)" stroke-width="1" stroke-dasharray="3 7"/>

  <!-- Knuckle articulation nodes with glow -->
  <circle cx="105" cy="340" r="5" fill="#38BDF8" filter="url(#glowR-SHOT)"/>
  <circle cx="91" cy="162" r="4" fill="#38BDF8" filter="url(#glowR-SHOT)"/>
  <circle cx="120" cy="158" r="4" fill="#38BDF8" filter="url(#glowR-SHOT)"/>
  <circle cx="149" cy="162" r="4" fill="#38BDF8" filter="url(#glowR-SHOT)"/>
  <circle cx="174" cy="172" r="3.5" fill="#38BDF8" filter="url(#glowR-SHOT)"/>
  <circle cx="60" cy="248" r="3.5" fill="#38BDF8" filter="url(#glowR-SHOT)"/>

  <!-- Distal phalange tip nodes -->
  <circle cx="92" cy="62" r="3" fill="rgba(56,189,248,0.85)"/>
  <circle cx="122" cy="44" r="3" fill="rgba(56,189,248,0.85)"/>
  <circle cx="152" cy="62" r="3" fill="rgba(56,189,248,0.85)"/>
  <circle cx="183" cy="88" r="3" fill="rgba(56,189,248,0.7)"/>
</svg>"""

# ─── Volumetric Rubber Hand SVG (amber/gold prosthetic skin) ─────────────────
RUBBER_HAND_SVG = """<svg class="rubber-svg-container" viewBox="0 0 260 420" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Prosthetic silicone skin — warm amber tones with depth -->
    <radialGradient id="palmGradRH-SHOT" cx="45%" cy="55%" r="58%" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="rgba(80,45,8,0.9)"/>
      <stop offset="50%" stop-color="rgba(55,32,5,0.95)"/>
      <stop offset="100%" stop-color="rgba(30,15,2,0.98)"/>
    </radialGradient>
    <!-- Subsurface amber scatter -->
    <radialGradient id="sssRH-SHOT" cx="50%" cy="45%" r="55%" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="rgba(242,180,40,0.0)"/>
      <stop offset="60%" stop-color="rgba(242,180,40,0.07)"/>
      <stop offset="100%" stop-color="rgba(242,180,40,0.28)"/>
    </radialGradient>
    <!-- Edge highlight gradient (left rim-lit) -->
    <linearGradient id="rimRH-SHOT" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="rgba(242,210,75,0.65)"/>
      <stop offset="25%" stop-color="rgba(242,210,75,0.15)"/>
      <stop offset="100%" stop-color="rgba(180,100,20,0.08)"/>
    </linearGradient>
    <filter id="glowRH-SHOT" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Wrist / forearm stub -->
  <path d="M82 410 C78 380 76 358 80 336 L140 336 C144 358 142 380 138 410 Z"
        fill="url(#palmGradRH-SHOT)" stroke="rgba(242,210,75,0.55)" stroke-width="1.8"/>

  <!-- Main palm — full volumetric prosthetic skin body -->
  <path d="M68 336
           C46 302 40 260 44 216
           C48 182 62 165 80 157
           C85 145 94 136 105 134
           C116 136 124 145 128 157
           C147 163 160 182 165 216
           C170 260 164 302 142 336 Z"
        fill="url(#palmGradRH-SHOT)" stroke="rgba(242,210,75,0.75)" stroke-width="2"/>

  <!-- Inner subsurface scatter glow -->
  <path d="M68 336
           C46 302 40 260 44 216
           C48 182 62 165 80 157
           C85 145 94 136 105 134
           C116 136 124 145 128 157
           C147 163 160 182 165 216
           C170 260 164 302 142 336 Z"
        fill="url(#sssRH-SHOT)"/>

  <!-- Rim light layer -->
  <path d="M68 336 C46 302 40 260 44 216 C48 182 62 165 80 157 C85 145 94 136 105 134"
        stroke="url(#rimRH-SHOT)" stroke-width="3" fill="none"/>

  <!-- Thumb — filled prosthetic rubber volume -->
  <path d="M68 238 C52 224 36 206 26 180 C20 160 25 146 38 146
           C51 146 60 163 64 186 C68 208 68 224 70 238 Z"
        fill="url(#palmGradRH-SHOT)" stroke="rgba(242,210,75,0.65)" stroke-width="1.8"/>

  <!-- Index finger — volumetric rubber skin -->
  <path d="M76 158 C72 136 70 110 72 82 C74 65 83 55 93 55
           C103 55 109 65 109 82 C109 110 107 136 103 158 Z"
        fill="url(#palmGradRH-SHOT)" stroke="rgba(242,210,75,0.72)" stroke-width="1.8"/>

  <!-- Middle finger — tallest -->
  <path d="M103 156 C101 128 101 98 103 66 C105 48 113 37 123 37
           C133 37 139 48 139 66 C139 98 137 128 133 156 Z"
        fill="url(#palmGradRH-SHOT)" stroke="rgba(242,210,75,0.85)" stroke-width="2"/>

  <!-- Ring finger -->
  <path d="M133 158 C131 134 131 108 133 82 C135 65 143 55 153 55
           C163 55 167 65 167 82 C165 108 163 134 161 158 Z"
        fill="url(#palmGradRH-SHOT)" stroke="rgba(242,210,75,0.72)" stroke-width="1.8"/>

  <!-- Little finger — shorter -->
  <path d="M161 168 C161 148 163 126 167 104 C169 90 176 82 184 82
           C192 82 196 90 194 104 C192 126 190 148 187 168 Z"
        fill="url(#palmGradRH-SHOT)" stroke="rgba(242,210,75,0.62)" stroke-width="1.6"/>

  <!-- Tendon crease lines on back of hand (realistic detail) -->
  <path d="M93 158 Q95 200 97 240" stroke="rgba(242,210,75,0.35)" stroke-width="1" stroke-dasharray="3 5"/>
  <path d="M123 155 Q124 200 125 240" stroke="rgba(242,210,75,0.42)" stroke-width="1.2" stroke-dasharray="3 5"/>
  <path d="M153 158 Q152 200 150 240" stroke="rgba(242,210,75,0.35)" stroke-width="1" stroke-dasharray="3 5"/>

  <!-- Knuckle joint highlights — amber glowing nodes -->
  <circle cx="105" cy="338" r="5.5" fill="#F2D24B" filter="url(#glowRH-SHOT)"/>
  <circle cx="91" cy="160" r="4.5" fill="#F2D24B" filter="url(#glowRH-SHOT)"/>
  <circle cx="121" cy="156" r="4.5" fill="#F2D24B" filter="url(#glowRH-SHOT)"/>
  <circle cx="151" cy="160" r="4.5" fill="#F2D24B" filter="url(#glowRH-SHOT)"/>
  <circle cx="175" cy="170" r="4" fill="#F2D24B" filter="url(#glowRH-SHOT)"/>
  <circle cx="60" cy="245" r="4" fill="#F2D24B" filter="url(#glowRH-SHOT)"/>

  <!-- Fingertip terminal nodes -->
  <circle cx="93" cy="58" r="3.5" fill="rgba(242,210,75,0.9)"/>
  <circle cx="123" cy="40" r="3.5" fill="rgba(242,210,75,0.9)"/>
  <circle cx="153" cy="58" r="3.5" fill="rgba(242,210,75,0.9)"/>
  <circle cx="184" cy="85" r="3" fill="rgba(242,210,75,0.75)"/>
</svg>"""


def get_shot_id(filepath):
    """Extract shot id like 'S1', 'S2' etc for gradient namespacing."""
    basename = os.path.basename(filepath)
    mapping = {
        'shot-01-setup.html': 'S1',
        'shot-02-sync.html': 'S2',
        'shot-03-adoption.html': 'S3',
        'shot-04-strike.html': 'S4',
        'shot-05-plasticity.html': 'S5',
    }
    return mapping.get(basename, 'SX')


def patch_file(filepath):
    shot_id = get_shot_id(filepath)
    with open(filepath, 'r') as f:
        content = f.read()

    real_svg = REAL_HAND_SVG.replace('-SHOT', f'-{shot_id}')
    rubber_svg = RUBBER_HAND_SVG.replace('-SHOT', f'-{shot_id}')

    # Replace real hand SVG (in hand-svg-container)
    content = re.sub(
        r'<svg class="hand-svg-container"[^<]*viewBox="0 0 260 420"[^>]*>.*?</svg>',
        real_svg,
        content,
        flags=re.DOTALL
    )

    # Replace rubber hand SVG (in rubber-svg-container)
    content = re.sub(
        r'<svg class="rubber-svg-container"[^<]*viewBox="0 0 260 420"[^>]*>.*?</svg>',
        rubber_svg,
        content,
        flags=re.DOTALL
    )

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"✅ Patched {os.path.basename(filepath)} (shot_id={shot_id})")


if __name__ == '__main__':
    shots = [
        'shot-01-setup.html',
        'shot-02-sync.html',
        'shot-03-adoption.html',
        'shot-04-strike.html',
        'shot-05-plasticity.html',
    ]
    for shot in shots:
        path = os.path.join(FRAMES_DIR, shot)
        if os.path.exists(path):
            patch_file(path)
        else:
            print(f"⚠️  Not found: {shot}")

    print("\n🎬 All rubber hand visuals upgraded to volumetric anatomical forms.")
