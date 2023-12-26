import sys
import sqlite3
import datetime
import re

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox

dbpath = 'data.db'

class DatabaseController:
    def __init__(self):
        self.path = dbpath
        self.connection = sqlite3.connect(self.path)
        
    def deleteRow(self, iid: int):
        with self.connection as con:
            return con.cursor().execute(f'DELETE FROM emplInf WHERE id = {iid}')
        
    def addEmplInfo(self, emplInfo: tuple):
            with self.connection as con:
                return con.cursor().execute('INSERT INTO emplInf VALUES (?,?,?,?,?,?,?,?,?,?)', emplInfo)
            
    def getEmplInfo(self, iid: int):
        with self.connection as con:
            return con.cursor().execute(f'SELECT * FROM emplInf WHERE id = {iid}').fetchall()[0]
        
    def updateEmplPos(self, iid: int):
        with self.connection as con:
            return con.cursor().execute(f'UPDATE emplInf SET is_on_territory = NOT is_on_territory WHERE id = {iid};')
        
    def getEmplPos(self, iid: int):
        with self.connection as con:
            return con.cursor().execute(f'SELECT is_on_territory FROM emplInf WHERE id = {iid};').fetchone()[0] == 1
        
    def updateEmplLastVisit(self, iid: int, lastVisitDate: str):
        with self.connection as con:
            return con.cursor().execute(f'UPDATE emplInf SET last_visit_date = "{lastVisitDate}" WHERE id = {iid}')
        
    def checkId(self, iid: int):
        with self.connection as con:
            return int(con.cursor().execute(f'SELECT COUNT(*) FROM emplInf WHERE id = {iid};').fetchone()[0]) == 0
    
class MessageHandler:
    def show_message(self, icon: QMessageBox.Icon, window_title: str, message: str):
        error = QMessageBox()
        error.setWindowTitle(window_title)
        error.setIcon(icon)
        error.setText(message)
        error.setDefaultButton(QMessageBox.StandardButton.Ok)
        error.exec()
        
