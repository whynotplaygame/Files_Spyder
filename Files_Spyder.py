# -*- coding: utf-8 -*-
# 
# project: Files Spyder
# summary:  this is a tool which can help user to serch target text in many files. 
#           it supports CSV,XLS and txt
# author : why
# build  : 1.0
# date   : 2019.08.11

import sys
import os
import time
from enum import Enum

import threading

from mainui import Ui_Form

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtCore import *

# 主窗口类
class mainUI(QWidget, Ui_Form):
	def __init__(self):
		super(mainUI,self).__init__()
		self.setupUi(self)
		self.setMainUi()
		self.initMainUi()

	# 设置窗口的基本属性
	def setMainUi(self):
		pass

	# 初始化窗口
	def initMainUi(self):

		# 为查找按钮绑定槽函数work()
		self.pushButton.clicked.connect(self.work)

		# radioButton 默认选择为CSV类型文件
		self.radioButton_csv.setChecked(True)

		# 为三种文件类型radiobutton绑定槽函数
		self.radioButton_csv.toggled.connect(lambda:self.radioButtonState(self.radioButton_csv))
		self.radioButton_xls.toggled.connect(lambda:self.radioButtonState(self.radioButton_xls))
		self.radioButton_gbc.toggled.connect(lambda:self.radioButtonState(self.radioButton_gbc))

		# 默认搜索文件类型为CSV
		self.fileType = '.csv'
		self.label_7.setText('准备就绪。。。。')

		# 是否可以执行work函数
		# 防止target为空
		self.isCanWork = True

		self.tableWidget.setColumnWidth(0,600)
		self.tableWidget.setColumnWidth(1,50)
		self.tableWidget.setColumnWidth(2,50)
		self.tableWidget.setColumnWidth(3,100)

		# self.tableWidget.setHorizontalHeaderLabels(['路径','类型','行号','操作'])


	# 主要的功能函数
	def work(self):
		QApplication.processEvents()
		self.label_7.setText('开始干活儿喽。。。。')
		# 每次按下 查找 按钮后 需要重置的内容
		global global_file_list
		global_file_list.clear()
		self.tableWidget.clear()
		QApplication.processEvents()
		self.tableWidget.setRowCount(0)
		QApplication.processEvents()

		# 获得搜索相关条件
		targetDir = self.getTagetDir()
		target = self.getTarget()
		fileType = self.getFileType()
		skipFiles = self.getSkipFiles()


		if self.isCanWork == True:
			#fff = (targetDir,target,fileType,skipFiles)
			self.getfiles = getAllLatentFiles(fileType,targetDir)
			self.getfiles.start()
			self.getfiles.sinOut.connect(self.stateLabel)
			self.getfiles.sinFinish.connect(lambda:self.findfuc(target,fileType,skipFiles))

	
	# 获得目标目录
	def getTagetDir(self):
		if len(self.lineEdit_dir.text()) == 0:
			return '.'
		return self.lineEdit_dir.text()

	# 获得搜索目标
	def getTarget(self):
		print('geting target func...')
		if len(self.lineEdit_target.text()) == 0:
			self.label_7.setText('目标必填！！！！')
			self.isCanWork = False
		else:
			self.isCanWork = True
			return self.lineEdit_target.text()

	# 获得文件类型
	def getFileType(self):
		return self.fileType

	# radiobutton 状态槽函数
	def radioButtonState(self,radiobutton):
		if radiobutton.text() == '*.CSV':
			if radiobutton.isChecked() == True:
				self.fileType = '.csv'

		if radiobutton.text() == '*.XLS':
			if radiobutton.isChecked() == True:
				self.fileType = '.xls'

		if radiobutton.text() == '*.gbc':
			if radiobutton.isChecked() == True:
				self.fileType = '.gbc'

	# 获得跳过内容
	def getSkipFiles(self):
		return []

	# 状态label_7的槽函数
	def stateLabel(self,str_from_threading):
		self.label_7.setText(str_from_threading)


	# 三种文件搜索线程的初始化和启动
	def findfuc(self,target, ft ,skip):
		global global_file_list
		#print(target,ft,skip)

		if len(global_file_list) == 0:
			self.label_7.setText('没有找到指定类型的文件！')
			return 
		if ft == '.csv':
			print('查找csv文件')
			self.find = findTargetFromCsvFiles(target,global_file_list,skip)
			self.find.sinOutResult.connect(self.insertTable)
			self.find.sinOutBlank.connect(self.stateLabel)
			self.find.start()

		elif ft == '.xls':
			print('查找xls文件')
			self.find = findTargetFromXlsFiles(target,global_file_list,skip)
			self.find.start()
			self.find.sinOutState.connect(self.stateLabel)
			self.find.sinOutResult.connect(self.insertTable)
			self.find.sinOutBlank.connect(self.stateLabel)
		elif ft == '.gbc':
			print('查找gbc文件')
			self.find = findTargetFromGbcFiles(target,global_file_list,skip)
			self.find.start()
			self.find.sinOutState.connect(self.stateLabel)
			self.find.sinOutResult.connect(self.insertTable)
			self.find.sinOutBlank.connect(self.stateLabel)


		#print('查找潜在文件列表结束')


	# 更新表格数据
	def insertTable(self,row,path,cell,rown):
		print('calling insertable and row: %d  path: %s, cell:%s, row number: %d' % (row, path,cell, rown) )
		self.tableWidget.insertRow(row-1)
		self.tableWidget.setHorizontalHeaderLabels(['路径','概况','行号','操作'])
		item = QtWidgets.QTableWidgetItem(path)
		self.tableWidget.setItem(row-1,0,item)

		item = QtWidgets.QTableWidgetItem(cell)
		self.tableWidget.setItem(row-1,1,item)

		item = QtWidgets.QTableWidgetItem(str(rown))
		self.tableWidget.setItem(row-1,2,item)

		item = QtWidgets.QTableWidgetItem('Check')
		self.tableWidget.setItem(row-1,3,item)

	# 打开配置
	def openIniFile(self):
		pass

