import tkinter as tk
from bs4 import BeautifulSoup
import translators as ts
import requests
import json
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
from youtube_search import YoutubeSearch
import webbrowser
import json


languages = {
	'af': 'Afrikaans',
	'sq': 'Albanian',
	'ar': 'Arabic',
	'hy': 'Armenian',
	'bn-BD': 'Bengali',
	'bs-Latn': 'Bosnian',
	'bg': 'Bulgarian',
	'ca': 'Catalan',
	'ny': 'Chichewa',
	'zh-Hans': 'Chinese (Simplified)',
	'zh-Hant': 'Chinese (Traditional)',
	'co': 'Corsican',
	'hr': 'Croatian',
	'cs': 'Czech',
	'da': 'Danish',
	'nl': 'Dutch',
	'en': 'English',
	'et': 'Estonian',
	'tl': 'Filipino',
	'fi': 'Finnish',
	'fr': 'French',
	'fy': 'Frisian',
	'gl': 'Falician',
	'ka': 'Georgian',
	'de': 'German',
	'el': 'Greek',
	'gu': 'Gujarati',
	'ht': 'Haitian Creole',
	'ha': 'Hausa',
	'haw': 'Hawaiian',
	'hi': 'Hindi',
	'hmn': 'Hmong',
	'hu': 'Hungarian',
	'is': 'Icelandic',
	'ig': 'Igbo',
	'id': 'Indonesian',
	'ga': 'Irish',
	'it': 'Italian',
	'ja': 'Japanese',
	'jw': 'Javanese',
	'kn': 'Kannada',
	'kk': 'Kazakh',
	'km': 'Khmer',
	'ko': 'Korean',
	'ku': 'Kurdish (Kurmanji)',
	'ky': 'Kyrgyz',
	'lo': 'Lao',
	'la': 'Latin',
	'lv': 'Latvian',
	'lt': 'Lithuanian',
	'lb': 'Luxembourgish',
	'mk': 'Macedonian',
	'mg': 'Malagasy',
	'ms': 'Malay',
	'ml': 'Malayalam',
	'mt': 'Maltese',
	'mi': 'Maori',
	'mr': 'Marathi',
	'my': 'Myanmar (Burmese)',
	'ne': 'Nepali',
	'no': 'Norwegian',
	'ps': 'Pashto',
	'fa': 'Persian',
	'pl': 'Polish',
	'pt': 'Portuguese',
	'pa': 'Punjabi',
	'ro': 'Romanian',
	'ru': 'Russian',
	'sm': 'Samoan',
	'gd': 'Scots Gaelic',
	'sr-Latn': 'Serbian',
	'st': 'Sesotho',
	'sn': 'Shona',
	'sd': 'Sindhi',
	'si': 'Sinhala',
	'sk': 'Slovak',
	'sl': 'Slovenian',
	'so': 'Somali',
	'es': 'Spanish',
	'su': 'Sundanese',
	'sw': 'Swahili',
	'sv': 'Swedish',
	'tg': 'Tajik',
	'ta': 'Tamil',
	'te': 'Telugu',
	'th': 'Thai',
	'tr': 'Turkish',
	'uk': 'Ukrainian',
	'ur': 'Urdu',
	'uz': 'Uzbek',
	'vi': 'Vietnamese',
	'cy': 'Welsh',
	'xh': 'Xhosa',
	'yi': 'Yiddish',
	'yo': 'Yoruba',
	'zu': 'Zulu',
	'fj': 'Fijian',
	'fil': 'Filipino',
	'he': 'Hebrew'
}



def listToString(s):  
	str1 = "" 
	return (str1.join(s)) 

def lyrics(artist, song):
	base = "https://www.azlyrics.com/"
	artistUse = artist.lower().replace(" ", "")
	songUse = song.lower().replace(" ", "")
	url = base+"lyrics/"+artistUse+"/"+songUse+".html"

	req = requests.get(url)
	soup = BeautifulSoup(req.content, "html.parser")
	lyrics = soup.find_all("div", attrs={"class": None, "id": None})
	newLyrics = [x.getText() for x in lyrics]
	return newLyrics

