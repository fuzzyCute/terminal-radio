#!/usr/bin/env python
#-*- coding:utf-8 -*-

__version__ = "0.0.over9000_zeroez.1.2"
__author__ = "fuzzyCute"
__license__ = "OpenSource"

import radio_programming as radio, signal

signal.signal(signal.SIGINT, radio.signal_handler)

radio.create_files()

print (radio.spaces)

print (radio.start)

while True:
	if len(radio.previous_radio) != 0:
		print("Last Radio Played:",radio.previous_radio[0])
		print("Type 'last radio' to play last radio")
	user_input = input(radio.user_input_prompt)
	if user_input in radio.start_commands or user_input.startswith("search genre") or user_input.startswith("search radio"):
		# HELP MENU
		if user_input == radio.start_commands[3]:
			radio.getHelp()
		
		# GENRES MENU
		elif user_input == radio.start_commands[0]:
			genre = radio.genres_menu()
			if genre != "home":
				id_radio = radio.radios_menu("genre",genre)
				if id_radio == 0:
					print (radio.spaces)
					print (radio.start)
					print ("No radios availabre for this genre at the moment, please try another one")
					
				elif id_radio != "return_genre":
					ip = radio.radio_get_ip(id_radio)
					radio.play_radio(ip)
				else:
					id_radio = ""
					genre = ""
					print (radio.spaces)
					print (radio.start)
			else:
				genre = ""
				print (radio.spaces)
				print (radio.start)
		
		# SEARCH BY GENDER OR RADIO MENU
		elif user_input.startswith("search"):
			user_input = user_input.split()
			if len(user_input[2:]) == 0:
				print ("Please type something")
			else:
				if user_input[1] == "genre":
					keywords = radio.genres_menu(' '.join(user_input[2:]).title())
					if keywords == 0:
						print (radio.spaces)
						print (radio.start)
						print ("No genres with the keyword:", ' '.join(user_input[2:]).title(), "try something else")
					elif keywords != "home":
						id_radio = radio.radios_menu('genre',keywords)
						if id_radio == 0:
							print (radio.spaces)
							print (radio.start)
							print ("No radios available for this genre at the moment, please try another one")
						elif id_radio != "return_genre":
							ip = radio.radio_get_ip(id_radio)
							radio.play_radio(ip)
						else:
							id_radio = ""
							keywords = ""
							print (radio.spaces)
							print (radio.start)
					else:
						keywords = ""
						print (radio.spaces)
						print (radio.start)
					
				elif user_input[1] == "radio":
					id_radio = radio.radios_menu('keywords', ' '.join(user_input[2:]))
				
					if id_radio == 0:
						print (radio.spaces)
						print (radio.start)
						print ("No radios available for the keyword", ' '.join(user_input[2:]), "try something else")
					elif id_radio != "return_genre":
						ip = radio.radio_get_ip(id_radio)
						radio.play_radio(ip)
				
					else:
						id_radio = ""
						keywords = ""
						print (radio.spaces)
						print (radio.start)
				else:
					print ("unknow search inputs")
		
		elif user_input == radio.start_commands[5]:
			radio.options_menu()
			print (radio.spaces)
			print (radio.start)
	
		elif user_input == radio.start_commands[4]:
			print (radio.spaces)
			print ("see you around")
			radio.sys.exit(0)
		
		elif user_input == radio.start_commands[6]:
			option = radio.recent_radios()
			if option != 0:
				radio.play_radio(option)
			else:
				print (radio.spaces)
				print (radio.start)
		
		elif user_input == radio.start_commands[7]:
			if len(radio.previous_radio) != 0:
				ip = radio.radio_get_ip(radio.previous_radio[1])
				radio.play_radio(ip)
			else:
				print("No Previous Radio Found")
		
	else:
		print (radio.spaces)
		print (radio.start)
		print ("unknown Command")
		
