import os
from pathlib import Path

# Load .env into os.environ if present
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            val = val.strip().strip("'\"")
            if val:
                os.environ[key.strip()] = val

from sarvamai import SarvamAI

client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

response = client.chat.completions(
    model="sarvam-105b-conversations",
    messages=[
        {"role": "user", "content": "Hello! Introduce yourself in one sentence."}
    ],
)

print(response.choices[0].message.content)

