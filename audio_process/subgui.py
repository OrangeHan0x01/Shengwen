import sys
from PyQt5.QtWidgets import QApplication, QWidget,QLabel
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,QThread , pyqtSignal
import time

class subgui:
	def __init__(self,sub_path,font_size=18,height=100,width=1500,x=400,y=950):#使用：一个函数subgui.subgui('test_output/subtitle.txt')即可
		self.timer = QTimer()
		self.timer.timeout.connect(self.display)
		font = QtGui.QFont()
		font.setPointSize(font_size)
		self.count=0
		self.app = QApplication(sys.argv)
		self.w = QWidget()
		self.w.setWindowTitle('Simple')
		self.w.resize(width, height)
		self.w.move(x, y)
		self.w.setWindowOpacity(0.85)
		self.w.setWindowFlags(self.w.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.w.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.w.label = QLabel(self.w)
		self.w.label.setGeometry(QtCore.QRect(0, 0, width, height)) #(x, y, width, height)
		self.w.setFont(font)
		print('初始化完毕')
		fp=open(sub_path,encoding='utf8')
		self.data_buf=fp.readlines()
		self.data_len=len(self.data_buf)
		fp.close()
		print('已读取文件')
		self.display()
		self.w.show()
		sys.exit(self.app.exec_())

	def display(self):
		if(self.count<=self.data_len):
			line=self.data_buf[self.count]
			self.count+=1
			sentence,start,span = line.split('& ')
			start,span=map(float,(start,span))
			strT = '<span style=\" color: #ff0000;\">%s</span>' %(sentence)
			print(strT)
			self.w.label.setText("%s" %(strT))
			QApplication.processEvents()
			print('[',self.count-1,']wait:',span)
			self.timer.start(span*1000)
		else:
			print('播放完毕！')
			sys.exit()
	



