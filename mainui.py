# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(851, 695)
        Form.setStyleSheet("")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(240, 0, 321, 51))
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 50, 541, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_dir = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_dir.setText("")
        self.lineEdit_dir.setObjectName("lineEdit_dir")
        self.horizontalLayout.addWidget(self.lineEdit_dir)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_target = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_target.setObjectName("lineEdit_target")
        self.horizontalLayout_2.addWidget(self.lineEdit_target)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.radioButton_csv = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_csv.setObjectName("radioButton_csv")
        self.horizontalLayout_3.addWidget(self.radioButton_csv)
        self.radioButton_xls = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_xls.setObjectName("radioButton_xls")
        self.horizontalLayout_3.addWidget(self.radioButton_xls)
        self.radioButton_gbc = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_gbc.setObjectName("radioButton_gbc")
        self.horizontalLayout_3.addWidget(self.radioButton_gbc)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.lineEdit_skip = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_skip.setObjectName("lineEdit_skip")
        self.horizontalLayout_4.addWidget(self.lineEdit_skip)
        self.toolButton = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_4.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(580, 50, 251, 131))
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(20, 340, 72, 15))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(20, 240, 811, 16))
        self.label_7.setObjectName("label_7")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(20, 190, 821, 51))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 290, 831, 391))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><img src=\":/pic/ui/title.png\"/></p></body></html>"))
        self.label_2.setText(_translate("Form", "目录"))
        self.lineEdit_dir.setPlaceholderText(_translate("Form", "默认为当前目录"))
        self.label_3.setText(_translate("Form", "目标"))
        self.lineEdit_target.setPlaceholderText(_translate("Form", "必填！"))
        self.label_4.setText(_translate("Form", "类型"))
        self.radioButton_csv.setText(_translate("Form", "*.CSV"))
        self.radioButton_xls.setText(_translate("Form", "*.XLS"))
        self.radioButton_gbc.setText(_translate("Form", "*.gbc"))
        self.label_5.setText(_translate("Form", "跳过"))
        self.lineEdit_skip.setToolTip(_translate("Form", "<html><head/><body><p>跳过内容配置 之外的临时配置，需要,间隔。</p></body></html>"))
        self.lineEdit_skip.setWhatsThis(_translate("Form", "<html><head/><body><p>在 跳过内容配置 之外，临时跳过的文件名。用逗号间隔。</p></body></html>"))
        self.lineEdit_skip.setPlaceholderText(_translate("Form", "跳过内容配置之外的临时配置。逗号间隔。"))
        self.toolButton.setText(_translate("Form", "跳过内容配置"))
        self.pushButton.setText(_translate("Form", "查找"))
        self.label_7.setToolTip(_translate("Form", "<html><head/><body><p>dddddd</p></body></html>"))
        self.label_7.setText(_translate("Form", "。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "路径"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "概况"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "行号"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "操作"))
import res_rc
