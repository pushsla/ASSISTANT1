#!/usr/bin/python3
import requests
import os
import pyaudio
import wave

CHUNK = 1024


def synth(text):
	url = 'https://tts.voicetech.yandex.net/generate'
	params = {'text' : text,
			  'format' : 'wav',
			  'lang' : 'ru-RU',
			  'speaker' : 'zahar',
			  'key' : 'f1233cf8-c27a-4bad-9b5e-04f6ed2f265a'}
	req = requests.get(url, params = params)
	filename = 'synthesys.wav'
	with open(filename, 'wb') as file:
		file.write(req.content)

	wf = wave.open(filename, 'rb')

	p = pyaudio.PyAudio()

	# open stream (2)
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)

	# read data
	data = wf.readframes(CHUNK)

	# play stream (3)
	while len(data) > 0:
		stream.write(data)
		data = wf.readframes(CHUNK)

	# stop stream (4)
	stream.stop_stream()
	stream.close()

	# close PyAudio (5)
	p.terminate()
	wf.close()
	os.remove(filename)
	pass
	