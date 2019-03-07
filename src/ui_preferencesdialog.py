# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../forms/preferencesdialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.resize(393, 190)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PreferencesDialog.sizePolicy().hasHeightForWidth())
        PreferencesDialog.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/applicationIcon128"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PreferencesDialog.setWindowIcon(icon)
        PreferencesDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(PreferencesDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxSelectFirstDrive = QtWidgets.QCheckBox(PreferencesDialog)
        self.checkBoxSelectFirstDrive.setObjectName("checkBoxSelectFirstDrive")
        self.verticalLayout.addWidget(self.checkBoxSelectFirstDrive)
        self.checkBoxShowToolbar = QtWidgets.QCheckBox(PreferencesDialog)
        self.checkBoxShowToolbar.setObjectName("checkBoxShowToolbar")
        self.verticalLayout.addWidget(self.checkBoxShowToolbar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelLanguage = QtWidgets.QLabel(PreferencesDialog)
        self.labelLanguage.setObjectName("labelLanguage")
        self.horizontalLayout.addWidget(self.labelLanguage)
        self.comboBoxLanguage = QtWidgets.QComboBox(PreferencesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxLanguage.sizePolicy().hasHeightForWidth())
        self.comboBoxLanguage.setSizePolicy(sizePolicy)
        self.comboBoxLanguage.setMinimumSize(QtCore.QSize(280, 0))
        self.comboBoxLanguage.setObjectName("comboBoxLanguage")
        self.horizontalLayout.addWidget(self.comboBoxLanguage)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelRequireRestart = QtWidgets.QLabel(PreferencesDialog)
        self.labelRequireRestart.setObjectName("labelRequireRestart")
        self.verticalLayout.addWidget(self.labelRequireRestart)
        self.buttonBox = QtWidgets.QDialogButtonBox(PreferencesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.labelLanguage.setBuddy(self.comboBoxLanguage)

        self.retranslateUi(PreferencesDialog)
        self.buttonBox.accepted.connect(PreferencesDialog.accept)
        self.buttonBox.rejected.connect(PreferencesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)
        PreferencesDialog.setTabOrder(self.checkBoxSelectFirstDrive, self.checkBoxShowToolbar)
        PreferencesDialog.setTabOrder(self.checkBoxShowToolbar, self.comboBoxLanguage)

    def retranslateUi(self, PreferencesDialog):
        _translate = QtCore.QCoreApplication.translate
        PreferencesDialog.setWindowTitle(_translate("PreferencesDialog", "Preferences"))
        self.checkBoxSelectFirstDrive.setText(_translate("PreferencesDialog", "&Select first available USB drive in the list"))
        self.checkBoxShowToolbar.setText(_translate("PreferencesDialog", "S&how toolbar"))
        self.labelLanguage.setText(_translate("PreferencesDialog", "&Language*"))
        self.labelRequireRestart.setText(_translate("PreferencesDialog", "* - this option requires restart"))


import appresources_rc
