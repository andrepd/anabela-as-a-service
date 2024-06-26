import json
import sys
import subprocess
import uuid
from pathlib import Path

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
	print(file, text)
	for i in get_segments(f'data/{file}.json'):
		# print(manual_fix(i))
		if text in i.text.lower():
			yield i

###

def manual_fixes(text):
	return (
		text
			.replace('Ana Bela', 'Anabela')
	)

def manual_fix(segment):
	return Segment(manual_fixes(segment.text), segment.start, segment.end)

###

def extract_audio(file, segment):
	input = list(Path('audio').glob(f'{file}.*'))[0]
	output = f'{uuid.uuid1()}{input.suffix}'

	cmd = f'ffmpeg -y -i {input} -ss {segment.start} -to {segment.end} -c copy {output}'
	print(cmd)
	subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	return output
