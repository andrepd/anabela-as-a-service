import whisper_timestamped as whisper

audio = whisper.load_audio("anabela.opus")

model = whisper.load_model("large", device="cpu")

result = whisper.transcribe(model, audio, language="pt")

import json
print(json.dumps(result, indent = 2, ensure_ascii = False))