def get_key(val, dictName): 
	for key, value in dictName.items(): 
		if val == value: 
			return key 
	return "key doesn't exist2"

def is_value(k, dictName):
	for key, value in dictName.items(): 
		if k == key: 
			return True
	return False

def translateNow():
	global songT
	global artistT
	
	songT = str(songTitle.get())
	artistT= str(artistTitle.get())
	
	print(artistT)
	print(songT)
	gotLyrics = listToString(lyrics(artistT, songT))
	
	langKey=str(get_key(langOptMenu.get(), languages))
	

	if len(gotLyrics) == 0:
		messagebox.showerror(title="Song Not Found", message="Please enter another song, that song wasn't found")
		print("Hello")
	elif len(gotLyrics)>0:
		result = ts.bing(gotLyrics, from_language='auto', to_language=langKey)
		print("Hell1o")
		lyricsByLine = result.split('\n')
		print(lyricsByLine)
		longestLineLength = 0
		for i in lyricsByLine:
			if i != None and len(i) > longestLineLength:
				longestLineLength = len(i)
		longestLineLength = longestLineLength*6.2+10
		
		master2 = tk.Tk()
		styleMaster2 = ttk.Style(master2)
		styleMaster2.theme_use('default')
		styleMaster2.configure("2orange.TButton", background='#ff8f00',foreground="black", font=("System", 20))
		styleMaster2.configure("2orange.TLabel", foreground='#ff8f00',background="white", font=("System", 12),anchor='center', justify='center', align='center')
		styleMaster2.configure("2orangeTitle.TLabel", foreground='#ff8f00',background="white", font=("System", 20),anchor='center', justify='center', align='center')

		canvas = tk.Canvas(master2, height=800, width=longestLineLength)
		scroll_y = Scrollbar(master2, orient="vertical", command=canvas.yview)

		frame = tk.Frame(canvas)

		lyricsText = tk.StringVar(master2)
		lyricsText.set(result)
		
		titleText = tk.StringVar(master2)
		titleText.set(songT.title()+" — "+artistT.title())
		
		labelTitle = Label(frame, textvariable=titleText, style="2orangeTitle.TLabel")
		labelLyrics = Label(frame, textvariable=lyricsText, style="2orange.TLabel")
		Button(frame, text="Open Song in New Tab", command=open_Youtube_link, style="2orange.TButton").grid(column=0, row=2, columnspan=3, padx=10, pady=10)
		
		labelTitle.grid(column=0, row=0, columnspan=3, padx=10, pady=10, sticky="nsew")
		labelLyrics.grid(column=0, row=1, columnspan=3, padx=10, pady=10, sticky="nsew")
		canvas.create_window((0, 0), anchor='center', window=frame)
		canvas.update_idletasks()
		canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
		canvas.pack(fill='both', expand=True, side='left')
		scroll_y.pack(fill='y', side='right')
		canvas.yview_moveto('0.0')
		master2.mainloop()
		
def open_Youtube_link():
	youtubeSearchQuery = songT+' '+artistT+' '+'audio'
	results = YoutubeSearch(youtubeSearchQuery, max_results=1).to_dict()
	link = 'https://www.youtube.com'+results[0]['url_suffix']
	url = str(link)
	webbrowser.open(url)
		
def saveNativeLang():
	nativeLangFile = open("native_lang.txt", "w")
	print(get_key(langOptMenu2.get(), languages))
	nativeLangFile.write(get_key(langOptMenu2.get(), languages))
	nativeLangFile.close()
	master3.destroy()
	tkinter_run()

def reOpenSettings():
	nativeLangFile = open("native_lang.txt", "w")
	nativeLangFile.write('0')
	nativeLangFile.close()
	tkinter_run()
	

