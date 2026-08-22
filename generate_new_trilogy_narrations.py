import subprocess
import os
import sys
import json

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
    filter_parts.append(f"{mix_inputs}amix=inputs={len(measurements)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=7[out]")
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
    with open(manifest_path, "w") as f:
        json.dump({
            "master_duration": master_dur,
            "frames": measurements
        }, f, indent=2)
    print(f"Saved manifest to {manifest_path}")

P1_FRAMES = [
    {
        "id": "01-hook",
        "text": "Every minute you are awake, your brain builds trillions of new synaptic connections. But if this nonstop growth continued unchecked, your neural circuits would literally overheat and burn out."
    },
    {
        "id": "02-origin",
        "text": "In two thousand and three, neuroscientists Giulio Tononi and Chiara Cirelli formulated the groundbreaking Synaptic Homeostasis Hypothesis."
    },
    {
        "id": "03-mechanism",
        "text": "During deep slow-wave sleep, the brain performs global synaptic downsizing. It systematically weakens and prunes away noisy, trivial connections while preserving the vital signals."
    },
    {
        "id": "04-cascade",
        "text": "Without this nocturnal pruning, neural networks become oversaturated. Memory consolidation fails, cognitive processing drops, and cellular energy depletes rapidly."
    },
    {
        "id": "05-reframe",
        "text": "Sleep is not wasted downtime. Sleep is the biological price we pay for learning, clearing the canvas so you can think clearly tomorrow."
    },
    {
        "id": "06-lesson",
        "text": "Protect your sleep like your brain depends on it. Because without deep restoration, you are operating on a cluttered, oversaturated circuit."
    }
]

P2_FRAMES = [
    {
        "id": "01-hook",
        "text": "Within forty-eight hours of learning something new, your brain will silently erase nearly seventy percent of it. Why is human memory so fragile?"
    },
    {
        "id": "02-origin",
        "text": "In eighteen eighty-five, German psychologist Hermann Ebbinghaus conducted the first rigorous scientific study of memory, discovering the mathematical Forgetting Curve."
    },
    {
        "id": "03-mechanism",
        "text": "Memory decays exponentially over time. But if you actively retrieve the information just before you forget it, the decay curve instantly resets and flattens."
    },
    {
        "id": "04-cascade",
        "text": "Passive re-reading tricks your brain into a false illusion of mastery. Spaced retrieval creates desirable difficulty, forcing the brain to reinforce long-term structural storage."
    },
    {
        "id": "05-reframe",
        "text": "Forgetting is not a flaw in your biology. It is an intelligent filtering algorithm. Active recall is how you signal what is too important to delete."
    },
    {
        "id": "06-lesson",
        "text": "Stop cramming in single marathon sessions. Space out your reviews, test your recall, and lock knowledge into permanent memory."
    }
]

P3_FRAMES = [
    {
        "id": "01-hook",
        "text": "World-class masters do not just have better ideas. Their brains transmit electrical nerve impulses up to one hundred times faster than average."
    },
    {
        "id": "02-origin",
        "text": "Neuroscientists discovered that deliberate practice triggers specialized glial cells called oligodendrocytes to wrap nerve fibers in insulating myelin sheaths."
    },
    {
        "id": "03-mechanism",
        "text": "Uninsulated axons leak electrical charge and crawl at barely two miles per hour. Thickly myelinated axons supercharge signals up to two hundred miles per hour."
    },
    {
        "id": "04-cascade",
        "text": "Every time you push to the edge of your ability and correct errors, another microscopic layer of myelin is wrapped around that exact circuit."
    },
    {
        "id": "05-reframe",
        "text": "Talent is not an inborn mystical trait. Talent is the physical accumulation of myelin insulation built through thousands of reps of deliberate focus."
    },
    {
        "id": "06-lesson",
        "text": "Embrace the struggle of difficult practice. Precision and focused repetition are physically wrapping the high-speed cables of mastery."
    }
]

if __name__ == "__main__":
    process_project("synaptic-pruning", P1_FRAMES)
    process_project("ebbinghaus-forgetting-curve", P2_FRAMES)
    process_project("myelination-speed", P3_FRAMES)