##############################################

from enum import Enum

# 文件类型枚举
class filetypeEnum(Enum):
	xls = r'.xls'
	csv = r'.csv'
	gbc = r'.gbc'

global_file_list = []

# 从指定目录获取指定文件类型的文件序列
class getAllLatentFiles(QThread):

	sinOut = pyqtSignal(str)
	sinFinish = pyqtSignal()

	def __init__(self, filetype, dir_path):
		super(getAllLatentFiles,self).__init__()
		self.filetype = filetype
		self.dir_path = dir_path
		print('搜索指定类型线程中。。。。')

	def __del__(self):
		self.wait()

	def run(self):
		global global_file_list

		for root,dirs,files in os.walk(self.dir_path):
			QApplication.processEvents()
			for file in files:
				QApplication.processEvents()
				if self.filetype == '.xls':
					xlsType = ['.xls','.xlsx','.xlsm','.xlt','.et']
					if os.path.splitext(file)[1] in xlsType:
						print('I got a file. hahahhahahahhahahhah')
						global_file_list.append(os.path.join(root,file))
				else:
					if os.path.splitext(file)[1] == self.filetype:
						print('I got a file. hahahhahahahhahahhah')
						global_file_list.append(os.path.join(root,file))
		#print(global_file_list)
		#time.sleep(10)
		self.sinOut.emit('已经查到到的 %s 类型文件，数量为 %d 个' % (self.filetype,len(global_file_list)))	
		self.sinFinish.emit()			

#		return (self.filetype,file_list)


##############################################

import xlrd
import csv