class Ui_addWindow(MessageHandler, DatabaseController):
    def setupUi(self, addWindow):
        addWindow.setObjectName("addWindow")
        addWindow.resize(380, 250)
        addWindow.setMinimumSize(QtCore.QSize(380, 250))
        addWindow.setMaximumSize(QtCore.QSize(380, 250))
        self.centralwidget = QtWidgets.QWidget(parent=addWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        
        self.idAddLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.idAddLine.setGeometry(QtCore.QRect(130, 15, 121, 60))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(26)
        self.idAddLine.setFont(font)
        self.idAddLine.setText("")
        self.idAddLine.setMaxLength(4)
        self.idAddLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.idAddLine.setObjectName("idAddLine")
        
        
        self.firstNameLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.firstNameLine.setGeometry(QtCore.QRect(10, 90, 121, 25))
        self.firstNameLine.setText("")
        self.firstNameLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.firstNameLine.setObjectName("firstNameLine")
        
        
        self.secondNameLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.secondNameLine.setGeometry(QtCore.QRect(130, 90, 121, 25))
        self.secondNameLine.setText("")
        self.secondNameLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.secondNameLine.setObjectName("secondNameLine")
        

        self.lastNameLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lastNameLine.setGeometry(QtCore.QRect(250, 90, 121, 25))
        self.lastNameLine.setText("")
        self.lastNameLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lastNameLine.setObjectName("lastNameLine")
        

        self.birhdayLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.birhdayLine.setGeometry(QtCore.QRect(10, 121, 121, 25))
        self.birhdayLine.setText("")
        self.birhdayLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.birhdayLine.setObjectName("birhdayLine")
        

        self.jobtitleLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.jobtitleLine.setGeometry(QtCore.QRect(130, 121, 121, 25))
        self.jobtitleLine.setText("")
        self.jobtitleLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.jobtitleLine.setObjectName("jobtitleLine")
        

        self.phoneNumberLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.phoneNumberLine.setGeometry(QtCore.QRect(250, 121, 121, 25))
        self.phoneNumberLine.setText("")
        self.phoneNumberLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.phoneNumberLine.setObjectName("phoneNumberLine")
        

        self.accesEndingLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.accesEndingLine.setEnabled(False)
        self.accesEndingLine.setGeometry(QtCore.QRect(190, 155, 131, 25))
        self.accesEndingLine.setText("")
        self.accesEndingLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.accesEndingLine.setObjectName("accesEndingLine")


        self.tempEmplCB = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.tempEmplCB.setGeometry(QtCore.QRect(50, 155, 131, 25))
        self.tempEmplCB.setObjectName("tempEmplCB")
        self.tempEmplCB.toggled.connect(self.setAccesEndingLine)

        
        self.delEmplBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delEmplBtn.setGeometry(QtCore.QRect(60, 189, 261, 25))
        self.delEmplBtn.setObjectName("delEmplBtn")
        self.delEmplBtn.clicked.connect(self.delEmpl)
        

        self.addEmplBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addEmplBtn.setGeometry(QtCore.QRect(60, 220, 261, 25))
        self.addEmplBtn.setObjectName("addEmplBtn")
        self.addEmplBtn.clicked.connect(self.addEmpl)
        

        addWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(addWindow)
        QtCore.QMetaObject.connectSlotsByName(addWindow)

    def retranslateUi(self, addWindow):
        _translate = QtCore.QCoreApplication.translate
        addWindow.setWindowTitle(_translate("addWindow", "Add employee"))
        self.idAddLine.setPlaceholderText(_translate("addWindow", "ID"))
        self.firstNameLine.setPlaceholderText(_translate("addWindow", "Имя"))
        self.secondNameLine.setPlaceholderText(_translate("addWindow", "Фамилия"))
        self.lastNameLine.setPlaceholderText(_translate("addWindow", "Отчество"))
        self.birhdayLine.setPlaceholderText(_translate("addWindow", "Дата рождения"))
        self.jobtitleLine.setPlaceholderText(_translate("addWindow", "Должность"))
        self.phoneNumberLine.setPlaceholderText(_translate("addWindow", "Номер телефона"))
        self.tempEmplCB.setText(_translate("addWindow", "Временный пропуск"))
        self.accesEndingLine.setPlaceholderText(_translate("addWindow", "Дата отзыва пропуска"))
        self.delEmplBtn.setText(_translate("addWindow", "Удалить сотрудника (задействуется только ID)"))
        self.addEmplBtn.setText(_translate("addWindow", "Добавить сотрудника"))
        self.addEmplBtn.setShortcut(_translate("addWindow", "Return"))
        
    def addEmplInfoIsValid(self):
        if len(self.firstNameLine.text().strip()) == 0 or len(self.firstNameLine.text().strip().split()) != 1:
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Имя введено некоректно.')
            return False
        
        if len(self.secondNameLine.text().strip()) == 0 or len(self.secondNameLine.text().strip().split()) != 1:
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Фамилия введена некоректно.')
            return False    
        
        if len(self.lastNameLine.text().strip()) == 0 or len(self.lastNameLine.text().strip().split()) != 1:
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Отчество введено некоректно.')
            return False     
        
        if re.match(r'(0?[1-9]|[12][0-9]|3[01]).(0?[1-9]|1[012]).((19|20)\d\d)', self.birhdayLine.text().strip()) is None or len(self.birhdayLine.text().strip().split()) > 1:
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Дата рождения введена некоректно. Она должна быть в формате дд/мм/гггг')
            return False
        
        if len(self.jobtitleLine.text().strip()) == 0 or len(self.jobtitleLine.text().strip().split()) > 4:
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Должность введена некоректно.')
            return False
                    
        if re.fullmatch(r'\+7\d{10}', self.phoneNumberLine.text().strip()) is None or len(self.phoneNumberLine.text().strip()) != 12:
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Номер телефона введён некоректно. Он должен быть в формате +7**********')
            return False
        
        if self.tempEmplCB.isChecked():
            if re.match(r'(0?[1-9]|[12][0-9]|3[01]).(0?[1-9]|1[012]).((19|20)\d\d)', self.accesEndingLine.text().strip()) is None or len(self.accesEndingLine.text().strip().split()) > 1:
                self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Дата отзыва пропуска введена некоректно. Она должна быть в формате дд/мм/гггг')
                return False
        
        return True
       
    def setAccesEndingLine(self):
        self.accesEndingLine.setEnabled(self.tempEmplCB.isChecked())
    
    def delEmpl(self):
        if self.idAddLine.text() == '':
            return
        
        inputid = int(self.idAddLine.text())        
        if inputid not in range(1000, 10000):
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'ID должен состоять из 4 цифр.')
            self.idAddLine.clear()
            return
        
        if self.checkId(inputid):
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Сотрудника с таким ID не существует.')
            self.idAddLine.clear()
            return
        
        self.deleteRow(inputid)
        self.show_message(QMessageBox.Icon.NoIcon, ' ', 'Сотрудник удалён из базы данных.')
    
    def addEmpl(self):
        if self.idAddLine.text() == '':
            return
        
        inputid = int(self.idAddLine.text())        
        if inputid not in range(1000, 10000):
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'ID должен состоять из 4 цифр.')
            self.idAddLine.clear()
            return
        
        if not self.checkId(inputid):
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Сотрудник с таким ID уже существует.')
            self.idAddLine.clear()
            return
        
        if self.addEmplInfoIsValid():
            if not self.tempEmplCB.isChecked(): addAccesEndingLine = 'не ожидается' 
            else: addAccesEndingLine = self.accesEndingLine.text()
            
        addId = int(self.idAddLine.text().strip())
        addSN = self.secondNameLine.text().strip()
        addFN = self.firstNameLine.text().strip()
        addLN = self.lastNameLine.text().strip()
        addBL = self.birhdayLine.text().strip()
        addJL =  self.jobtitleLine.text().strip()
        addPN = self.phoneNumberLine.text().strip().replace('+', '')
        addLV = 'Никогда'
        addOT = 0
        
        inputInfo = (addId, addSN, addFN, addLN, addBL, addJL, addPN, addLV, addAccesEndingLine, addOT)
        
        self.addEmplInfo(inputInfo)
        self.show_message(QMessageBox.Icon.NoIcon, ' ', 'Сотрудник добавлен в базу данных.')
        
