#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, subprocess, platform, importlib #importlib is needed in py3
importlib.reload(sys)
#sys.setdefaultencoding('utf8') #standard default in py3...useless command

start_commands = ["genres", "search genre", "search radio" , "help", "exit", "options"] # list of possible commands the user can use

genre_list = [] # global list that will store the genres

search_type = "" # for searching type process

id_rad = 0 #id of the radio, used to get the http link for the mplayer

user_input_prompt = "> " # text to promp what the user will write

spaces = "\n" * 100 # use it to give space between options

exit_program = 0 # signal to quit program

attempt = 3 # for exceptions errors

#OPTIONS MENU VARS

options = {'Number of Items Per Page' : 16} #A dict that contains all the options and his values

#Number of Items Per Page that will be display, the user can change this value freely, by default this value is 16



start = '''		

__        _______ _     ____ ___  __  __ _____   _____ ___  
\ \      / / ____| |   / ___/ _ \|  \/  | ____| |_   _/ _ \ 
 \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|     | || | | |
  \ V  V / | |___| |__| |__| |_| | |  | | |___    | || |_| |
   \_/\_/  |_____|_____\____\___/|_|  |_|_____|   |_| \___/ 
                                                            
 _____ _   _ _____   ____      _    ____ ___ ___  
|_   _| | | | ____| |  _ \    / \  |  _ \_ _/ _ \ 
  | | | |_| |  _|   | |_) |  / _ \ | | | | | | | |
  | | |  _  | |___  |  _ <  / ___ \| |_| | | |_| |
  |_| |_| |_|_____| |_| \_\/_/   \_\____/___\___/ 
                                                       
Type search genre *genre here* for genre search
Type search radio *name here* for a radio search
Type genres to see all possible genres
Type options for options menu
Type help for help documentation
Type exit to quit application
'''

help_manual = '''
This radio connects to the website https://www.xatworld.com/radio-search/
were it gets all the available genres of that website and radios os that genre

It's Simple To use This Radio By Terminal, All you have to do is
search for a genre you'd like to hear and then select
a radio by index.

To See all Genres Available, 
Type *genres* and it'll show you all genres available
To Search a radio by his genre, type *seach genre 'name of the genre'*
and this show you all radios of that genre

then select a radio by typing the radio's index

To navigate to Next page, type n
To navigate to previous page, type p
To return to the main page, type b
to exit a radio and return to the main page, do Ctrl + c
Type exit to leave aplication

inside the player, mplayer in this case you can:
9 to lower your volume
0 to raise your volume
q to quit

Type options to go to the options menu where at the moment there is only
the option number of items
more to come in the future

to change a value of some option just type the id of that option and then the new value
i.e: 1 25 


press q to return'''

def installModulesIfNotFound():
	try:
		import requests, lxml.html, json, os, time
		from tabulate import tabulate
	except ImportError:
		list_modules = ['requests','lxml','tabulate']
		print ("To use this radio application you need to install the following modules:")
		print ("requests, lxml and tabulate")
		print ("will you install them??")
		answer = input("type yes|no -> ")
		if answer == "yes":
			for i in list_modules:
				p = subprocess.Popen(['pip3', 'install', i])
				p.wait()
			print ("Sucess installing all required modules!")
			time.sleep(2)
		elif answer == "no":
			print ("To use this program you'll need to install tabulate")
			exit()
		else:
			print ("unknown keyword")
			exit()

installModulesIfNotFound()

import requests, lxml.html, json, time, os
from tabulate import tabulate

def getHelp():
	quit_key = ""
	print (spaces)
	print (help_manual)
	while quit_key != "q":
		quit_key = input(user_input_prompt)
	print (spaces)
	print (start)

def options_menu():
	global options
	command = ""
	msg = ""
	while command != "b":
		items = []
		i = 1

		print (spaces)
		for key, values in options.items():
			items.append([i,key,values])
			i += 1
		print (tabulate(items, headers = ["ID", "NAME OF OPTION", "VALUES"], tablefmt="simple"))
		print ("\n")
		print (msg)
		print ("Type the id and the new value to update it, b to return home")
		command = input(user_input_prompt)
		if command == "":
			msg = "you need to type something"
		else:
			command = command.split()
			if command[0].isdigit() and int(command[0]) in range(0, len(items) + 1) and len(command) == 2:
				options[items[int(command[0])- 1][1]] = int(command[1])
				msg = "Update sucessfull"
		
		
			elif command[0] == "b":
				break
			else:
				msg = "unknown command"


def selector_menu(list_with_options, select_type, user_content=""):

	number_options_pages = int(len(list_with_options) / options['Number of Items Per Page'])
	header = []
	previous_page = 0
	next_page = 1
	option = ""
	command = ""
	genre = ""
	
	
	while option == "":
		print (spaces)
		table = []
		i = 1
		
		if select_type == "genre":
			header = ["ID", "GENRE NAME"]
			genre = "Please Select a genre"
			for opt in list_with_options[(previous_page*options['Number of Items Per Page']):(options['Number of Items Per Page']*next_page)]:
				table.append([i,opt])
				i = i + 1
		
		elif select_type == "radio":
			header = ["ID","NAME", "NOW PLAYING","LISTENERES", "BITRATE"]
			genre = "Please Select a Radio."
			for opt in list_with_options[(previous_page*options['Number of Items Per Page']):(options['Number of Items Per Page']*next_page)]:
				table.append([i, opt[0], opt[1], opt[4], opt[3]])
				i = i + 1
			
		print (tabulate(table, headers = header, tablefmt="simple"))
		print ("\n" + genre)
		print ("n for next page, p for previous page, b to return to the start menu")
		print ("PAGE NUMBER:", next_page, "OF", number_options_pages + 1,"PAGES")
		command = input(user_input_prompt)
		if command.isdigit() and int(command) in range(0, options['Number of Items Per Page']+1):
			option = (options['Number of Items Per Page']*previous_page) + int(command)
		elif command == "n":
			if next_page <= number_options_pages:
				next_page = next_page + 1						
				previous_page = previous_page + 1
		elif command == "p":
			if previous_page != 0:
				next_page = next_page - 1
				previous_page = previous_page - 1
		elif command == "b":
			if select_type == "genre":
				return "home"
			else:
				return "return_genre"
		else:
			print ("unknown command")
	if(select_type == "genre"):
		return list_with_options[option - 1]
	elif(select_type == "radio"):
		return list_with_options[option -1][5]
		


