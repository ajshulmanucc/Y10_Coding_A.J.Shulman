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
import tkinter.filedialog as tkFileDialog
languages = {'af': 'Afrikaans', 'ar': 'Arabic', 'bn-BD': 'Bengali', 'bs-Latn': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan', 'zh-Hans': 'Chinese (Simplified)', 'zh-Hant': 'Chinese (Traditional)', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 'et': 'Estonian', 'fj': 'Fijian', 'fil': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'ht': 'Haitian Creole', 'he': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong Daw', 'hu': 'Hungarian', 'is': 'Icelandic', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)', 'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'no': 'Norwegian', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'sr-Latn': 'Serbian', 'sk': 'Slovak', 'sl': 'Slovenian', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'cy': 'Welsh'}

def saveas(lyrics, title, fileName):
	savelocation=tkFileDialog.asksaveasfilename(defaultextension=".txt", initialfile=fileName)
	file1=open(savelocation, "w")
	file1.write(title + "\n" + lyrics) 
	file1.close()

def longestLine(list1):
	lyricsByLine = list1.split('\n')
	longestLineLength = 0
	for i in lyricsByLine:
		if i != None and len(i) > longestLineLength:
			longestLineLength = len(i)
	longestLineLength = longestLineLength*6.2+10
	return longestLineLength

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

	gotLyrics = listToString(lyrics(artistT, songT))
	
	langKey=str(get_key(langOptMenu.get(), languages))

	if len(gotLyrics) == 0:
		messagebox.showerror(title=ts.bing("Song Not Found", from_language='auto', to_language=getNativeLang()).title(), message=ts.bing("Please enter another song, that song wasn't found.", from_language='auto', to_language=getNativeLang()))
	elif len(gotLyrics)>0:
		result = ts.bing(gotLyrics, from_language='auto', to_language=langKey)
		newOriginalLyrics = gotLyrics.replace('\r','')
		newOriginalLyrics = '\n'.join(newOriginalLyrics.split('\n')[1:])
		longestLineTotal = longestLine(result)+longestLine(newOriginalLyrics)+20

		saveTitle = songT.title()+"_"+artistT.title()+"_"+ts.bing(langOptMenu.get().title(), from_language='auto', to_language=getNativeLang())
		saveTitle = saveTitle.replace(" ","_")
		
		master2 = tk.Tk()
		master2.bind_all("<Command-q>", master2.quit)
		
		master2.title(ts.bing("Translated Lyrics for ", from_language='auto', to_language=getNativeLang()).title()+songT.title()+ts.bing(" by ", from_language='auto', to_language=getNativeLang()).title()+artistT.title())
		styleMaster2 = ttk.Style(master2)
		styleMaster2.theme_use('default')
		styleMaster2.configure("2orange.TButton", background='#ff8f00',foreground="black", font=("System", 20))
		styleMaster2.configure("2orange.TLabel", foreground='#ff8f00',background="white", font=("System", 12),anchor='center', justify='center', align='center')
		styleMaster2.configure("2orangeTitle.TLabel", foreground='#ff8f00',background="white", font=("System", 20),anchor='center', justify='center', align='center')

		canvas = tk.Canvas(master2, height=800, width=longestLineTotal)
		scroll_y = Scrollbar(master2, orient="vertical", command=canvas.yview)

		frame = tk.Frame(canvas)
		
		titleOriginal = ts.bing("Original Lyrics", from_language='auto', to_language=getNativeLang()).title()
		titleOriginalText = tk.StringVar(master2)
		titleOriginalText.set(titleOriginal)
		
		lyricsOriginalText = tk.StringVar(master2)
		lyricsOriginalText.set(newOriginalLyrics)

		lyricsTransText = tk.StringVar(master2)
		lyricsTransText.set(result)
		
		titleTrans = ts.bing("Lyrics in "+langOptMenu.get(), from_language='auto', to_language=getNativeLang()).title()
		titleTransText = tk.StringVar(master2)
		titleTransText.set(titleTrans)
		
		labelOriginalTitle = Label(frame, textvariable=titleOriginalText, style="2orangeTitle.TLabel")
		labelOriginalLyrics = Label(frame, textvariable=lyricsOriginalText, style="2orange.TLabel", borderwidth = 3,
			relief="ridge")
		
		labelTransTitle = Label(frame, textvariable=titleTransText, style="2orangeTitle.TLabel")
		labelTransLyrics = Label(frame, textvariable=lyricsTransText, style="2orange.TLabel", borderwidth = 3,
			relief="ridge")
		
		youtubeText = ts.bing("Open Song in New Tab", from_language='auto', to_language=getNativeLang()).title()
		
		downloadText = ts.bing("Download Translated Lyrics", from_language='auto', to_language=getNativeLang()).title()
		
		Button(frame, text=youtubeText, command=open_Youtube_link, style="2orange.TButton").grid(column=0, row=3, columnspan=2, padx=10, pady=10)
		Button(frame, text=downloadText, command=lambda: saveas(result, songT+" - "+artistT, saveTitle), style="2orange.TButton").grid(column=0, row=2, columnspan=2, padx=10, pady=10)
		
		labelOriginalTitle.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")
		labelOriginalLyrics.grid(column=0, row=1, padx=10, pady=10, sticky="nsew", ipadx=10)
		labelTransTitle.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")
		labelTransLyrics.grid(column=1, row=1, padx=10, pady=10, sticky="nsew", ipadx=10)
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
	nativeLangFile.write(get_key(langOptMenu2.get(), languages))
	nativeLangFile.close()
	master3.destroy()
	tkinter_run()