def getNativeLang():
	global langOptMenu2
	nativeLangFileRead = open("native_lang.txt", "r")
	nativeFileContent = nativeLangFileRead.read()
	print(str(nativeFileContent)+"yes")
	return str(nativeFileContent)

def tkinter_run():
	global langOptMenu2
	global songTitle
	global artistTitle
	global langOptMenu
	global master3
	global nativeLang
	
	print (is_value(getNativeLang(), languages))
		
	if is_value(getNativeLang(), languages):	
		
		print(getNativeLang())
		nativeLang = getNativeLang()
		print(nativeLang)

		master = tk.Tk()
		style2 = ttk.Style(master)
		style2.theme_use('default')

		style2.configure("2orange.horizontal.TEntry", foreground='#ff8f00', font=("System", 20))
		style2.configure("2orange.TButton", background='#ff8f00',foreground="black", font=("System", 20))
		style2.configure("2orange.TLabel", foreground='#ff8f00',background="white", font=("System", 20))
		style2.configure("2orange.TMenubutton", foreground='#ff8f00',background="white", width="5", font=("System", 20))
			
		langList=list(languages.values())
		
		langOptMenu = tk.StringVar(master)
		langOptMenu.set(langList[0])
		lang = ttk.OptionMenu(master, langOptMenu, *langList, style="2orange.TMenubutton")

		songLabelText = ts.bing("Enter the Song Title:", from_language='en', to_language=nativeLang)
		artistLabelText = ts.bing("Enter the Artist Title:", from_language='en', to_language=nativeLang)
		destinationLabelText = ts.bing("Enter the Destination Language:", from_language='en', to_language=nativeLang)
		translateButtonText = ts.bing("Translate", from_language='en', to_language=nativeLang)
		Label(master, text=songLabelText, style="2orange.TLabel").grid(row=0, column=0, pady='5px', padx='10px')
		Label(master, text=artistLabelText, style="2orange.TLabel").grid(row=1, column=0, pady='5px', padx='10px')
		Label(master, text=destinationLabelText, style="2orange.TLabel").grid(row=2, column=0, pady='5px', padx='10px')

		songTitle = Entry(master, width=15,style='2orange.horizontal.TEntry',font=("System", 20))
		artistTitle = Entry(master, width=15,style='2orange.horizontal.TEntry',font=("System", 20))

		Button(master, text=translateButtonText, command=translateNow, style='2orange.TButton').grid(row=3, column=0, columnspan=2, pady='10px', padx='10px')

		lang.config(width=15)
		songTitle.config(width=15)
		artistTitle.config(width=15)
		songTitle.grid(row=0, column=1, pady='5px', padx='10px')
		artistTitle.grid(row=1, column=1, pady='5px', padx='10px')
		lang.grid(row=2, column=1, pady='5px', padx='10px')


		master.mainloop()

	else:
		master3 = tk.Tk()
		style3 = ttk.Style(master3)
		style3.theme_use('default')

		style3.configure("3orange.TButton", background='#ff8f00',foreground="black", font=("System", 20))
		style3.configure("3orange.TLabel", foreground='#ff8f00',background="white", font=("System", 20), justify='CENTER')
		style3.configure("3orange.TMenubutton", foreground='#ff8f00',background="white", width="5", font=("System", 20))
			

		langList=list(languages.values())
		
				

		langOptMenu2 = tk.StringVar(master3)
		langOptMenu2.set(langList[0])
		nLangPicker = ttk.OptionMenu(master3, langOptMenu2, *langList, style="3orange.TMenubutton")

		Label(master3, text="Please pick your native language here:", style="3orange.TLabel").grid(row=0, column=0, columnspan=2, pady='5px', padx='10px')

		Button(master3, text="Enter", command=saveNativeLang, style='3orange.TButton').grid(row=3, column=0, columnspan=2, pady='10px', padx='10px')

		nLangPicker.config(width=15)
		nLangPicker.grid(row=2, column=0, columnspan=2, pady='5px', padx='10px')

		master3.mainloop()

		getNativeLang()


		
tkinter_run()