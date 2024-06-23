import maas
import sys

try:
	text = sys.argv[1]
except IndexError:
	print(f'Usage: {sys.argv[0]} <text> [<file>]')
	exit(1)

try:
	file = sys.argv[2]
except IndexError:
	file = None

def play_from_file(text, file):
	for i in maas.search(file, text):
		maas.encode(i, file)

if file is not None:
	play_from_file(text, file)
else:
	from pathlib import Path
	for i in Path.glob('data/*.json'):
		play_from_file(text, i.basename())
