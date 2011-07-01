import Tkinter as tk
root = tk.Tk()

import bass.pybass as bass
import config

import pandora
from pandora.connection import AuthenticationError

import urllib2
import threading

class WorkerThread(threading.Thread):
	def __init__(self, app, pandora):
		threading.Thread.__init__(self)
		self.daemon = True
		self.app     = app
		self.pandora = pandora
		self.stop    = False
	
	def run(self):
		while not self.stop:
			# get next song
			try:
				song = self.pandora.getNextSong()
			except AuthenticationError:
				self.pandora.authenticate(username=config.PANDORA_USERNAME, password=config.PANDORA_PASSWORD)
				song = self.pandora.getNextSong()
			
			# play next song
			handle = bass.BASS_StreamCreateURL(song['audioURL'], 0, bass.BASS_STREAM_AUTOFREE, bass.DOWNLOADPROC(), 0)
			channel_length = bass.BASS_ChannelGetLength(handle, bass.BASS_POS_BYTE)
			channel_position = bass.BASS_ChannelGetPosition(handle, bass.BASS_POS_BYTE)
			bass.BASS_ChannelPlay(handle, False)
			while channel_position < channel_length:
				channel_position = bass.BASS_ChannelGetPosition(handle, bass.BASS_POS_BYTE)
				time.sleep(1)
			bass.BASS_StreamFree(handle)
	

class Application(tk.Frame):
	station = tk.StringVar()
	
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.createWidgets()
		self.initPandora()
	
	def createWidgets(self):
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
		top = self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(4, weight=1)
		self.master.title("Pandora")
		
		# main buttons + station list
		self.prevButton	= tk.Button(self, text='<<', command=self.prev)
		self.playButton	= tk.Button(self, text='>', command=self.playPause)
		self.stopButton	= tk.Button(self, text='[]', command=self.stop)
		self.nextButton	= tk.Button(self, text='>>', command=self.next)
		self.quitButton	= tk.Button(self, text='Quit', command=self.quit)
		self.stationLst = tk.OptionMenu(self, self.station, [])
		self.trackList	= tk.Listbox(self)
				
		# layout-ing
		self.prevButton.grid(row=0, column=0)
		self.playButton.grid(row=0, column=1)
		self.stopButton.grid(row=0, column=2)
		self.nextButton.grid(row=0, column=3)
		self.stationLst.grid(row=0, column=4, sticky=tk.N+tk.S+tk.E+tk.W)
		self.quitButton.grid(row=0, column=5)
		self.trackList.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=1, column=0, columnspan=6)
	
	def initPandora(self):
		# setup proxy
		if config.PANDORA_PROXY:
			proxy_support = urllib2.ProxyHandler({"http" : config.PANDORA_PROXY})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
		
		# setup pandora
		self.pandora = pandora.Pandora()
		if not self.pandora.authenticate(username=config.PANDORA_USERNAME, password=config.PANDORA_PASSWORD):
			raise ValueError("Wrong pandora credentials or proxy supplied")
		
		# get station list
		self.stationCache = self.pandora.getStationList()
		self.stationLst['menu'].delete(0, tk.END)
		for station in self.stationCache:
			self.stationLst['menu'].add_command(label=station['stationName'], command=lambda s=station: self.switchStation(s['stationName'], s['stationId']))
		
		# switch to first station
		self.switchStation(self.stationCache[0]['stationName'], self.stationCache[0]['stationId'])
	
	def prev(self):
		pass
		
	def next(self):
		pass
	
	def playPause(self):
		self.worker = WorkerThread(self, self.pandora)
		self.worker.start()
	
	def stop(self):
		self.worker.stop = True
		self.worker.join()
	
	def switchStation(self, stationName, stationId):
		print stationName
		
		# set value
		self.stationLst.setvar(self.stationLst.cget("textvariable"), value=stationName)
		
		# switch station online
		try:
			self.pandora.switchStation(stationId)
		except AuthenticationError:
			self.pandora.authenticate(username=config.PANDORA_USERNAME, password=config.PANDORA_PASSWORD)
			self.pandora.switchStation(stationId)

app = Application()
app.mainloop()