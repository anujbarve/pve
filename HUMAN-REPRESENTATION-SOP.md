# Specialized Standard Operating Procedure (SOP): Human Representation & Anatomy

A specialized standard operating procedure for depicting human figures, hands, eyes, faces, and anatomical structures in cinematic explainer films and visual essays.

---

## 🚨 THE CORE PRINCIPLE: ZERO AI IMAGINATION — STRICTLY USE SVG / PNG FILES

> **The Golden Law:** **Never let the AI "imagine" or draw human anatomy from scratch.** 
> An LLM cannot draw human bodies, hands, fingers, or eyes. It must **always use actual, pre-existing `.svg` or `.png` asset files** sourced from standard vector/icon libraries (Flaticon, The Noun Project, Phosphor Icons, FontAwesome, Wikimedia Commons, or scientific archives).
>
> **The Division of Labor:**
> 1. **The Asset (`assets/*.svg` / `assets/*.png`)**: Provides the authentic, mathematically correct, and proportional human anatomy.
> 2. **The AI / Code**: ONLY handles **theming, lighting, and animation** (applying the Editorial Dark Mode gradients, rim lighting, glow filters, and GSAP motion). It NEVER draws the geometry.


---

## 1. Why the Previous Approaches Failed

### The Two Historic Failures:

```
❌ FAILURE MODE A: The "Abstract Evasion" (Orb / Sensor Pad Trap)
   Problem: Stripping all human elements and replacing people/hands with glowing circles or 
            engineering sensor pads (e.g., Change Blindness using "Identity Token Orbs", 
            Rubber Hand using "Tactile Input Sensor Pads").
   Why it fails: Destroys the "Reality-First Entry Point" doctrine. Audiences cannot empathize 
                 with or instinctively understand an abstract sensor pad the way they feel a 
                 human hand or see a real social interaction.

❌ FAILURE MODE B: The "Toddler Bézier" (AI-Invented Paths)
   Problem: Asking an LLM to write raw SVG Bézier curves from scratch 
            (e.g., `M68 338 C48 305 42 265...`).
   Why it fails: Results in deformed fingers, crooked skull profiles, alien-like posture, 
                 and an amateurish, uncalibrated visual aesthetic that instantly breaks immersion.
```

### The Standardized Solution:
Use **curated, geometrically verified vector archetypes** (standardized vector geometry from top-tier iconographic and anatomical standards) and elevate them into high-end, volumetric, editorial dark mode assets via **layered radial gradients, directional rim lighting, glow filters, and articulated GSAP rigging**.

---

## 2. Asset File Management & Mandatory Download Workflow

### 🚨 THE HARD RULE: 100% SOURCED FILES — ZERO AI DRAWING
Every vector asset MUST be an actual file downloaded into `projects/<project>/assets/<name>.svg` before writing the shot HTML. The AI is strictly forbidden from writing or imagining raw SVG `<path>` coordinates.

### The Mandatory `curl` Sourcing Cookbook:
Use the **Iconify API** (which gives immediate access to FontAwesome, Material Design Icons, Phosphor, Lucide, Fluent) to pull authentic, mathematically correct vectors directly into `assets/`:

