import sys

try:
    with open('timings.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines()]
except:
    sys.exit(0)
    
TOTAL_DURATION = float(lines[0])
frames = []
for line in lines[1:]:
    fid, start, duration = line.split(',')
    frames.append({"id": fid, "start": float(start), "duration": float(duration)})

html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Predictive Processing V4</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: "Playfair Display";
        font-style: normal;
        font-weight: 400 900;
        src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM86xQ.woff2) format("woff2");
      }}
      @font-face {{
        font-family: "Inter";
        font-style: normal;
        font-weight: 100 900;
        src: url(https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2) format("woff2");
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{ background: #000000; overflow: hidden; }}
      #root {{ width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #000000; }}
      .frame-track {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
    </style>
  </head>
  <body>
    <div data-hf-id="root" id="root" data-composition-id="predictive-processing-main" data-width="1080" data-height="1920" data-start="0" data-duration="{TOTAL_DURATION}">
"""

for i, fr in enumerate(frames):
    track = 1 if i % 2 == 0 else 2
    html += f'      <div data-hf-id="f0{i+1}" id="f0{i+1}" class="clip frame-track" data-composition-id="{fr["id"]}" data-composition-src="compositions/frames/{fr["id"]}.html" data-start="{fr["start"]}" data-duration="{fr["duration"]}" data-track-index="{track}" data-layout-allow-overlap></div>\n'

html += f"""
      <audio data-hf-id="audio-narration" id="audio-narration" src=".temp_audio/narration_full.wav" data-start="0" data-duration="{TOTAL_DURATION}" data-track-index="10" data-volume="1.0"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const masterTl = gsap.timeline({{ paused: true }});
      window.__timelines["predictive-processing-main"] = masterTl;
"""

for i in range(len(frames)):
    html += f'      const f0{i+1} = document.getElementById("f0{i+1}");\n'

html += "\n      // Cinematic crossfades\n"
for i in range(1, len(frames)):
    prev_id = f"f0{i}"
    curr_id = f"f0{i+1}"
    start = frames[i]["start"]
    html += f'      masterTl.fromTo({curr_id}, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power2.inOut" }}, {start});\n'
    html += f'      masterTl.to({prev_id}, {{ opacity: 0, duration: 0.5, ease: "power2.inOut" }}, {start});\n'

html += """    </script>
  </body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(html)
