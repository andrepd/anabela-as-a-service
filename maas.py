import json
import sys
import subprocess
import tempfile
import time
from playsound import playsound

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

def encode(segment, file):
	# with tempfile.TemporaryFile() as output:
	output = 'akjwebfwejh.opus'

	cmd = f'ffmpeg -y -i audio/{file}.opus -ss {segment.start} -to {segment.end} -c copy -f opus {output}'
	print(cmd)
	subprocess.run(cmd, shell=True)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	# cmd = f'command xdg-open {output}'
	# print(cmd)
	# subprocess.run(cmd, shell=True)#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	# # time.sleep(10)

	playsound(output)
	time.sleep(1)