```bash
# 1. Hands & Gestures
curl -s "https://api.iconify.design/mdi:hand-back-left.svg?color=%2338BDF8" > assets/hand_left.svg
curl -s "https://api.iconify.design/mdi:hand-back-right.svg?color=%23F2D24B" > assets/hand_right.svg
curl -s "https://api.iconify.design/fa6-solid:hand.svg?color=%23F2F1EC" > assets/hand_open.svg
curl -s "https://api.iconify.design/fa6-solid:hand-pointer.svg?color=%23F2D24B" > assets/hand_pointer.svg

# 2. Human Figures, People & Workers
curl -s "https://api.iconify.design/fa6-solid:person.svg?color=%2338BDF8" > assets/figure_standing.svg
curl -s "https://api.iconify.design/fa6-solid:person-walking.svg?color=%23F2D24B" > assets/figure_walking.svg
curl -s "https://api.iconify.design/fa6-solid:people-carry-box.svg?color=%23F2D24B" > assets/workers_carrying.svg
curl -s "https://api.iconify.design/fa6-solid:user.svg?color=%23F2F1EC" > assets/user_avatar.svg

# 3. Sensory, Eyes & Anatomy
curl -s "https://api.iconify.design/fa6-solid:eye.svg?color=%2338BDF8" > assets/eye.svg
curl -s "https://api.iconify.design/ph:brain-fill.svg?color=%23F2D24B" > assets/brain.svg
curl -s "https://api.iconify.design/ph:heart-straight-fill.svg?color=%23D4622B" > assets/heart.svg

# 4. Physical Tools & Objects
curl -s "https://api.iconify.design/fa6-solid:paintbrush.svg?color=%23F2D24B" > assets/paintbrush.svg
curl -s "https://api.iconify.design/fa6-solid:hammer.svg?color=%23CBD5E1" > assets/hammer.svg
curl -s "https://api.iconify.design/fa6-solid:door-closed.svg?color=%2392400E" > assets/door.svg
```

### Approved Icon Collection Prefixes:
* `fa6-solid:` (FontAwesome 6 Solid — highest quality silhouettes and figures)
* `mdi:` (Material Design Icons — rich anatomical hands, gestures, body parts)
* `ph:` (Phosphor Icons — clean, modern icons and anatomical shapes)
* `lucide:` (Lucide / Feather Icons — minimalist technical line art)
* `fluent:` (Microsoft Fluent System Icons)



---

## 3. The "Editorial Dark Mode" Skinning Pipeline

