import json
import sys
import subprocess

class Segment:
	def __init__(self, text, start, end):
		self.text = text
		self.start = start
		self.end = end

	def __str__(self):
		return f'{self.start:.3f} | {self.text}'

	# def __repr__(self):
	# 	return str(self)

def get_segments(file):
	with open(file) as f:
		db = json.load(f)
		return [
			Segment(segment['text'].strip(), segment['start'], next_segment['start'])
			for segment, next_segment in zip(db['segments'], db['segments'][1:])
		]

def search(file, text):
	'''Search for text in file. Return start and stop timestamp, or None'''
	pass

###

def manual_fixes(text):
	return (
		text
			.replace('Ana Bela', 'Anabela')
	)

def manual_fix(segment):
	return Segment(manual_fixes(segment.text), segment.start, segment.end)

###

def encode(segment):
	cmd = f'ffmpeg -i audio/{sys.argv[1]}.opus -ss {segment.start} -to {segment.end} -c copy -f opus - | ffplay -'
	subprocess.run(cmd, shell=True)

###

for i in get_segments(f'data/{sys.argv[1]}.json'):
	print(manual_fix(i))
	if sys.argv[2] in i.text.lower():
		encode(i)
