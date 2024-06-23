import whisper
import sys

audio = whisper.load_audio("anabela.opus")

model = whisper.load_model("large", device="cpu")

tokenizer = whisper.tokenizer.get_tokenizer(multilingual=False)
other_tokens = [
	tokenizer.encode(" Navela")[0],
	tokenizer.encode(" Moment")[0],
]
print(other_tokens, file=sys.stderr)

number_tokens = [
    i 
    for i in range(tokenizer.eot)
    # if all(c in "0123456789" for c in tokenizer.decode([i]).strip().removesuffix('kg'))
    if any(c in "0123456789" for c in tokenizer.decode([i]))
]
print(len(number_tokens), file=sys.stderr)

result = whisper.transcribe(
	model,
	audio,
	language="pt",
	word_timestamps=True,
	suppress_tokens=([-1] + number_tokens + other_tokens),
)

import json
print(json.dumps(result, indent = 2, ensure_ascii = False))