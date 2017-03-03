#!/usr/bin/python3
import requests
import xml.etree.ElementTree as xmlt
import CmdRecorder as rec

def getCommand():

	url = 'https://asr.yandex.net/asr_xml'
	params = {'uuid':'34353bf726ff4ea885eea4164d3ab413',
			  'key' : 'f1233cf8-c27a-4bad-9b5e-04f6ed2f265a',
	          'topic' : 'queries', 
	          'lang':'ru-RU'}
	headers = {"Content-Type": "audio/x-pcm;bit=16;rate=16000"}
	#rec.recordCommand()

	with open('../command.pcm', 'rb') as file1:
		files = {'file': file1.read()}
	req = requests.post(url, params = params, headers = headers, files = files)
	try:
		income_xml = xmlt.fromstring(req.text)
		command = income_xml[0].text
		return(command)
	except:
		return "Couldn's recognise"

print(getCommand())