import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE = "/Users/anujbarve/Documents/gate-research/reference_clean.wav"

def get_duration(path):
    dur_result = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", path
    ], capture_output=True, text=True)
    return float(dur_result.stdout.strip())

def process_project(project_name, frames):
    print(f"\n=======================================================")
    print(f"Generating Narration for: {project_name}")
    print(f"=======================================================")
    
    project_dir = os.path.join(BASE_DIR, "projects", project_name)
    output_dir = os.path.join(project_dir, ".temp_audio")
    os.makedirs(output_dir, exist_ok=True)
    
    measurements = []
    current_start = 0.0
    crossfade = 0.5

    for frame in frames:
        raw_path = os.path.join(output_dir, f"{frame['id']}_raw.wav")
        synced_path = os.path.join(output_dir, f"{frame['id']}.wav")
        
        cmd = [
            "pocket-tts", "generate",
            "--voice", REFERENCE,
            "--text", frame["text"],
            "--output-path", raw_path,
            "--temperature", "0.1",
        ]
        env = os.environ.copy()
        env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        print(f"  [gen] {frame['id']}: \"{frame['text'][:60]}...\"")
        res = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [ERR] {frame['id']}: {res.stderr[-300:]}")
            sys.exit(1)
            
        tts_dur = get_duration(raw_path)
        offset = 0.5
        hold_buffer = 1.6
        frame_dur = max(tts_dur + offset + hold_buffer, 6.5)
        
        measurements.append({
            "id": frame["id"],
            "raw_path": raw_path,
            "tts_dur": tts_dur,
            "reveal_offset": offset,
            "duration": frame_dur,
            "start": current_start,
            "text": frame["text"]
        })
        current_start += (frame_dur - crossfade)

    # Master mix
    inputs = []
    filter_parts = []
    for i, m in enumerate(measurements):
        inputs.extend(["-i", m["raw_path"]])
        delay_ms = int((m["start"] + m["reveal_offset"]) * 1000)
        filter_parts.append(f"[{i}]adelay={delay_ms}|{delay_ms}[d{i}]")

    mix_inputs = "".join(f"[d{i}]" for i in range(len(measurements)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(measurements)}:duration=longest:dropout_transition=0[out]")
    filter_str = ";".join(filter_parts)
    narration_path = os.path.join(output_dir, "narration_full.wav")

    res = subprocess.run([
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[out]",
        "-ar", "24000", "-ac", "1",
        narration_path
    ], capture_output=True, text=True)
    
    if res.returncode != 0:
        print(f"[ERR] master mix: {res.stderr[-300:]}")
        sys.exit(1)
        
    master_dur = get_duration(narration_path)
    print(f"\n[OK] Master Narration: {master_dur:.2f}s")
    
    # Save timing manifest
    manifest_path = os.path.join(project_dir, "timing_manifest.json")
    import json
    with open(manifest_path, "w") as f:
        json.dump({
            "master_duration": master_dur,
            "frames": measurements
        }, f, indent=2)
    print(f"Saved manifest to {manifest_path}")

# DEFINITIONS FOR 3 VIDEOS
P1_FRAMES = [
    {
        "id": "01-hook",
        "text": "Every thought, every skill, and every obsession physically changes the cellular architecture of your brain. How does an abstract idea turn into solid biological circuitry?"
    },
    {
        "id": "02-origin",
        "text": "In nineteen forty-nine, Canadian psychologist Donald Hebb proposed a revolutionary biological law that redefined neuroscience forever."
    },
    {
        "id": "03-mechanism",
        "text": "Neurons that fire together, wire together. When two neurons repeatedly activate at the exact same moment, their synaptic connection strengthens and forms a permanent highway."
    },
    {
        "id": "04-cascade",
        "text": "The flip side is brutal. Neurons out of sync fail to link. The brain aggressively prunes away unused neural pathways to conserve vital metabolic energy."
    },
    {
        "id": "05-reframe",
        "text": "You are not stuck with the brain you were born with. Repetition acts like a physical chisel, carving permanent grooves into your neural landscape."
    },
    {
        "id": "06-lesson",
        "text": "Your habits are literally building physical brain circuits right now. Feed what you want to grow. Starve what you want to prune."
    }
]

P2_FRAMES = [
    {
        "id": "01-hook",
        "text": "For over a century, the greatest scientists believed the adult brain was completely hardwired, immutable, and incapable of physical repair."
    },
    {
        "id": "02-origin",
        "text": "Then came Edward Taub and Michael Merzenich. In groundbreaking primate experiments, they discovered something the medical establishment considered impossible."
    },
    {
        "id": "03-mechanism",
        "text": "When a limb is immobilized or injured, the brain does not leave that cortical real estate empty. Neighboring areas physically expand and colonize the silent territory."
    },
    {
        "id": "04-cascade",
        "text": "This gave birth to Constraint Induced Movement Therapy. By forcing patients to repeatedly use damaged limbs, they forced the adult brain to completely rewire its motor cortex."
    },
    {
        "id": "05-reframe",
        "text": "The brain is not a static machine with fixed hardware. It is dynamic, living neuro-cartography that constantly remaps itself based on demand."
    },
    {
        "id": "06-lesson",
        "text": "The takeaway? Your capacity is not fixed. Force the demand, and the biological hardware will reshape itself to meet you."
    }
]

P3_FRAMES = [
    {
        "id": "01-hook",
        "text": "To become a licensed London black cab driver, you must memorize twenty-five thousand streets and one hundred thousand landmarks. It is known simply as The Knowledge."
    },
    {
        "id": "02-origin",
        "text": "In the year two thousand, neuroscientist Eleanor Maguire scanned the brains of London cabbies using high resolution MRI technology."
    },
    {
        "id": "03-mechanism",
        "text": "The results shocked the scientific world. The posterior hippocampus, the brain's spatial navigation center, was significantly larger in drivers than in the general public."
    },
    {
        "id": "04-cascade",
        "text": "Even more astonishing, the size of their hippocampus grew in direct proportion to the number of years they had spent navigating the complex London streets."
    },
    {
        "id": "05-reframe",
        "text": "Intensive mental training does not just make you smarter. It physically expands the gray matter volume of targeted brain regions in real biological time."
    },
    {
        "id": "06-lesson",
        "text": "The mind is a muscle of staggering physical elasticity. Massive deliberate practice literally grows the brain you need."
    }
]

if __name__ == "__main__":
    process_project("hebbian-plasticity", P1_FRAMES)
    process_project("cortical-reorganization", P2_FRAMES)
    process_project("london-taxi-hippocampus", P3_FRAMES)