Do not display flat, primary-colored clip art. Every vector must undergo the **4-Layer Cinematic Skinning Process**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. BASE VOLUMETRIC CORE (Dark Slate / Obsidian Radial Fill)            │
│    radial-gradient(#151D2A 0%, #080C14 70%, #020408 100%)              │
├────────────────────────────────────────────────────────────────────────┤
│ 2. DIRECTIONAL RIM LIGHT (Linear Edge Glow)                            │
│    Warm Gold (#F2D24B) for focus/prosthetic, Electric Cyan (#38BDF8)   │
│    for neural/real, Bone White (#F2F1EC) for biological structure      │
├────────────────────────────────────────────────────────────────────────┤
│ 3. SUBSURFACE SCATTER (Soft Internal Alpha Glow)                       │
│    Feathered radial blur layer mimicking skin/translucency             │
├────────────────────────────────────────────────────────────────────────┤
│ 4. ARTICULATION & TACTILE NODES (Kinematic Reticles)                   │
│    Glow dots at knuckle joints, foveal focal points, neural impulses   │
└────────────────────────────────────────────────────────────────────────┘
```

### Standard SVG Defs Template:

```html
<svg style="display: none;">
  <defs>
    <!-- Neural Real Limb Shading (Cyan Palette) -->
    <radialGradient id="grad-human-neural" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#0E2238" />
      <stop offset="70%" stop-color="#060F1A" />
      <stop offset="100%" stop-color="#02060B" />
    </radialGradient>
    <linearGradient id="rim-neural" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="rgba(56, 189, 248, 0.85)" />
      <stop offset="40%" stop-color="rgba(56, 189, 248, 0.2)" />
      <stop offset="100%" stop-color="rgba(56, 189, 248, 0.02)" />
    </linearGradient>

    <!-- Synthetic / Prosthetic / Attention Shading (Gold Palette) -->
    <radialGradient id="grad-human-gold" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#2D2208" />
      <stop offset="70%" stop-color="#140F03" />
      <stop offset="100%" stop-color="#050301" />
    </radialGradient>
    <linearGradient id="rim-gold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="rgba(242, 210, 75, 0.9)" />
      <stop offset="40%" stop-color="rgba(242, 210, 75, 0.25)" />
      <stop offset="100%" stop-color="rgba(242, 210, 75, 0.02)" />
    </linearGradient>

    <!-- Cinematic Glow Filter -->
    <filter id="glow-cinematic" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
</svg>
```

---

## 4. Standardized Vector Archetype Catalog

### 4.1 Hands & Tactile Gestures (Top-Down Dorsal / Palmar)

Used in: **Rubber Hand Illusion, Predictive Reach, Tactile Binding, Tool Extension**.

```html
<!-- Standardized Anatomical Hand (Normalized 512x512 FlatIcon/Standard Vector Archetype) -->
<svg class="human-hand-vector" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Wrist Base -->
  <path class="hand-wrist" d="M210 460 C205 410, 205 380, 210 350 L302 350 C307 380, 307 410, 302 460 Z"
        fill="url(#grad-human-neural)" stroke="url(#rim-neural)" stroke-width="2.5" />
  
  <!-- Palm Volume -->
  <path class="hand-palm" d="M190 350 C160 310, 150 250, 160 200 C168 160, 195 145, 220 140 C235 125, 275 125, 290 140 C315 145, 345 160, 352 200 C362 250, 352 310, 322 350 Z"
        fill="url(#grad-human-neural)" stroke="url(#rim-neural)" stroke-width="2.5" />
  
  <!-- Thumb (Articulated Group) -->
  <g id="digit-thumb" class="hand-digit">
    <path d="M165 260 C135 240, 105 210, 90 175 C80 150, 95 130, 115 135 C135 140, 150 170, 162 205 Z"
          fill="url(#grad-human-neural)" stroke="url(#rim-neural)" stroke-width="2" />
    <circle cx="102" cy="155" r="4" fill="#38BDF8" filter="url(#glow-cinematic)" />
  </g>

  <!-- Index Finger -->
  <g id="digit-index" class="hand-digit">
    <path d="M192 145 C186 115, 182 80, 186 45 C190 25, 210 25, 216 45 C222 80, 220 115, 218 145 Z"
          fill="url(#grad-human-neural)" stroke="url(#rim-neural)" stroke-width="2" />
    <circle cx="201" cy="40" r="4" fill="#38BDF8" filter="url(#glow-cinematic)" />
  </g>

  <!-- Middle Finger -->
  <g id="digit-middle" class="hand-digit">
    <path d="M228 140 C225 105, 224 65, 228 30 C232 10, 252 10, 256 30 C260 65, 259 105, 256 140 Z"
          fill="url(#grad-human-neural)" stroke="url(#rim-neural)" stroke-width="2.5" />
    <circle cx="242" cy="22" r="4" fill="#38BDF8" filter="url(#glow-cinematic)" />
  </g>

  <!-- Ring Finger -->
  <g id="digit-ring" class="hand-digit">
    <path d="M266 145 C264 115, 264 80, 268 50 C272 32, 290 32, 294 50 C298 80, 296 115, 292 145 Z"
          fill="url(#grad-human-neural)" stroke="url(#rim-neural)" stroke-width="2" />
    <circle cx="281" cy="45" r="4" fill="#38BDF8" filter="url(#glow-cinematic)" />
  </g>

  <!-- Little Finger -->
  <g id="digit-pinky" class="hand-digit">
    <path d="M302 165 C304 140, 310 110, 318 85 C324 70, 340 72, 342 88 C344 112, 338 140, 332 165 Z"
          fill="url(#grad-human-neural)" stroke="url(#rim-neural)" stroke-width="2" />
    <circle cx="330" cy="80" r="4" fill="#38BDF8" filter="url(#glow-cinematic)" />
  </g>

  <!-- Tactile Receptive Field Lines -->
  <path d="M256 340 Q256 220 242 35" stroke="rgba(56, 189, 248, 0.3)" stroke-width="1.5" stroke-dasharray="4 6" />
</svg>
```

---

### 4.2 Full-Body Figure Silhouettes (Social Interaction & Pedestrians)

Used in: **Change Blindness (Door Experiment), Decision Fatigue (Judge & Defendant), Broken Windows, Spotlight Effect**.

```html
<!-- Standardized Proportional Human Figure (Normalized 140x480 Silhouette) -->
<svg class="human-figure-vector" viewBox="0 0 140 480" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Head (Proportional Oval) -->
  <circle cx="70" cy="45" r="28" fill="url(#grad-human-gold)" stroke="url(#rim-gold)" stroke-width="2" />
  
  <!-- Neck -->
  <path d="M64 73 L64 88 L76 88 L76 73 Z" fill="#0C121D" />
  
  <!-- Torso / Jacket -->
  <path class="figure-torso" d="M42 90 C42 85, 98 85, 98 90 L106 195 L102 270 C102 276, 38 276, 38 270 L34 195 Z"
        fill="url(#grad-human-gold)" stroke="url(#rim-gold)" stroke-width="2" />
  
  <!-- Left Arm (Braced/Pockets) -->
  <path class="figure-arm-left" d="M40 95 C28 115, 24 160, 30 190 C34 200, 44 195, 46 185 L50 120 Z"
        fill="#090E17" stroke="rgba(242, 210, 75, 0.4)" stroke-width="1.5" />
  
  <!-- Right Arm (Gesticulating / Speaking) -->
  <path class="figure-arm-right" d="M100 95 C115 110, 130 135, 132 165 C132 175, 122 178, 116 168 L104 125 Z"
        fill="#090E17" stroke="url(#rim-gold)" stroke-width="1.5" />
  
  <!-- Legs / Stride -->
  <path class="figure-legs" d="M42 272 L38 440 L56 440 L66 315 L74 315 L84 440 L102 440 L98 272 Z"
        fill="#05080F" stroke="rgba(242, 241, 236, 0.3)" stroke-width="1.5" />
</svg>
```

---

### 4.3 Sensory Profile & Eye Architecture (Gaze, Fovea, Saccade)

Used in: **Change Blindness (Foveal Cone), Chronostasis (Saccadic Suppression), Spotlight Effect (Social Gaze)**.

```html
<!-- Standardized Profile Head & Anatomical Optical Rig -->
<svg class="sensory-eye-rig" viewBox="0 0 920 660" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 2-Degree Foveal Focus Spotlight -->
    <linearGradient id="fovea-laser" x1="160" y1="330" x2="880" y2="330" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F2D24B" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#F2D24B" stop-opacity="0.1" />
    </linearGradient>
  </defs>

  <!-- Peripheral Vision Cone (Blur/Void Field) -->
  <path d="M160 330 L880 80 L880 580 Z" fill="rgba(56, 189, 248, 0.04)" stroke="rgba(56, 189, 248, 0.25)" stroke-width="1.5" stroke-dasharray="6 6" />

  <!-- Razor 2° Foveal Spotlight -->
  <polygon points="160,330 880,305 880,355" fill="url(#fovea-laser)" />

  <!-- Proportional Profile Head Silhouette -->
  <g id="head-profile" transform="translate(20, 180)">
    <!-- Standardized Cranial Contour -->
    <path d="M30 280 C28 240, 32 190, 42 160 C55 120, 85 70, 125 60 C155 52, 172 65, 178 85 C182 98, 175 115, 180 125 C190 135, 198 140, 192 152 C184 160, 176 160, 180 170 C186 180, 178 192, 166 195 C158 198, 160 215, 168 225 C158 240, 130 260, 120 290 Z"
          fill="#0A0E17" stroke="rgba(56, 189, 248, 0.8)" stroke-width="2" />
    
    <!-- Cornea & Iris Lens Structure -->
    <path d="M172 135 C176 130, 184 130, 188 135 C184 140, 176 140, 172 135 Z" fill="#38BDF8" />
    <circle cx="180" cy="135" r="4" fill="#F2D24B" filter="url(#glow-cinematic)" />
  </g>
</svg>
```

---

## 5. GSAP Articulation & Animation Standard

When animating human anatomy, follow kinematic physics:

1. **Set Precise `transformOrigin`**:
   - Wrist / Hand: `transformOrigin: "50% 100%"` (rotates from the wrist, not center of hand).
   - Forearm / Elbow: `transformOrigin: "50% 0%"`.
   - Eyeball / Pupil: `transformOrigin: "50% 50%"`.
   - Finger Phalanges: `transformOrigin: "50% 100%"`.

2. **Kinematic Decoupling**:
   - When reaching, move the arm/body first, followed by a slight rotational delay on the hand (`ease: "power2.out"`).
   - For eye gaze shifts (saccades), snap instantaneously (`duration: 0.08`, `ease: "power4.out"`), followed by a subtle micro-drift.

```js
// Example: Synchronous Tactile Brushstroke & Somatosensory Pulse
const tl = gsap.timeline({ paused: true });

// 1. Brush strokes sweep simultaneously across both real & rubber hands
tl.to(".brush-stroke-vector", {
  y: 120,
  duration: 1.4,
  ease: "power1.inOut",
  repeat: 3,
  yoyo: true
}, 0.5);

// 2. Tactile impulses radiate up the neural tract from fingertips
tl.fromTo(".tactile-pulse-node", 
  { scale: 0, opacity: 1 },
  { scale: 3, opacity: 0, stagger: 0.2, duration: 0.8, ease: "power2.out" },
  0.7
);
```

---

## 6. Case Study Audits: Before vs. After

### Case Study 1: The Rubber Hand Illusion (`2026-09-03_rubber-hand-illusion`)

| Dimension | Previous Mistake | Standardized SOP Solution |
|---|---|---|
| **Real Hand** | Replaced by a flat dashed square (`pad-real` with "Limb Occluded" badge). | Standardized anatomical left hand with cyan neural tractography (`#38BDF8`), ghosted behind the partition. |
| **Rubber Hand** | Hand-coded crooked SVG Bézier curves with uneven finger thicknesses. | Standardized proportional right hand skinned in warm prosthetic amber (`#F2D24B`) with tactile joint nodes. |
| **Tactile Binding** | Abstract coordinate pulses in the void. | Realistic animated brush vectors applying synchronous physical strokes along corresponding index fingers. |
| **Hammer Strike** | A rectangle sliding down onto an abstract sensor pad. | Heavy metal hammer silhouette delivering a high-velocity physical impact directly above the adopted rubber hand, triggering autonomic pulse waves. |

---

### Case Study 2: Change Blindness (`2026-09-06_change-blindness`)

| Dimension | Previous Mistake | Standardized SOP Solution |
|---|---|---|
| **Direction Giver & Stranger A** | Abstract colored circles (`Token A`, `Token B1`) connected by a neon line. | Two proportional human silhouettes (Direction Giver in cyan rim light, Stranger A in warm amber jacket) facing each other in natural conversation poses. |
| **The Swap Mechanism** | A black slab sliding past two glowing dots. | Two standardized worker silhouettes carrying an authentic wooden door slab physically occluding the conversation partner. |
| **Stranger B Replacement** | An orb changing color from amber to red. | Stranger B (distinct height, different coat silhouette) emerging from behind the door slab while the Direction Giver remains oblivious. |
| **Foveal Vision Arc** | Diagrammatic chart box. | Anatomical profile silhouette projecting an authentic 2° golden laser cone against a blurred 178° peripheral field. |

---

## 7. Quality Gate: The Anatomy Litmus Test

Before rendering any video featuring human figures or body parts:

- [ ] **Zero Freehand Béziers**: No raw, hand-invented anatomical coordinate strings. All paths originate from verified vector archetypes.
- [ ] **Editorial Dark Mode Skinning**: Every body part has a deep volumetric gradient core + directional rim lighting (`#F2D24B` or `#38BDF8`) + subtle glow.
- [ ] **Anatomical Proportions**: Human figures maintain proper 1:7.5 head-to-body ratios; hands have 5 distinct proportional digits with correct phalange lengths.
- [ ] **Proper Kinematic Pivot**: GSAP `transformOrigin` matches real joint mechanics (wrist at base, elbow at top, neck at collar).
- [ ] **No Card Enclosures**: Human figures interact directly within the full-bleed 1080×1920 spatial environment.
