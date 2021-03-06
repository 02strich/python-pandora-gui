# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyside_main.ui'
#
# Created: Sat Apr 13 19:18:39 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

import os.path

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 206)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../pandora.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnPlay = QtGui.QToolButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "icons/control_play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPlay.setIcon(icon1)
        self.btnPlay.setObjectName("btnPlay")
        self.horizontalLayout.addWidget(self.btnPlay)
        self.btnPause = QtGui.QToolButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "icons/control_pause.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPause.setIcon(icon2)
        self.btnPause.setObjectName("btnPause")
        self.horizontalLayout.addWidget(self.btnPause)
        self.btnNext = QtGui.QToolButton(Dialog)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "icons/control_end.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNext.setIcon(icon3)
        self.btnNext.setObjectName("btnNext")
        self.horizontalLayout.addWidget(self.btnNext)
        self.btnMute = QtGui.QToolButton(Dialog)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "icons/sound_mute.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMute.setIcon(icon4)
        self.btnMute.setObjectName("btnMute")
        self.horizontalLayout.addWidget(self.btnMute)
        self.btnUnmute = QtGui.QToolButton(Dialog)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "icons/sound_none.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUnmute.setIcon(icon5)
        self.btnUnmute.setObjectName("btnUnmute")
        self.horizontalLayout.addWidget(self.btnUnmute)
        self.btnSettings = QtGui.QToolButton(Dialog)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "icons/wrench.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSettings.setIcon(icon6)
        self.btnSettings.setObjectName("btnSettings")
        self.horizontalLayout.addWidget(self.btnSettings)
        self.cbStations = QtGui.QComboBox(Dialog)
        self.cbStations.setObjectName("cbStations")
        self.horizontalLayout.addWidget(self.cbStations)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.lstSongs = QtGui.QTableView(Dialog)
        self.lstSongs.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lstSongs.setAutoScroll(False)
        self.lstSongs.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.lstSongs.setAlternatingRowColors(True)
        self.lstSongs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.lstSongs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.lstSongs.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.lstSongs.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.lstSongs.setShowGrid(False)
        self.lstSongs.setObjectName("lstSongs")
        self.lstSongs.horizontalHeader().setVisible(False)
        self.lstSongs.horizontalHeader().setStretchLastSection(True)
        self.lstSongs.verticalHeader().setVisible(False)
        self.lstSongs.verticalHeader().setDefaultSectionSize(100)
        self.verticalLayout_2.addWidget(self.lstSongs)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Python Pandora", None, QtGui.QApplication.UnicodeUTF8))

