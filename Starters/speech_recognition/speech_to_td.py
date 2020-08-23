#!/usr/bin/env python3

# todo:
# * Feature for selecting a specific cloud service.
# * Improve latency?
# * Timeout, noise level etc. parameters

import argparse

parser = argparse.ArgumentParser(description='Use a microphone to record a speaker, convert the \
	speech to text using a cloud services API, and send the text to TouchDesigner via UDP.')
parser.add_argument('--udp_port', dest='udp_port', type=int, default=9010,
	help='The UDP Port for TouchDesigner')
parser.add_argument('--udp_ip', dest='udp_ip', type=str, default="127.0.0.1",
	help='The UDP IP Address for TouchDesigner')
parser.add_argument('--timeout', dest='timeout', type=float, default=None,
	help='The timeout for the speech recognition listener.')
parser.add_argument('--pause_threshold', dest='pause_threshold', type=float, default=.8,
	help='The threshold time of silence before the speech recognizer tries conversion.')
parser.add_argument('--language',dest='language', type=str,
	choices=['en-US','es-US','fr-FR','ja-JP','ko-KR'], default='en-US')

args = parser.parse_args()

import speech_recognition as sr
from socket import *

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
UDP_PORT = args.udp_port
UDP_IP = args.udp_ip
TIMEOUT = args.timeout
PAUSE_THRESHOLD = args.pause_threshold
LANGUAGE = args.language

addr = (UDP_IP, UDP_PORT)

import os
WIT_AI_KEY = os.getenv('KEY_WIT_AI')
if WIT_AI_KEY is None:
	raise Exception('You must set the environment variable for KEY_WIT_AI')

def handle_source(source):
	print("Say something!")
	audio = r.listen(source, timeout=TIMEOUT)
	print('The cloud will parse what you said.')

	try:
		text = r.recognize_wit(audio, key=WIT_AI_KEY)
		# text = r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY",language=LANGUAGE)
		print("The cloud thinks you said: " + text)

		# Send over UDP.
		# To receive this message,
		# TouchDesigner UDP In DAT row/callback format should be set to One Per Message.
		encoded = text.encode('utf-8')
		clientSocket.sendto(encoded, addr)

	except sr.UnknownValueError:
		print("Could not understand audio")
	except sr.RequestError as e:
		print("Could not request results; {0}".format(e))

# obtain audio from the microphone
r = sr.Recognizer()
r.pause_threshold = PAUSE_THRESHOLD

with sr.Microphone() as source:
	while True:
		handle_source(source)
