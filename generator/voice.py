import subprocess
from pathlib import Path

def synthesize(text, output_path: Path):
    # espeak-ng is installed on the GitHub runner; no external paid TTS API.
    subprocess.run(
        ["espeak-ng", "-v", "en-us", "-s", "155", "-p", "48", "-a", "175", "-w", str(output_path), text],
        check=True,
        capture_output=True,
        text=True
    )
