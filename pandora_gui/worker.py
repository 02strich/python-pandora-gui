import pandora_gui.bass.pybass as bass

from pandora.connection import AuthenticationError

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
				song = self.pandora.get_next_song()
			except AuthenticationError:
				self.pandora.authenticate(username=app.config['PANDORA_USERNAME'], password=app.config['PANDORA_PASSWORD'])
				song = self.pandora.get_next_song()
			
			# call app
			self.app.newSong(song)
			
			# create stream
			handle = bass.BASS_StreamCreateURL(song['additionalAudioUrl'], 0, bass.BASS_STREAM_AUTOFREE, bass.DOWNLOADPROC(), 0)
			if handle == 0:
				print bass.get_error_description(bass.BASS_ErrorGetCode())
			
			# play it
			channel_length = bass.BASS_ChannelGetLength(handle, bass.BASS_POS_BYTE)
			channel_position = bass.BASS_ChannelGetPosition(handle, bass.BASS_POS_BYTE)
			if not bass.BASS_ChannelPlay(handle, False):
				print bass.get_error_description(bass.BASS_ErrorGetCode())
			
			# wait for it to end
			while (channel_position != -1) and (channel_position < channel_length):
				# check whether we should continue
				if self.stop or self.next:
					bass.BASS_ChannelStop(handle)
					self.next = False
					break
				
				channel_position = bass.BASS_ChannelGetPosition(handle, bass.BASS_POS_BYTE)
				time.sleep(1)
			bass.BASS_StreamFree(handle)