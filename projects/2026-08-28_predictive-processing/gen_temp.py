import subprocess
import os

REFERENCE = "../../reference_clean.wav"
OUTPUT_DIR = ".temp_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

frames = [
    {"id": "01", "text": "You think you're seeing this video right now. You aren't."},
    {"id": "02", "text": "We used to think perception worked like a camera. Light enters the eye, travels to the back of the brain, and builds a picture. But neuroscientists noticed something strange. The physical wiring goes the wrong way."},
    {"id": "03", "text": "Your brain doesn't wait to see the world. It predicts what you are about to perceive, a fraction of a second before it happens. It projects a guess. Your senses don't tell your brain what is there. They only report the errors."},
    {"id": "04", "text": "If the guess matches the input, no information travels up. You only process the surprises. This is why you can miss a typo you've stared at for hours. If the expectation is strong enough, your brain literally overrides your eyes."},
    {"id": "05", "text": "You aren't experiencing objective reality. You are experiencing your brain's expectation of reality, constantly corrected by the world."}
]

total = 0
for f in frames:
    raw_path = os.path.join(OUTPUT_DIR, f"{f['id']}_raw.wav")
    env = os.environ.copy()
    env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    subprocess.run([
        "pocket-tts", "generate",
        "--voice", REFERENCE,
        "--text", f["text"],
        "--output-path", raw_path,
        "--temperature", "0.1"
    ], env=env, capture_output=True)
    
    dur_res = subprocess.run([
        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
        "-of", "csv=p=0", raw_path
    ], capture_output=True, text=True)
    
    dur = float(dur_res.stdout.strip())
    print(f"Frame {f['id']}: {dur:.2f}s")
    total += dur

print(f"Total pure speech: {total:.2f}s")