# 分析表格线程
class findTargetFromXlsFiles(QThread):
	sinOutState = pyqtSignal(str)
	sinOutResult = pyqtSignal(int,str,str,int) #信号：结果号，文件路径，表格内容，行号
	sinOutBlank = pyqtSignal(str)

	def __init__(self, target, filelsit,skipfiles):
		super(findTargetFromXlsFiles,self).__init__()
		self.target = target
		self.filelsit = filelsit
		self.skipfiles = skipfiles
		print('查找xls表格文件线程中。。。')

	def __del__(self):
		self.wait()

	def run(self):
		self.sinOutState.emit('开始检索Xls文件')
		result = []
		for file in self.filelsit:
			book = xlrd.open_workbook(file)
			sheetsList= book.sheet_names()

			for sheetname in sheetsList:
				sheet = book.sheet_by_name(sheetname)
				#print(sheetname)
				#print(sheet)
				for i in range(sheet.nrows):
					# print('{} 的内容为：{}'.format(file,sheet.row_values(i)))
					cells = sheet.row_values(i)
					for cell in cells:
						#print('cell的内容为{}'.format(cell))
						if isinstance(cell,int) == True:
							#print('I got int cell and content is : {}'.format(str(cell)))
							if self.target in str(cell):
								#print('then I got the target in this cell: and row number is {}'.format(str(cell),i))
								result.append(file)
								self.sinOutResult.emit(len(result),file,cell)
								time.sleep(0.2)
						elif isinstance(cell,float) == True:
							#print('I got float cell and content is : {}'.format(str(cell)))
							if self.target in str(cell):
								#print('then I got the target in this cell: {} and row number is {}'.format(str(cell),i))
								result.append(file)
								#self.sinOutReult.emit(len(result),file)
								self.sinOutResult.emit(len(result),file,str(cell),i)
								time.sleep(0.2)
						elif isinstance(cell,str) == True:
							#print('I got string cell and content is : {}'.format(str(cell)))
							if self.target in cell:
								#print('then I got the target in this cell: {} and row number is {}'.format(str(cell),i))
								result.append(file)
								self.sinOutResult.emit(len(result),file,cell,i)
								time.sleep(0.2)

		if len(result) == 0:
			self.sinOutBlank.emit('没有搜索到目标内容')							
#		print(result)


# 分析CSV文件线程
class findTargetFromCsvFiles(QThread):

	sinOutState = pyqtSignal(str)
	sinOutResult = pyqtSignal(int,str,str,int) #信号：结果号，文件路径，表格内容，行号
	sinOutBlank = pyqtSignal(str)

	def __init__(self, target, filelsit,skipfiles):
		super(findTargetFromCsvFiles,self).__init__()
		self.target = target
		self.filelsit = filelsit
		self.skipfiles = skipfiles
		print('查找CSV文件线程中。。。')

	def __del__(self):
		self.wait()

	def run(self):
		self.sinOutState.emit('开始检索CSV文件')
		result = []
		for file in self.filelsit:
			QApplication.processEvents()
			csv_file = csv.reader(open(file, 'r'))
			number = 1
			for line in csv_file:
				QApplication.processEvents()
				for cell in line:
					QApplication.processEvents()
					if self.target in cell:
						result.append(file)
						self.sinOutState.emit('开始检索CSV文件中。。。。')
						self.sinOutState.emit('开始检索CSV文件中。。。。。。。。。。')
						self.sinOutResult.emit(len(result), file, cell,number)
						time.sleep(0.2)

				number= number + 1

		if len(result) == 0:
			self.sinOutBlank.emit('没有搜索到目标内容')

# 分析gbc文件线程
class findTargetFromGbcFiles(QThread):

	sinOutState = pyqtSignal(str)
	sinOutResult = pyqtSignal(int,str,str,int) #信号：结果号，文件路径，表格内容，行号
	sinOutBlank = pyqtSignal(str)

	def __init__(self, target, filelsit,skipfiles):
		super(findTargetFromGbcFiles,self).__init__()
		self.target = target
		self.filelsit = filelsit
		self.skipfiles = skipfiles
		print('查找gbc文件线程中。。。')

	def __del__(self):
		self.wait()

	def run(self):
		self.sinOutState.emit('开始检索gbc文件')
		result = []
		for file in self.filelsit:
			with open(file,'r') as f:
				number = 1
				for line in f:
					#print('line的内容为: %s' % line)
					if self.target in line:
						result.append(file)
						self.sinOutResult.emit(len(result), file, line,number)
					number = number + 1

		print(result)
		if len(result)== 0:
			self.sinOutBlank.emit('没有搜索到目标内容')


###############################################



if __name__ == '__main__':
	# sercher = getAllLatentFiles(filetypeEnum.gbc.value,'.')
	# sercher.serch()
	app = QApplication(sys.argv)
	mainui = mainUI()
	mainui.show()
	sys.exit(app.exec_())