def reOpenSettings():
	master.destroy()
	nativeLangFileSettings = open("native_lang_settings.txt", "w")
	nativeLangFileSettings.write(getNativeLang())
	nativeLangFileSettings.close()
	nativeLangFile = open("native_lang.txt", "w")
	nativeLangFile.write('0')
	nativeLangFile.close()
	tkinter_run()
	

def getNativeLang():
	nativeLangFileRead = open("native_lang.txt", "r")
	nativeFileContent = nativeLangFileRead.read()
	return str(nativeFileContent)

def getSettingsLang():
	nativeLangSettingsFileRead = open("native_lang_settings.txt", "r")
	nativeSettingsFileContent = nativeLangSettingsFileRead.read()
	return str(nativeSettingsFileContent)

def tkinter_run():
	global langOptMenu2
	global songTitle
	global artistTitle
	global langOptMenu
	global master3
	global nativeLang
	global master
			
	if is_value(getNativeLang(), languages):
		
		nativeLang = getNativeLang()

		master = tk.Tk()
		master.bind_all("<Command-q>", master.quit)
		master.title(ts.bing("Song Search", from_language='en', to_language=nativeLang).title())
		style2 = ttk.Style(master)
		style2.theme_use('default')

		style2.configure("2orange.horizontal.TEntry", foreground='#ff8f00', font=("System", 20))
		style2.configure("2orange.TButton", background='#ff8f00',foreground="black", font=("System", 20))
		style2.configure("2orangeSettings.TButton", background='#ff8f00',foreground="black", font=("System", 10))
		style2.configure("2orange.TLabel", foreground='#ff8f00',background="white", font=("System", 20))
		style2.configure("2orange.TMenubutton", foreground='#ff8f00',background="white", width="5", font=("System", 20))
			
		langList=list(languages.values())
		
		langOptMenu = tk.StringVar(master)
		langOptMenu.set(langList[0])
		lang = ttk.OptionMenu(master, langOptMenu, langList[0], *langList, style="2orange.TMenubutton")

		songLabelText = ts.bing("Enter the Song Title:", from_language='en', to_language=nativeLang)
		artistLabelText = ts.bing("Enter the Artist Title:", from_language='en', to_language=nativeLang)
		destinationLabelText = ts.bing("Enter the Destination Language:", from_language='en', to_language=nativeLang)
		translateButtonText = ts.bing("Translate", from_language='en', to_language=nativeLang)
		Label(master, text=songLabelText, style="2orange.TLabel").grid(row=0, column=0, columnspan=2, pady='5px', padx='10px')
		Label(master, text=artistLabelText, style="2orange.TLabel").grid(row=1, column=0, columnspan=2, pady='5px', padx='10px')
		Label(master, text=destinationLabelText, style="2orange.TLabel").grid(row=2, column=0,columnspan=2, pady='5px', padx='10px')

		songTitle = Entry(master, width=15,style='2orange.horizontal.TEntry',font=("System", 20))
		artistTitle = Entry(master, width=15,style='2orange.horizontal.TEntry',font=("System", 20))

		Button(master, text=translateButtonText, command=translateNow, style='2orange.TButton').grid(row=3, column=0, columnspan=4, pady='10px', padx='10px')
		
		settingsButtonText = ts.bing("Settings", from_language='en', to_language=nativeLang)
		photo = tk.PhotoImage(file = r"settings.png")
		Button(master, text = settingsButtonText+" ", image = photo, command=reOpenSettings, compound='right', style='2orangeSettings.TButton').grid(row=3, column=3, pady='10px')
		

		lang.config(width=15)
		songTitle.config(width=15)
		artistTitle.config(width=15)
		songTitle.grid(row=0, column=2,columnspan=2, pady='5px', padx='10px')
		artistTitle.grid(row=1, column=2,columnspan=2, pady='5px', padx='10px')
		lang.grid(row=2, column=2,columnspan=2, pady='5px', padx='10px')


		master.mainloop()

	else:
		master3 = tk.Tk()
		master3.bind_all("<Command-q>", master3.quit)
		master3.title(ts.bing("Settings", from_language='auto', to_language=getSettingsLang()))
		style3 = ttk.Style(master3)
		style3.theme_use('default')

		style3.configure("3orange.TButton", background='#ff8f00',foreground="black", font=("System", 20))
		style3.configure("3orange.TLabel", foreground='#ff8f00',background="white", font=("System", 20), justify='CENTER')
		style3.configure("3orange.TMenubutton", foreground='#ff8f00',background="white", width="5", font=("System", 20))
			

		langList=list(languages.values())
		
				

		langOptMenu2 = tk.StringVar(master3)
		langOptMenu2.set(langList[0])
		nLangPicker = ttk.OptionMenu(master3, langOptMenu2, langList[0], *langList, style="3orange.TMenubutton")

		Label(master3, text=ts.bing("Please pick your native language here:", from_language='auto', to_language=getSettingsLang()), style="3orange.TLabel").grid(row=0, column=0, columnspan=2, pady='5px', padx='10px')

		Button(master3, text=ts.bing("Enter", from_language='auto', to_language=getSettingsLang()), command=saveNativeLang, style='3orange.TButton').grid(row=3, column=0, columnspan=2, pady='10px', padx='10px')

		nLangPicker.config(width=15)
		nLangPicker.grid(row=2, column=0, columnspan=2, pady='5px', padx='10px')

		master3.mainloop()

		getNativeLang()

tkinter_run()