class Ui_mainWindow(Ui_addWindow):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(260, 190)
        mainWindow.setMinimumSize(QtCore.QSize(260, 190))
        mainWindow.setMaximumSize(QtCore.QSize(260, 190))
        self.centralwidget = QtWidgets.QWidget(parent=mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        

        self.idLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.idLine.setGeometry(QtCore.QRect(70, 15, 121, 60))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(26)
        self.idLine.setFont(font)
        self.idLine.setText("")
        self.idLine.setMaxLength(4)
        self.idLine.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        int_validator = QtGui.QIntValidator(1, 9999)
        self.idLine.setValidator(int_validator)
        self.idLine.setObjectName("idLine")
        

        self.letMeInBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.letMeInBtn.setGeometry(QtCore.QRect(20, 90, 221, 25))
        self.letMeInBtn.setObjectName("letMeInBtn")
        self.letMeInBtn.clicked.connect(self.accessEmpl)
        

        self.informationBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.informationBtn.setGeometry(QtCore.QRect(20, 120, 221, 25))
        self.informationBtn.setObjectName("informationBtn")
        self.informationBtn.clicked.connect(self.showEmplInformation)


        self.addWindowBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addWindowBtn.setGeometry(QtCore.QRect(20, 150, 221, 25))
        self.addWindowBtn.setObjectName("addWindowBtn")
        self.addWindowBtn.clicked.connect(self.showAddWindow)
        

        mainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Acces Control"))
        self.idLine.setPlaceholderText(_translate("mainWindow", "ID"))
        self.letMeInBtn.setText(_translate("mainWindow", "Пропустить сотрудника"))
        self.informationBtn.setText(_translate("mainWindow", "Информация о сотруднике"))
        self.addWindowBtn.setText(_translate("mainWindow", "Добавить сотрудника"))
        
    def unvalid(self):
        if self.idLine.text() == '':
            return True
        
        inputid = int(self.idLine.text())
        if self.checkId(inputid) or inputid not in range(1000, 10000):
            self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Сотрудника с таким ID не существует. ID состоит из 4 цифр.')
            self.idLine.clear()
            return True
        
        return False
    
    def showAddWindow(self):
        self.add = QtWidgets.QMainWindow()
        self.ui = Ui_addWindow()
        self.ui.setupUi(self.add)
        self.add.show()

    def accessEmpl(self):
        if self.unvalid():
            return
       
        inputid = int(self.idLine.text())
        self.updateEmplLastVisit(inputid, datetime.datetime.now().strftime('%d/%m/%Y'))
        self.updateEmplPos(inputid)
        
        if self.getEmplPos(inputid): message = f'Сотрудник с ID {inputid} вошёл на территорию.'
        else: message = f'Сотрудник с ID {inputid} покинул территорию.'
            
        self.show_message(QMessageBox.Icon.NoIcon, ' ', message)
        
    def showEmplInformation(self):
        if self.unvalid():
            return
        
        inputid = int(self.idLine.text())
        outputInfo = self.getEmplInfo(inputid)
        
        if self.getEmplPos(inputid): emplPosStr = 'Сейчас находится на территории'
        else: emplPosStr = 'Сейчас находится вне территории'        
        message = (f'ID: {outputInfo[0]}\n'
                   f'Фамилия: {outputInfo[1]}\n'
                   f'Имя: {outputInfo[2]}\n'
                   f'Отчество: {outputInfo[3]}\n'
                   f'Дата рождения: {outputInfo[4]}\n'
                   f'Должность: {outputInfo[5]}\n'
                   f'Номер телефона: +{outputInfo[6]}\n'
                   f'Последнее посещение: {outputInfo[7]}\n'
                   f'Отзыв пропуска {outputInfo[8]}\n'
                   f'{emplPosStr}\n')

        self.show_message(QMessageBox.Icon.Information, 'Информация о сотруднике', message)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
