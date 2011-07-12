# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Tue Jul 12 15:49:08 2011
#      by: pyside-uic 0.2.11 running on PySide 1.0.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 220)
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
        self.btnPlay.setObjectName("btnPlay")
        self.horizontalLayout.addWidget(self.btnPlay)
        self.btnNext = QtGui.QToolButton(Dialog)
        self.btnNext.setObjectName("btnNext")
        self.horizontalLayout.addWidget(self.btnNext)
        self.btnMute = QtGui.QToolButton(Dialog)
        self.btnMute.setObjectName("btnMute")
        self.horizontalLayout.addWidget(self.btnMute)
        self.cbStations = QtGui.QComboBox(Dialog)
        self.cbStations.setObjectName("cbStations")
        self.horizontalLayout.addWidget(self.cbStations)
        self.btnQuit = QtGui.QToolButton(Dialog)
        self.btnQuit.setObjectName("btnQuit")
        self.horizontalLayout.addWidget(self.btnQuit)
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
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPlay.setText(QtGui.QApplication.translate("Dialog", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNext.setText(QtGui.QApplication.translate("Dialog", ">>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMute.setText(QtGui.QApplication.translate("Dialog", "@", None, QtGui.QApplication.UnicodeUTF8))
        self.btnQuit.setText(QtGui.QApplication.translate("Dialog", "Q", None, QtGui.QApplication.UnicodeUTF8))

