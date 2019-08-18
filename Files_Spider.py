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
from PyQt5.QtWidgets import QApplication,QWidget,QTableWidgetItem,QTableWidget,QFileDialog
from PyQt5.QtCore import *
import configparser
import res_rc
from PyQt5.QtGui import QPalette,QBrush,QPixmap



# 主窗口类
class mainUI(QWidget, Ui_Form):
	def __init__(self):
		super(mainUI,self).__init__()
		self.setupUi(self)
		self.setMainUi()
		self.initMainUi()

	# 设置窗口的基本属性
	def setMainUi(self):
		self.setWindowTitle('Files spyder')
		self.setFixedSize(851,695)

	# 初始化窗口
	def initMainUi(self):

		# 为查找按钮绑定槽函数work()
		self.pushButton.clicked.connect(self.work)

		# 为跳过内容配置 按钮 绑定槽函数
		self.toolButton.clicked.connect(self.openSkipIniFile)

		# 声明且初始化从配置文件中获得跳过文件名
		self.skipFilesInIniFile = []

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

		#self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers0No)
		self.tableWidget.itemClicked.connect(self.showFileOfClikcedItem)



	# 主要的功能函数
	def work(self):
		#QApplication.processEvents()
		self.label_7.setText('开始干活儿喽。。。。')
		# 每次按下 查找 按钮后 需要重置的内容
		global global_file_list
		global_file_list.clear()
		self.tableWidget.clear()
		self.tableWidget.setRowCount(0)

		# 由于在重置 查找 时，用了self.tableWidget.clear() 已清掉所有内容，包括表头，所以在此地设置。
		self.tableWidget.setHorizontalHeaderLabels(['路径','概况','行号','操作'])

		# 获得搜索相关条件
		targetDir = self.getTagetDir()
		target = self.getTarget()
		fileType = self.getFileType()
		skipFiles = self.getSkipFiles()


		if self.isCanWork == True:
			fff = (targetDir,target,fileType,skipFiles)
			print (fff)
			self.getfiles = getAllLatentFiles(fileType,targetDir)
			self.getfiles.start()
			self.getfiles.sinOut.connect(self.stateLabel)
			self.getfiles.sinFinish.connect(lambda:self.findfuc(target,fileType,skipFiles))

	
	# 获得目标目录
	def getTagetDir(self):
		if len(self.lineEdit_dir.text()) == 0:
			#return r'E:\BaiduNetdiskDownload\sercher_final\csv_folder' # 测试配置
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

		# 汇总跳过文件名序列
		total_skip_file = []

		# 获得从输出框中的文字
		custom_skip_file_str = self.lineEdit_skip.text()

		if len(custom_skip_file_str) == 0:
			total_skip_file = self.skipFilesInIniFile
		else:
			# 将输入框中获得的文字拆分成序列，以逗号分割
			custom_skip_file_lsit = custom_skip_file_str.split(',')
			# 自定义跳过 + 配置文件中的文件名 = 总共需要跳过的文件
			total_skip_file = custom_skip_file_lsit + self.skipFilesInIniFile

		# 去重，防止自定义与配置中重复，以免导致过滤函数中的remove函数导致问题。
		total_skip_file = list(set(total_skip_file))
		return total_skip_file

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
			self.find.sinOutState.connect(self.stateLabel)
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
		# print('calling insertable and row: %d  path: %s, cell:%s, row number: %d' % (row, path,cell, rown) )
		self.tableWidget.insertRow(row-1)
		#self.tableWidget.setHorizontalHeaderLabels(['路径','概况','行号','操作'])
		item = QtWidgets.QTableWidgetItem(path)
		self.tableWidget.setItem(row-1,0,item)

		item = QtWidgets.QTableWidgetItem(cell)
		self.tableWidget.setItem(row-1,1,item)

		item = QtWidgets.QTableWidgetItem(str(rown))
		self.tableWidget.setItem(row-1,2,item)

		item = QtWidgets.QTableWidgetItem('Check')
		self.tableWidget.setItem(row-1,3,item)


	# 查看按钮的槽函数，用于获取路径并启动查看文件线程。
	def showFileOfClikcedItem(self,item):
		if item.text() == 'Check':
			#print('您想看这个表啊。。。。')
			pathItem = self.tableWidget.item(item.row(),0)
			pathItemText = pathItem.text()
			self.checkFileThread = checkFileThread(pathItemText)
			self.checkFileThread.start()

			#print(row.text())
	

	# 打开配置
	def openSkipIniFile(self):
		# 打开当前目录的dialog
		fname, _ = QFileDialog.getOpenFileName(self,'open file','.',"INI file(*.ini)")

		print(fname)

		# 如果没有选择文件，直接返回
		if len(fname) == 0 :
			return -1

		# 读取配置文件
		config = configparser.ConfigParser()
		config.read_file(open(fname))
		xls = config.get('skipFiles','skipXls')
		csv = config.get('skipFiles','skipCsv')
		gbc = config.get('skipFiles','skipGbc')

		all_files = xls + ',' + csv + ',' + gbc
		#print(xls,'\n', csv,'\n',gbc,'\n',all_files)
		#print(len(all_files))
		self.skipFilesInIniFile = all_files.split(',')
		print(self.skipFilesInIniFile)


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
						#print('I got a file. hahahhahahahhahahhah')
						global_file_list.append(os.path.join(root,file))
				else:
					if os.path.splitext(file)[1] == self.filetype:
						#print('I got a file. hahahhahahahhahahhah')
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

		# 去self.filelist中的需要跳过的文件
		cleanr = removeSKipFileFromOrigionalFileList(self.skipfiles,self.filelsit)
		cleanedFileList = cleanr.do()

		self.sinOutState.emit('开始检索Xls文件')
		result = []

		for file in cleanedFileList:
		#for file in self.filelsit:
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
						# 由于cell的数据类型不同，需要分别进行处理。
						if isinstance(cell,int) == True:
							#print('I got int cell and content is : {}'.format(str(cell)))
							if self.target in str(cell):
								#print('then I got the target in this cell: and row number is {}'.format(str(cell),i))
								result.append(file)

								# 由于xls 包含N个sheet,所以应显示为具体哪个sheet下的行号下的cell内容。
								summary = '%s： %d' % (sheetname,cell)
								self.sinOutResult.emit(len(result),file,summary,i)
								time.sleep(0.2)
						elif isinstance(cell,float) == True:
							#print('I got float cell and content is : {}'.format(str(cell)))
							if self.target in str(cell):
								#print('then I got the target in this cell: {} and row number is {}'.format(str(cell),i))
								result.append(file)
								
								# 由于xls 包含N个sheet,所以应显示为具体哪个sheet下的行号下的cell内容。
								summary = '%s： %s' % (sheetname,str(cell))								
								#self.sinOutResult.emit(len(result),file,str(cell),i)
								self.sinOutResult.emit(len(result),file,summary,i)
								time.sleep(0.2)
						elif isinstance(cell,str) == True:
							#print('I got string cell and content is : {}'.format(str(cell)))
							if self.target in cell:
								#print('then I got the target in this cell: {} and row number is {}'.format(str(cell),i))
								result.append(file)

								# 由于xls 包含N个sheet,所以应显示为具体哪个sheet下的行号下的cell内容。								
								summary = '%s： %s' % (sheetname,cell)
								self.sinOutResult.emit(len(result),file,summary,i)								
								#self.sinOutResult.emit(len(result),file,cell,i)
								time.sleep(0.2)

		if len(result) == 0:
			self.sinOutBlank.emit('没有搜索到目标内容')
		else:
			self.sinOutBlank.emit('已搜索到以下内容。。。您可以点击Check并查看')							
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
		# 去self.filelist中的需要跳过的文件
		cleanr = removeSKipFileFromOrigionalFileList(self.skipfiles,self.filelsit)
		cleanedFileList = cleanr.do()

		self.sinOutState.emit('开始检索CSV文件')
		result = []
		for file in cleanedFileList:		
		#for file in self.filelsit:
			QApplication.processEvents()
			csv_file = csv.reader(open(file, 'r'))
			number = 1
			for line in csv_file:
				QApplication.processEvents()
				for cell in line:
					QApplication.processEvents()
					if self.target in cell:
						result.append(file)
						self.sinOutResult.emit(len(result), file, cell,number)
						time.sleep(0.2)

				number= number + 1

		if len(result) == 0:
			self.sinOutBlank.emit('没有搜索到目标内容')
		else:
			self.sinOutBlank.emit('已搜索到以下内容。。。您可以点击Check并查看')	

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
		# 去self.filelist中的需要跳过的文件
		cleanr = removeSKipFileFromOrigionalFileList(self.skipfiles,self.filelsit)
		cleanedFileList = cleanr.do()

		self.sinOutState.emit('开始检索gbc文件')

		result = []
		for file in cleanedFileList:
		#for file in self.filelsit:
			with open(file,'r') as f:
				number = 1
				for line in f:
					#print('line的内容为: %s' % line)
					if self.target in line:
						result.append(file)
						self.sinOutResult.emit(len(result), file, line,number)
					number = number + 1

		#print(result)
		if len(result)== 0:
			self.sinOutBlank.emit('没有搜索到目标内容')
		else:
			self.sinOutBlank.emit('已搜索到以下内容。。。您可以点击Check并查看')


