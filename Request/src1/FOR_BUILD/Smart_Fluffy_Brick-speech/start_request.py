#!/usr/bin/python3
import pyaudio
import wave
import audioop
from collections import deque
import os
import requests
import time
import math
import xml.etree.ElementTree as xmlt


url = 'https://asr.yandex.net/asr_xml'
params = {'uuid':'34353bf726ff4ea885eea4164d3ab413',
			  'key' : 'f1233cf8-c27a-4bad-9b5e-04f6ed2f265a',
			  'topic' : 'queries', 
			  'lang': 'ru-RU'}
headers = {"Content-Type": "audio/x-pcm;bit=16;rate=16000"}

# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 2500  # The threshold intensity that defines silence
				  # and noise signal (an int. lower than THRESHOLD is silence).

SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
				   # only silence is recorded. When this time passes the
				   # recording finishes and the file is delivered.

PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
				  # is detected, how much of previously recorded audio is
				  # prepended. This helps to prevent chopping the beggining
				  # of the phrase.


def audio_int(num_samples=50):
	""" Gets average audio intensity of your mic sound. You can use it to get
		average intensities while you're talking and/or silent. The average
		is the avg of the 20% largest intensities recorded.
	"""

	print ("Getting intensity values from mic.")
	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
			  for x in range(num_samples)] 
	values = sorted(values, reverse=True)
	r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
	print (" Finished ")
	print (" Average audio intensity is ", r)
	stream.close()
	p.terminate()
	return r


def listen_for_speech(threshold=THRESHOLD, num_phrases=1):
	"""
	Listens to Microphone, extracts phrases from it and sends it to 
	Google's TTS service and returns response. a "phrase" is sound 
	surrounded by silence (according to threshold). num_phrases controls
	how many phrases to process before finishing the listening process 
	(-1 for infinite). 
	"""

	#Open stream
	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	print ("* Listening mic. ")
	audio2send = []
	cur_data = ''  # current chunk  of audio data
	rel = int(RATE/CHUNK)
	slid_win = deque(maxlen=SILENCE_LIMIT * rel)
	#Prepend audio from 0.5 seconds before noise was detected
	prev_audio = deque(maxlen=int(PREV_AUDIO * rel)) 
	started = False
	n = num_phrases
	response = []

	while (num_phrases == -1 or n > 0):
		cur_data = stream.read(CHUNK)
		slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
		#print slid_win[-1]
		if(sum([x > THRESHOLD for x in slid_win]) > 0):
			if(not started):
				print ("Starting record of phrase")
				started = True
			audio2send.append(cur_data)
		elif (started is True):
			print ("Finished")
			# The limit was reached, finish capture and deliver.
			filename = save_speech(list(prev_audio) + audio2send, p)
			# Send file to Google and get response
			r = stt_google_wav(filename) 
			# Reset all
			started = False
			slid_win = deque(maxlen=SILENCE_LIMIT * rel)
			prev_audio = deque(maxlen=int(0.5 * rel) )
			audio2send = []
			n -= 1
		else:
			prev_audio.append(cur_data)

	print ("* Done recording")
	stream.close()
	p.terminate()

	return r


def save_speech(data, p):
	""" Saves mic data to temporary WAV file. Returns filename of saved 
		file """

	filename = 'command'
	# writes data to WAV file
	data = b''.join(data)
	wf = wave.open(filename + '.pcm', 'wb')
	wf.setnchannels(1)
	wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
	wf.setframerate(16000)  # TODO make this value a function parameter?
	wf.writeframes(data)
	wf.close()
	pass


def stt_google_wav(audio_fname):
	""" Sends audio file (audio_fname) to Google's text to speech 
		service and returns service's response. We need a FLAC 
		converter if audio is not FLAC (check FLAC_CONV). """

   
	with open('command.pcm', 'rb') as file1:
		files = {'file': file1.read()}

	
	print ("Sending request to Yandex SK")
	req = requests.post(url, params = params, headers=headers, files = files)
	try:
		 response = req.text
		 income_xml = xmlt.fromstring(req.text)
		 command = income_xml[0].text
	except:
	   print ("Couldn't parse service response")
	   command = 'динахуй блять'

	return command


if(__name__ == '__main__'):
	print(listen_for_speech())
	os.remove('command.pcm')