import Tkinter as tk
import tkMessageBox
root = tk.Tk()

import tkMessageBox

import ConfigParser
import string
import sys

import pandora_gui.bass.pybass as bass
from pandora_gui import worker

import pandora
from pandora.connection import AuthenticationError

import urllib2
import tkSimpleDialog

class Settings(tkSimpleDialog.Dialog):
	def body(self, master):
		tk.Label(master, text="Username:").grid(row=0)
		tk.Label(master, text="Password:").grid(row=1)
		tk.Label(master, text="Proxy:").grid(row=2)
		
		self.username = tk.Entry(master)
		self.username.grid(row=0, column=1)
		
		self.password = tk.Entry(master, show="*")
		self.password.grid(row=1, column=1)
		
		self.proxy = tk.Entry(master)
		self.proxy.grid(row=2, column=1)
		
		# load settings
		self.load()
		
		# initial focus
		return self.username
	
	def load(self):
		configParser = ConfigParser.SafeConfigParser()
		configParser.read('config.ini')
		self.username.insert(0, configParser.get('pandora', 'username'))
		self.password.insert(0, configParser.get('pandora', 'password'))
		self.proxy.insert(0, configParser.get('pandora', 'proxy'))
		

	def apply(self):
		# save settings to file
		configParser = ConfigParser.SafeConfigParser()
		configParser.add_section("pandora")
		configParser.set("pandora", "username", self.username.get())
		configParser.set("pandora", "password", self.password.get())
		configParser.set("pandora", "proxy", self.proxy.get())
		
		# actually write file
		with open('config.ini', 'w') as configfile:
			configParser.write(configfile)
		
		# save settings into app
		self.parent.config['PANDORA_USERNAME'] = self.username.get()
		self.parent.config['PANDORA_PASSWORD'] = self.password.get()
		self.parent.config['PANDORA_PROXY'] = self.proxy.get()
		
		# set return value
		self.result = True

class Application(tk.Frame):
	station = tk.StringVar()
	old_volume = 0.5
	
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		
		self.createWidgets()
		self.initSettings()
		self.initPandora()
		self.initBass()
	
	def createWidgets(self):
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
		top = self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(3, weight=1)
		self.master.title("Pandora")
		self.master.geometry("300x150")
		try:
			self.master.iconbitmap('pandora.ico')
		except:
			self.master.iconbitmap('@pandora.xbm')
		
		# main buttons + station list
		self.plStButton	= tk.Button(self, text='>', command=self.playStop)
		self.nextButton	= tk.Button(self, text='>>', command=self.next)
		self.quitButton	= tk.Button(self, text='Quit', command=self.quit)
		self.muteButton = tk.Button(self, text='@', command=self.mute)
		self.stationLst = tk.OptionMenu(self, self.station, [])
		self.trackList	= tk.Listbox(self)
				
		# layout-ing
		self.plStButton.grid(row=0, column=0)
		self.nextButton.grid(row=0, column=1)
		self.muteButton.grid(row=0, column=2)
		self.stationLst.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
		self.quitButton.grid(row=0, column=4)
		self.trackList.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=1, column=0, columnspan=5)
	
	def initSettings(self):
		# default settings
		self.config = {
			'PANDORA_PROXY': None,
			'PANDORA_USERNAME': None,
			'PANDORA_PASSWORD': None }
		
		# read settings from file
		configParser = ConfigParser.SafeConfigParser()
		configParser.read('config.ini')
		for section in configParser.sections():
			for option in configParser.options(section):
				name = string.upper("%s_%s" % (section, option))
				self.config[name] = configParser.get(section, option)
		
		# check settings
		if self.config['PANDORA_USERNAME'] == None or self.config['PANDORA_PASSWORD'] == None:
			if not self.showSettings():
				sys.exit()
	
	def initPandora(self):
		# setup proxy
		if self.config['PANDORA_PROXY']:
			proxy_support = urllib2.ProxyHandler({"http" : self.config['PANDORA_PROXY']})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
		
		# setup pandora
		self.pandora = pandora.Pandora()
		if not self.pandora.authenticate(username=self.config['PANDORA_USERNAME'], password=self.config['PANDORA_PASSWORD']):
			tkMessageBox.showerror("Pandora Player", "Wrong pandora credentials or proxy supplied")
			if self.showSettings():
				self.initPandora()
			else:
				sys.exit()
		
		# get station list
		self.stationCache = self.pandora.get_station_list()
		self.stationLst['menu'].delete(0, tk.END)
		for station in self.stationCache:
			self.stationLst['menu'].add_command(label=station['stationName'], command=lambda s=station: self.switchStation(s['stationName'], s['stationId']))
		
		# switch to first station
		self.switchStation(self.stationCache[0]['stationName'], self.stationCache[0]['stationId'])
	
	def initBass(self):
		bass.BASS_Init(-1, 44100, 0, 0, 0)
	
	def showSettings(self):
		settingsDialog = Settings(self, "Settings")
		return bool(settingsDialog.result)
	
	def next(self):
		self.worker.next = True
	
	def playStop(self):
		if self.plStButton['text'] == '>':
			# play
			self.worker = worker.WorkerThread(self, self.pandora)
			self.worker.start()
			self.plStButton['text'] = "[]"
		else:
			#stop
			self.worker.stop = True
			self.worker.join()
			self.plStButton['text'] = ">"
		
	def switchStation(self, stationName, stationId):
		# set value
		self.stationLst.setvar(self.stationLst.cget("textvariable"), value=stationName)
		
		# switch station online
		try:
			self.pandora.switch_station(stationId)
		except AuthenticationError:
			self.pandora.authenticate(username=config.PANDORA_USERNAME, password=config.PANDORA_PASSWORD)
			self.pandora.switch_station(stationId)
		except Exception as e:
			print e
			tkMessageBox.showerror("Pandora", "An error occured: %s" % e.message)
	
	def mute(self):
		if bass.BASS_GetVolume() == 0.0:
			bass.BASS_SetVolume(self.old_volume)
		else:
			self.old_volume = bass.BASS_GetVolume()
			bass.BASS_SetVolume(0.0)
	
	def newSong(self, song):
		self.trackList.insert(0, "%s (%s on %s)" % (song['songName'], song['artistName'], song['albumName']))

app = Application()
app.mainloop()

# free bass
bass.BASS_Free()
