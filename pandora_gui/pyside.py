# -*- coding: utf-8 -*-
import sys
from PySide.QtCore import *
from PySide.QtGui import *
import pyside_main, pyside_settings

import pandora_gui.bass.pybass as bass
from pandora_gui import worker

import pandora
from pandora.connection import AuthenticationError

import urllib2

class TableModel(QAbstractTableModel):
	def __init__(self, songs=[], parent=None):
		super(TableModel, self).__init__(parent)
		self.songs = songs
	
	def addSong(self, song):
		self.beginInsertRows(QModelIndex(), 0, 0)
		self.songs = [song] + self.songs
		self.endInsertRows()
		
		return 0
	
	def rowCount(self, index=QModelIndex()):
		""" Returns the number of rows the model holds. """
		return len(self.songs)
	
	def columnCount(self, index=QModelIndex()):
		""" Returns the number of columns the model holds. """
		return 2
	
	def data(self, index, role=Qt.DisplayRole):
		""" Depending on the index and role given, return data. If not 
			returning data, return None (PySide equivalent of QT's 
			"invalid QVariant").
		"""
		if not index.isValid():
			return None
		
		if not 0 <= index.row() < self.rowCount():
			return None
		
		song = self.songs[index.row()]
		
		if role == Qt.DisplayRole:
			if index.column() == 1:
				result = "<b>%s</b><br/>by <b>%s</b> on <b>%s</b>" % (song['songTitle'], song['artistSummary'], song['albumTitle'])
				return result
		elif role == Qt.DecorationRole:
			if index.column() == 0:
				if not 'albumImage' in song:
					# get data
					u = urllib2.urlopen(song['artRadio'])
					imageData = u.read()
					u.close()
					
					# get it into qt
					bytearr = QByteArray(imageData)
					imagen = QImage()
					imagen.loadFromData(bytearr)
					imagen = imagen.scaledToWidth(75)
					song['albumImage'] = imagen
				return song['albumImage']
		return None
		
	

class FormattedTextDelegate(QStyledItemDelegate):
	def paint(self, painter, option, index):
		value = index.data(Qt.DisplayRole)
		if not value:
			return
		
		document = QTextDocument()
		document.setHtml(value)
		
		textHeight = document.size().height()
		translation = QPointF(option.rect.left(), option.rect.top() + (option.rect.height() - textHeight)/2.0)
		
		painter.translate(translation)
		document.drawContents(painter)
		painter.translate(-translation)
	

class SettingsForm(QDialog):
	settings = {}
	
	def __init__(self, parent=None):
		super(SettingsForm, self).__init__(parent)
		
		# call designer code
		self.ui = pyside_settings.Ui_Dialog()
		self.ui.setupUi(self)
		self.accepted.connect(self.saveSettings)
		
		# load settings
		self.qsettings = QSettings("02strich", "python-pandora")
		self.settings['PANDORA_USERNAME'] = self.qsettings.value("pandora/username", "")
		self.settings['PANDORA_PASSWORD'] = self.qsettings.value("pandora/password", "")
		self.settings['PANDORA_PROXY']    = self.qsettings.value("network/proxy", "")
		
		# display them
		self.ui.txtUsername.setText(self.settings['PANDORA_USERNAME'])
		self.ui.txtPassword.setText(self.settings['PANDORA_PASSWORD'])
		self.ui.txtProxy.setText(self.settings['PANDORA_PROXY'])
	
	def saveSettings(self):
		# load into settings
		self.settings['PANDORA_USERNAME'] = self.ui.txtUsername.text()
		self.settings['PANDORA_PASSWORD'] = self.ui.txtPassword.text()
		self.settings['PANDORA_PROXY'] = self.ui.txtProxy.text()
		
		# store them
		self.qsettings.setValue('pandora/username', self.settings['PANDORA_USERNAME'])
		self.qsettings.setValue('pandora/password', self.settings['PANDORA_PASSWORD'])
		self.qsettings.setValue('network/proxy', self.settings['PANDORA_PROXY'])
	
	def isUsernameAndPasswordSet(self):
		if not ('PANDORA_USERNAME' in self.settings) and ('PANDORA_PASSWORD' in self.settings): return False
		if not self.settings['PANDORA_USERNAME']: return False
		if not self.settings['PANDORA_PASSWORD']: return False
		return True
	