def genres_menu(client_keywords = ""):
	'''
	Creates a list with all genres, with that we can check each genre and see each station
	Requires: nothing, just call the function and it will return you the genre you've chosen 
	Ensures: a music genre
	
	'''
	client_keys = client_keywords
	print (spaces)
	print ("connecting, please standy.....")
	

	try:
		global attempt
		if len(genre_list) == 0:
			i = 0
			classes = lxml.html.fromstring(requests.post('https://www.xatworld.com/radio-search/', data={'search' : 'simple' , 'genre' : ''}).text)
			print ("connected, getting genres list...")
			for form in classes.xpath('//td[@class="centerTxt"]'):
				i = i + 1
				if i == 3:
					text = [line for line in form.text_content().split('\n') if line.strip() != '']
					for g_html in text[1::]:
						genre_list.append(g_html.lstrip())	

		if client_keywords != "":
			search_list = []
			for search_genre in genre_list:
				if search_genre.startswith(client_keywords) or client_keywords in search_genre:
					search_list.append(search_genre)
			if len(search_list) == 0:
				return 0
				
			option = selector_menu(search_list, "genre")
		
		else:
			option = selector_menu(genre_list, "genre")
		
		attempt = 3
		return option
		
	except requests.exceptions.RequestException:
		if attempt != 0:
			attempt -=1
			print ("Connection Time out, retrying in 5 seconds...")
			for i in range(5,0,-1):
				print ("retrying in",i)
				time.sleep(1)
			genres_menu(client_keys)
		else:
			print ("Connection time out, please try again later")
			sys.exit(1)
	

def radios_menu(type_radio, content_radio):
	'''
	creates a list of lists with all the radios of a certanint genre
	Requires: a string with the genre name
	Ensures: All possible radios of that genre
	'''
	
	type_recovery = type_radio
	content_recovery = content_radio
	print (spaces)
	print ("please standy...")
	try:
		table_radios = []
		classes = lxml.html.fromstring(requests.post('https://www.xatworld.com/radio-search/', data={'search' : 'simple' , type_radio : content_radio}).text)
		for form in classes.xpath('//td[@class="centerTxt"]'):
			if len(form) == 16 or len(form) == 15:
				r_genre = []
				text = [line for line in form.text_content().split('\n') if line.strip() != '']
				r_genre.append(text[0].lstrip()[9:35])
				r_genre.append(text[1].lstrip()[13:33])
				r_genre.append(text[3].lstrip()[7:])
				r_genre.append(text[4].lstrip()[9:])
				r_genre.append(text[5].lstrip()[12:])
			
				for field in form.getchildren():
					if 'value' in field.keys() and field.get('value') == 'Get IP':
						r_genre.append(field.get('onclick').split(", ")[1].replace(')', ''))
				table_radios.append(r_genre)
	
		if len(table_radios) == 0:
			return 0
		option = selector_menu(table_radios, "radio", content_radio)
	
		return option
	
	except requests.exceptions.RequestException:
		if attempt != 0:
			attempt -=1
			print ("Connection Time out, retrying in 5 seconds...")
			for i in range(5,0,-1):
				print ("retrying in",i)
				time.sleep(1)
			radios_menu(name_genre,is_ser)
		else:
			print ("Connection time out, please try again later")
			sys.exit(1)
	


def radio_get_ip(id_radio):
	'''
	get ip from radio station by id number
	Requires: int that is the radio's id
	Ensure: the http link of that radio id
	'''
	id_rad = id_radio
	print (spaces)
	print ("Connecting to radio, please standy...")
	try:
		ips = []
		for ip in json.loads(requests.post('https://www.xatworld.com/plugins/radio-search/getip.php?JsHttpRequest=0-xml', data={'id' : str(id_radio)}).text)['js']['ip'].split():
			ips.append(ip)
		return ips[0]
	
	except requests.exceptions.RequestException:
		if attempt != 0:
			attempt -=1
			print ("Connection Time out, retrying in 5 seconds...")
			for i in range(5,0,-1):
				print ("retrying in",i)
				time.sleep(1)
			radio_get_ip(id_rad)
		else:
			print ("Connection time out, please try again later")
			sys.exit(1)
	
def play_radio(radio_ip):
	#see what os does the user have
	osType = platform.system()
	p = ""
	player = ""
	if osType == 'Linux' or osType == "Ios":
		p = subprocess.Popen(['mplayer', radio_ip, '-vo', 'null', '-ao', 'alsa','-quiet'])
		player = "mplayer"
	elif osType == 'Windows':
		p = subprocess.Popen('C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe /play /close "' + radio_ip +'"')
		player = "Windows Music Player"
		
	
	print ("Connected, opening", player)
	
	p.wait()
	print (spaces)
	print (start)

def signal_handler(signal, frame):
	global exit_program
	if exit_program == 0:
		print ("press ctrl + c again to exit")
		exit_program = exit_program + 1
	else:
		print (spaces)
		print ("BYE :) see you around!")
		sys.exit(0)
