from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QLabel, QPushButton, QDialog,
                             QComboBox,
                             QFileDialog, QMessageBox, QListWidget, QGridLayout, QWidget, QLineEdit)
from file_read_write import add_new_contact_to_file
from NotificationBox import SuccessMessage
from constants import *


class AddNewContact(QDialog):
    error_msg = ''
    type = ''

    def __init__(self, parent, title, place_holder, error_msg, type):
        super().__init__(parent)
        self.error_msg = error_msg
        self.type = type

        self.setWindowTitle(title)

        self.top_lable = self.add_label(place_holder, 200, 50, 15, -10, 10)

        self.resize(300, 170)
        self.textbox = QLineEdit(self)
        self.textbox.move(15, 30)
        self.textbox.resize(270, 30)

        self.submit_btn = self.add_button('Submit', 270, 25, 15, 70, 10, self.on_click_submit_btn)
        self.submit_btn_ad_new = self.add_button('Submit and Add New', 270, 25, 15, 100, 10, self.on_click_submit_add_new_btn)
        self.send_button = self.add_button('Close', 270, 25, 15, 130, 10, self.close)

    def add_button(self, text, size_x, size_y, pos_x, pos_y, font_size, function):
        button = QPushButton(text, self)
        button.resize(size_x, size_y)
        button.move(pos_x, pos_y)
        button.setFont(QFont('Times', font_size))
        button.clicked.connect(function)
        return button

    def add_label(self, text, size_x, size_y, pos_x, pos_y, font_size):
        label = QLabel(text, self)
        label.resize(size_x, size_y)
        label.move(pos_x, pos_y)
        label.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold, pointSize=font_size))
        return label

    def on_click_submit_btn(self):
        index = 'contact'
        success_msg = CONTACT_ADDED_MSG
        if self.type == 'group':
            index = 'group'
            success_msg = GROUP_ADDED_MSG
        msg = self.textbox.text()
        if not msg:
            self.showdialog(self.error_msg)
            return
        else:
            status = add_new_contact_to_file(index=index, contact=msg)
            if status:
                self.success_msg = SuccessMessage(success_msg)
                self.success_msg.show()
                self.close()

    def on_click_submit_add_new_btn(self):
        index = 'contact'
        success_msg = CONTACT_ADDED_MSG
        if self.type == 'group':
            index = 'group'
            success_msg = GROUP_ADDED_MSG
        msg = self.textbox.text()
        if not msg:
            self.showdialog(self.error_msg)
            return
        else:
            status = add_new_contact_to_file(index=index, contact=msg)
            if status:
                self.success_msg = SuccessMessage(success_msg)
                self.success_msg.show()
                self.textbox.clear()

    def on_click_close_btn(self):
        self.close()

    def showdialog(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.move(240, 300)
        msg.setText(message)
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.msgbtn)

        retval = msg.exec_()

    def msgbtn(self):
        pass