class MainForm(QDialog):
	old_volume = 0.5
	newSongBegan = Signal(dict)
	
	def __init__(self, parent=None):
		super(MainForm, self).__init__(parent)
		
		# call designer code
		self.ui = pyside_main.Ui_Dialog()
		self.ui.setupUi(self)
		
		# create model
		self.trackModel = TableModel(parent=self)
		self.ui.lstSongs.setModel(self.trackModel)
		
		# configure more
		self.ui.lstSongs.setItemDelegateForColumn(1, FormattedTextDelegate(self))
		
		# connect events
		self.ui.btnPlay.clicked.connect(self.playStop)
		self.ui.btnNext.clicked.connect(self.next)
		self.ui.btnMute.clicked.connect(self.mute)
		self.ui.btnSettings.clicked.connect(self.settings)
		self.ui.btnQuit.clicked.connect(self.quit)
		self.ui.cbStations.currentIndexChanged[int].connect(self.switchStation)
		self.newSongBegan.connect(self.newSongInternal)
		
		# other inits
		self.cf = SettingsForm(self)
		self.initPandora()
		self.initBass()
	
	def initPandora(self):
		# check settings
		while not self.cf.isUsernameAndPasswordSet():
			if self.cf.exec_() == 0:
				sys.exit()
		
		# setup proxy
		if self.cf.settings['PANDORA_PROXY']:
			proxy_support = urllib2.ProxyHandler({"http" : self.cf.settings['PANDORA_PROXY']})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
		
		# setup pandora
		self.pandora = pandora.Pandora()
		while not self.pandora.authenticate(username=self.cf.settings['PANDORA_USERNAME'], password=self.cf.settings['PANDORA_PASSWORD']):
			QMessageBox.critical(self, "Python Pandora", "Wrong pandora credentials or proxy supplied")
			if self.cf.exec_() == 0:
				sys.exit()
		
		# get station list
		self.stationCache = self.pandora.getStationList()
		for station in self.stationCache:
			self.ui.cbStations.addItem(station['stationName'])
	
	def initBass(self):
		bass.BASS_Init(-1, 44100, 0, 0, 0)
	
	def next(self):
		if self.worker:
			self.worker.next = True
	
	def playStop(self):
		if self.ui.btnPlay.text() == '>':
			# play
			self.worker = worker.WorkerThread(self, self.pandora)
			self.worker.start()
			self.ui.btnPlay.setText("[]")
		else:
			#stop
			self.worker.stop = True
			self.worker.join()
			self.ui.btnPlay.setText(">")
	
	def switchStation(self, selectedIndex):
		# switch station online
		station = self.stationCache[selectedIndex]
		
		try:
			self.pandora.switchStation(station['stationId'])
		except AuthenticationError:
			self.pandora.authenticate(username=self.cf.settings['PANDORA_USERNAME'], password=self.cf.settings['PANDORA_PASSWORD'])
			self.pandora.switchStation(station['stationId'])
	
	def mute(self):
		if bass.BASS_GetVolume() == 0.0:
			bass.BASS_SetVolume(self.old_volume)
		else:
			self.old_volume = bass.BASS_GetVolume()
			bass.BASS_SetVolume(0.0)
	
	def newSong(self, song):
		self.newSongBegan.emit(song)
	
	def newSongInternal(self, song):
		i = self.trackModel.addSong(song)
		
		# resize stuff
		self.ui.lstSongs.resizeRowToContents(0)
		self.ui.lstSongs.resizeRowToContents(1)
		self.ui.lstSongs.resizeColumnsToContents()
	
	def settings(self):
		f = SettingsForm(self)
		f.open()
	
	def quit(self):
		QApplication.exit()
	


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = MainForm()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())