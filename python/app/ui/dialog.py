# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(426, 353)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.context = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.context.sizePolicy().hasHeightForWidth())
        self.context.setSizePolicy(sizePolicy)
        self.context.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.context.setObjectName("context")
        self.verticalLayout.addWidget(self.context)
        self.filenameLabel = QtGui.QLabel(Dialog)
        self.filenameLabel.setObjectName("filenameLabel")
        self.verticalLayout.addWidget(self.filenameLabel)
        self.versionName = QtGui.QLabel(Dialog)
        self.versionName.setObjectName("versionName")
        self.verticalLayout.addWidget(self.versionName)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.viewportCombo = QtGui.QComboBox(Dialog)
        self.viewportCombo.setMaxVisibleItems(4)
        self.viewportCombo.setMaxCount(4)
        self.viewportCombo.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.viewportCombo.setObjectName("viewportCombo")
        self.viewportCombo.addItem("")
        self.viewportCombo.addItem("")
        self.viewportCombo.addItem("")
        self.viewportCombo.addItem("")
        self.horizontalLayout_2.addWidget(self.viewportCombo)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.versionText = QtGui.QPlainTextEdit(Dialog)
        self.versionText.setObjectName("versionText")
        self.verticalLayout.addWidget(self.versionText)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.startButton = QtGui.QPushButton(Dialog)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.viewportCombo.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.context.setText(QtGui.QApplication.translate("Dialog", "Your Current Context: ", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameLabel.setText(QtGui.QApplication.translate("Dialog", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.versionName.setText(QtGui.QApplication.translate("Dialog", "Version Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Viewport:", None, QtGui.QApplication.UnicodeUTF8))
        self.viewportCombo.setItemText(0, QtGui.QApplication.translate("Dialog", "A", None, QtGui.QApplication.UnicodeUTF8))
        self.viewportCombo.setItemText(1, QtGui.QApplication.translate("Dialog", "B", None, QtGui.QApplication.UnicodeUTF8))
        self.viewportCombo.setItemText(2, QtGui.QApplication.translate("Dialog", "C", None, QtGui.QApplication.UnicodeUTF8))
        self.viewportCombo.setItemText(3, QtGui.QApplication.translate("Dialog", "D", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Add any notes about your capture here.", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("Dialog", "Start Capture", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
