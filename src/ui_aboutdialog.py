# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../forms/aboutdialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(508, 257)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/applicationIcon128"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        AboutDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.labelLogo = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLogo.sizePolicy().hasHeightForWidth())
        self.labelLogo.setSizePolicy(sizePolicy)
        self.labelLogo.setText("")
        self.labelLogo.setPixmap(QtGui.QPixmap(":/icons/applicationIcon96"))
        self.labelLogo.setScaledContents(False)
        self.labelLogo.setObjectName("labelLogo")
        self.gridLayout.addWidget(self.labelLogo, 0, 0, 3, 1)
        self.labelName = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelName.sizePolicy().hasHeightForWidth())
        self.labelName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.labelName.setFont(font)
        self.labelName.setObjectName("labelName")
        self.gridLayout.addWidget(self.labelName, 0, 1, 1, 1)
        self.labelVersion = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelVersion.sizePolicy().hasHeightForWidth())
        self.labelVersion.setSizePolicy(sizePolicy)
        self.labelVersion.setObjectName("labelVersion")
        self.gridLayout.addWidget(self.labelVersion, 1, 1, 1, 1)
        self.labelKmelDbVersion = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelKmelDbVersion.sizePolicy().hasHeightForWidth())
        self.labelKmelDbVersion.setSizePolicy(sizePolicy)
        self.labelKmelDbVersion.setObjectName("labelKmelDbVersion")
        self.gridLayout.addWidget(self.labelKmelDbVersion, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.labelInfo = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfo.sizePolicy().hasHeightForWidth())
        self.labelInfo.setSizePolicy(sizePolicy)
        self.labelInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelInfo.setWordWrap(True)
        self.labelInfo.setOpenExternalLinks(True)
        self.labelInfo.setObjectName("labelInfo")
        self.verticalLayout.addWidget(self.labelInfo)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About Kenwood Database Generator"))
        self.labelName.setText(_translate("AboutDialog", "Kenwood Database Generator"))
        self.labelVersion.setText(_translate("AboutDialog", "Version: "))
        self.labelKmelDbVersion.setText(_translate("AboutDialog", "KMEL DB CLI version: 0.2.3"))
        self.labelInfo.setText(_translate("AboutDialog", "<html><head/><body><p>This application is basically a GUI for the kmel_db utility (<a href=\"https://github.com/chrrrisw/kmel_db\"><span style=\" text-decoration: underline; color:#2980b9;\">https://github.com/chrrrisw/kmel_db</span></a>). Its purpose is to generate a Kenwood DAP database on a selected USB drive for using that drive with Kenwood car audio. The drive must be FAT32 formatted.</p><p>Kenwood Database Generator is distributed under the terms of <a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\"><span style=\" text-decoration: underline; color:#2980b9;\">GNU General Public License v3.0</span></a>. </p></body></html>"))


import appresources_rc
