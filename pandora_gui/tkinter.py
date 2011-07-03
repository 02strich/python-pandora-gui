import Tkinter as tk
root = tk.Tk()

import bass.pybass as bass
import config

import pandora
from pandora.connection import AuthenticationError

import urllib2
import threading
import time

class WorkerThread(threading.Thread):
	def __init__(self, app, pandora):
		threading.Thread.__init__(self)
		self.daemon  = True
		self.app     = app
		self.pandora = pandora
		
		self.stop    = False
		self.next	 = False
	
	def run(self):
		while not self.stop:
			# get next song
			try:
				song = self.pandora.getNextSong()
			except AuthenticationError:
				self.pandora.authenticate(username=config.PANDORA_USERNAME, password=config.PANDORA_PASSWORD)
				song = self.pandora.getNextSong()
			
			# call app
			app.newSong(song)
			
			# create stream
			handle = bass.BASS_StreamCreateURL(song['audioURL'], 0, bass.BASS_STREAM_AUTOFREE, bass.DOWNLOADPROC(), 0)
			if handle == 0:
				print bass.get_error_description(bass.BASS_ErrorGetCode())
			
			# play it
			channel_length = bass.BASS_ChannelGetLength(handle, bass.BASS_POS_BYTE)
			channel_position = bass.BASS_ChannelGetPosition(handle, bass.BASS_POS_BYTE)
			if not bass.BASS_ChannelPlay(handle, False):
				print bass.get_error_description(bass.BASS_ErrorGetCode())
			
			# wait for it to end
			while channel_position < channel_length:
				# check whether we should continue
				if self.stop or self.next:
					bass.BASS_ChannelStop(handle)
					self.next = False
					break
				
				channel_position = bass.BASS_ChannelGetPosition(handle, bass.BASS_POS_BYTE)
				time.sleep(1)
			bass.BASS_StreamFree(handle)
	

class Application(tk.Frame):
	station = tk.StringVar()
	old_volume = 0.5
	
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.createWidgets()
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
	
	def initBass(self):
		bass.BASS_Init(-1, 44100, 0, 0, 0)
	
	def next(self):
		self.worker.next = True
	
	def playStop(self):
		if self.plStButton['text'] == '>':
			# play
			self.worker = WorkerThread(self, self.pandora)
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
			self.pandora.switchStation(stationId)
		except AuthenticationError:
			self.pandora.authenticate(username=config.PANDORA_USERNAME, password=config.PANDORA_PASSWORD)
			self.pandora.switchStation(stationId)
	
	def mute(self):
		if bass.BASS_GetVolume() == 0.0:
			bass.BASS_SetVolume(self.old_volume)
		else:
			self.old_volume = bass.BASS_GetVolume()
			bass.BASS_SetVolume(0.0)
	
	def newSong(self, song):
		self.trackList.insert(tk.END, "%s (%s on %s)" % (song['songTitle'], song['artistSummary'], song['albumTitle']))

app = Application()
app.mainloop()

# free bass
bass.BASS_Free()