# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_function.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cam_Dialog(object):
    def setupUi(self, cam_Dialog):
        cam_Dialog.setObjectName("cam_Dialog")
        cam_Dialog.resize(640, 560)
        self.cam_label = QtWidgets.QLabel(cam_Dialog)
        self.cam_label.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.cam_label.setText("")
        self.cam_label.setObjectName("cam_label")
        self.tabWidget = QtWidgets.QTabWidget(cam_Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 480, 640, 80))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.record_button = QtWidgets.QPushButton(self.tab)
        self.record_button.setGeometry(QtCore.QRect(490, 10, 71, 41))
        self.record_button.setObjectName("record_button")
        self.LineEdit_username = QtWidgets.QLineEdit(self.tab)
        self.LineEdit_username.setGeometry(QtCore.QRect(90, 20, 113, 20))
        self.LineEdit_username.setObjectName("LineEdit_username")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 25, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(290, 25, 54, 12))
        self.label_2.setObjectName("label_2")
        self.comboBox_id = QtWidgets.QComboBox(self.tab)
        self.comboBox_id.setGeometry(QtCore.QRect(330, 20, 69, 22))
        self.comboBox_id.setObjectName("comboBox_id")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.comboBox_username = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_username.setGeometry(QtCore.QRect(120, 20, 69, 22))
        self.comboBox_username.setObjectName("comboBox_username")
        self.verify_button = QtWidgets.QPushButton(self.tab_2)
        self.verify_button.setGeometry(QtCore.QRect(410, 10, 71, 41))
        self.verify_button.setObjectName("verify_button")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(40, 25, 54, 12))
        self.label_3.setObjectName("label_3")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(cam_Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(cam_Dialog)

    def retranslateUi(self, cam_Dialog):
        _translate = QtCore.QCoreApplication.translate
        cam_Dialog.setWindowTitle(_translate("cam_Dialog", "Dialog"))
        self.record_button.setText(_translate("cam_Dialog", "录入"))
        self.label.setText(_translate("cam_Dialog", "用户名："))
        self.label_2.setText(_translate("cam_Dialog", "ID："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("cam_Dialog", "用户录入"))
        self.verify_button.setText(_translate("cam_Dialog", "验证"))
        self.label_3.setText(_translate("cam_Dialog", "用户名："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("cam_Dialog", "用户验证"))