###############################################

# 查看打开文件线程 
class checkFileThread(threading.Thread):
	def __init__(self,filepath):
		super(checkFileThread,self).__init__()
		self.filepath = filepath

	def run(self):
		os.system(self.filepath)

###############################################

# 功能为去掉原始列表中，以skipFiles中的文件名为的元素。
class removeSKipFileFromOrigionalFileList():
	def __init__(self,skipFiles,OrigionalFiles):
		self.skipFiles = skipFiles
		self.OrigionalFiles = OrigionalFiles
		
	def do(self):
		for file in self.OrigionalFiles:
			for skip in self.skipFiles:
				if skip in file:
					self.OrigionalFiles.remove(file)
		return self.OrigionalFiles


###############################################



if __name__ == '__main__':
	# sercher = getAllLatentFiles(filetypeEnum.gbc.value,'.')
	# sercher.serch()
	app = QApplication(sys.argv)
	mainui = mainUI()

	qssStyle = '''
				QPushButton{
					background-color : white
				}
				QPushButton:hover{
					background-image : url(:/pic/ui/Seek-no-bg.png)
				}
				QPushButton:pressed{
					background-color : gray
				}

	'''

	mainui.setStyleSheet(qssStyle)

	palette = QPalette()
	palette.setBrush(QPalette.Background,QBrush(QPixmap(":/pic/ui/背景2.jpg")))
	mainui.setPalette(palette)

	mainui.show()
	sys.exit(app.exec_())



