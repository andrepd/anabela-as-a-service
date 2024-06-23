import whisper
import sys

try:
	audio = whisper.load_audio(sys.argv[1])
except IndexError:
	print(f'Usage: {sys.argv[0]} audio_file', file=sys.stderr)
	exit(1)

print('Loaded audio', file=sys.stderr)

model = whisper.load_model("large", device="cpu")

print('Loaded model', file=sys.stderr)

tokenizer = whisper.tokenizer.get_tokenizer(multilingual=False)
other_tokens = [
	tokenizer.encode(' '+i)[0]
	for i in ['Navela', 'Moment']
]
print(other_tokens, file=sys.stderr)

number_tokens = [
    i 
    for i in range(tokenizer.eot)
    # if all(c in "0123456789" for c in tokenizer.decode([i]).strip().removesuffix('kg'))
    if any(c in "0123456789" for c in tokenizer.decode([i]))
]
print(len(number_tokens), file=sys.stderr)

print('Computed tokens to exclude', file=sys.stderr)

result = whisper.transcribe(
	model,
	audio,
	language="pt",
	word_timestamps=True,
	suppress_tokens=([-1] + number_tokens + other_tokens),
)

import json
print(json.dumps(result, indent = 2, ensure_ascii = False))