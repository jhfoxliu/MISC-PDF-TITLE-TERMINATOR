#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author  : Jianheng Liu
Date    : 20190618
Liscence: MIT
"""

import sys
from PyQt5.QtWidgets import QDialog,QLabel, QVBoxLayout, QMainWindow, QApplication, QWidget, QPushButton, QGridLayout,QTextEdit, QLineEdit
from PyQt5.QtGui import QFont
import copy
from functools import partial

replace_dict = {\
":":" ",
"|":" ",
"<":" ",
">":" ",
"?":" ",
"*":" ",
"/":" ",
"\\":" ",
"\"":" ",
"\r\n":" ",
"\n":" ",
}

class SettingWindow(QDialog):
	def __init__(self,reference):
		super(QWidget,self).__init__()
		self.newWindowUI()
		self.temp_dict = copy.deepcopy(reference)
		self.temp = None
		
	def newWindowUI(self):
		layout = QVBoxLayout()
		self.setLayout(layout)
		self.setWindowTitle('Settings')
		

		newLayout = QGridLayout()
		layout.addLayout(newLayout)
		n = 0
		for match, sub in replace_dict.items():
			if match == "\n":
				show_match = "LF"
			elif match == "\r\n":
				show_match = "CRLF"
			else:
				show_match = match
			
			if sub == " ":
				show_sub = "<space>"
			elif sub == "\n" or sub == "\r\n":
				show_sub = "<enter>"
			elif sub == "":
				show_sub = "<del>"
			else:
				show_sub = sub
			newLayout = QGridLayout()
			layout.addLayout(newLayout)
			
			LEFT = QLineEdit("%s" % show_match)
			LEFT.setReadOnly(True)
			RIGHT =  QLineEdit()

			RIGHT.setPlaceholderText(show_sub)
			RIGHT.textChanged.connect(partial(self.ChangeDict,match))
			DEL = QPushButton("delete")
			DEL.clicked.connect(partial(self.DeleteString,match,RIGHT))
			
			# CB = QCheckBox()
			# if sub == "":
				# CB.setChecked(True)
			# else:
				# CB.setChecked(False)
			# CB.stateChanged.connect(self.checkLanguage)
			
			# newLayout.addWidget(CB, n, 0, 1 , 1)
			newLayout.addWidget(LEFT, n, 0, 1, 1)
			newLayout.addWidget(QLabel(">>"), n,1, 1 , 1)
			newLayout.addWidget(RIGHT, n, 2, 1 , 1)
			newLayout.addWidget(DEL, n, 3, 1 , 1)
			# newLayout.addWidget(LEFT, n, 0)
			# newLayout.addWidget(QLabel(">>"),n, 1 )
			# newLayout.addWidget(RIGHT, n, 2)
			# newLayout.addWidget(DEL, n, 3)
			# newLayout.setColumnStretch(n, 6)
			
			n += 1
			
		newLayout = QGridLayout()
		layout.addLayout(newLayout)
		
		saveBottun = QPushButton("Save && Exit")
		saveBottun.clicked.connect(self.SaveAndExit)
		layout.addWidget(saveBottun) #,0,0,0,1
	
		ExitBottun = QPushButton("Exit")
		ExitBottun.clicked.connect(self.ExitWithoutSave)
		layout.addWidget(ExitBottun) #,0,1,0,1
		
		self.setGeometry(1100, 200, 250, 300)

	
	def ExitWithoutSave(self):
		self.temp_dict = copy.deepcopy(replace_dict)
		self.close()
	
	def SaveAndExit(self):
		global replace_dict
		replace_dict = copy.deepcopy(self.temp_dict)
		self.close()
	
	def DeleteString(self,KEY,RIGHT):
		self.temp_dict[KEY] = ""
		RIGHT.setPlaceholderText("<del>")
	
	def ChangeDict(self,KEY,text):
		self.temp_dict[KEY] = text
		
	
class MainWindow(QWidget):
	def __init__(self):
		super(QWidget,self).__init__()
		self.initUI()

	def initUI(self):
		self.setGeometry(1400, 100, 300, 600)
		self.setWindowTitle('PDF Title Terminator')
		layout = QVBoxLayout()
		
		self.sublayout_1 = QGridLayout()
		self.sublayout_2 = QGridLayout()
		self.sublayout_3 = QGridLayout()
		
		layout.addLayout(self.sublayout_1)
		layout.addLayout(self.sublayout_2)
		layout.addLayout(self.sublayout_3)
		
		self.setLayout(layout)
		
		self.inputbox = QTextEdit(self)
		self.inputbox.setPlaceholderText("Please enter PDF title here.")
		self.inputbox.setFont(QFont("Arial", 12))
		self.inputLabel = QLabel("Input:")
		self.inputLabel.setFont(QFont("Arial", 12, QFont.Bold))
		self.sublayout_1.addWidget(self.inputLabel,0,0,1,3)
		self.sublayout_1.addWidget(self.inputbox,1,0,1,3)
		self.sublayout_1.setContentsMargins(0,0,0,-2.5)
		
		self.outputbox = QTextEdit(self)
		self.outputbox.setPlaceholderText("Output will be shown here.")
		self.outputbox.setFont(QFont("Arial", 12))
		self.outputLabel = QLabel("Output:")
		self.outputLabel.setFont(QFont("Arial", 12, QFont.Bold))
		self.sublayout_2.addWidget(self.outputLabel,0,0,1,3)
		self.sublayout_2.addWidget(self.outputbox,1,0,1,3)
		self.sublayout_2.setContentsMargins(0,0,0,0)
		
		self.settingButton = QPushButton("Settings")
		self.settingButton.clicked.connect(self.show_settings)
		self.sublayout_3.addWidget(self.settingButton,0,0,0,1)
		
		self.exitButton = QPushButton("Exit")
		self.exitButton.clicked.connect(self.close)
		self.sublayout_3.addWidget(self.exitButton,0,2,0,1)
		
		self.inputbox.textChanged.connect(self.show_modified_text)
		
		self.show()
    
	def show_modified_text(self):
		text = self.inputbox.toPlainText()
		
		for match, target in replace_dict.items():
			text = text.replace(match,"■")
			self.outputbox.setPlainText(text)

			text = text.replace("■",target)
			self.outputbox.setPlainText(text)
	
	def show_settings(self):
		global replace_dict
		newWindow = SettingWindow(replace_dict)
		newWindow.show()
		# newWindow.exec_()
		
	def closeEvent(self,event):
		sys.exit(app.exec_())
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())