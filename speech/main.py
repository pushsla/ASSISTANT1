import start_request
import os
import quest
import synthesis

command2 = ''
while True:
	command1 = start_request.listen_for_speech()
	os.remove('command.pcm')
	if command1 == 'кирпич':
		print("I'm listening, my Owner!")
		command2 = start_request.listen_for_speech()
		print(command2)
		os.remove('command.pcm')
		answer = quest.main(command2)
		print(answer)
		synthesis.synth(answer)
	else:
		continue