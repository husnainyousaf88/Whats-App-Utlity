import sys
import time

from NotificationBox import SuccessMessage
from constants import *
from ListView import ContactBox
from file_read_write import *

from code import WhatsApp
from AddNewContact import AddNewContact

from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QLabel, QPushButton, QDialog, QPlainTextEdit,
                             QComboBox,
                             QFileDialog, QMessageBox)

P = None


class CalendarDialog(QDialog):
    send_file = False
    send_image = False
    selected_contact_group = 'Contacts'
    attach_file_path = ''
    attach_image_path = ''
    start_contact_index = 0
    end_contact_index = 0
    selected_list = []

    def __init__(self, parent, file_at_btn, img_at_btn):
        super().__init__(parent)
        self.send_file = file_at_btn
        self.send_image = img_at_btn
        self.setWindowTitle('Message Box')

        self.selected_list = read_contacts_data()['Contacts']
        self.end_contact_index = len(self.selected_list)-1

        self.top_lable = self.add_label('Type Message here!', 200, 50, 15, -10, 10)
        self.top_lable = self.add_label('Select Receivers', 200, 50, 15, 120, 10)

        self.resize(300, 340)
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(15, 30)
        self.textbox.resize(270, 100)
        self.textbox.setDisabled(file_at_btn)

        self.combo = QComboBox(self)
        self.combo.resize(270, 25)
        self.combo.move(15, 160)
        self.combo.addItem("Contacts")
        self.combo.addItem("Groups")
        self.combo.addItem("Bulk Contacts")
        self.combo.activated[str].connect(self.onChanged)

        # self.top_lable = self.add_label('Pick Start Contact', 130, 50, 15, 165, 10)
        # self.top_lable = self.add_label('Pick End Contact', 130, 50, 165, 165, 10)
        self.start_contact = QComboBox(self)
        self.start_contact.resize(120, 25)
        self.start_contact.move(15, 200)

        self.add_item_to_combo_box(self.start_contact, self.selected_list)
        self.start_contact.activated[str].connect(self.on_change_start)

        self.end_contact = QComboBox(self)
        self.end_contact.resize(120, 25)
        self.end_contact.move(165, 200)
        self.add_item_to_combo_box_reverse(self.end_contact, self.selected_list)
        self.end_contact.activated[str].connect(self.on_change_end)

        self.attach_image_button = self.add_button('Attach Image', 270, 25, 15, 230, 10, self.on_click_attach_image)
        self.attach_file_button = self.add_button('Attach File', 270, 25, 15, 260, 10, self.on_click_attach_file)
        self.send_button = self.add_button('Send', 270, 25, 15, 290, 10, self.on_click_send_button)

        self.attach_image_button.setDisabled(not img_at_btn)
        self.attach_file_button.setDisabled(not file_at_btn)

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

    def onChanged(self, text):
        self.selected_contact_group = text
        self.selected_list.clear()
        self.selected_list = read_contacts_data()[self.selected_contact_group]
        self.start_contact.clear()
        self.end_contact.clear()
        self.add_item_to_combo_box(self.start_contact, self.selected_list)
        self.add_item_to_combo_box_reverse(self.end_contact, self.selected_list)
        self.end_contact_index = len(self.selected_list)-1


    def on_click_attach_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # foo_dir = QFileDialog.getExistingDirectory(self, 'Documents')

        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Image Files (*.doc *.pdf)", options=options)
        if fileName:
            self.attach_file_path = fileName
            

    def on_click_attach_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Image Files (*.png *.jpg *.jpeg *.mp4)", options=options)
        if fileName:
            self.attach_image_path = fileName

    def on_click_send_button(self):
        # msg = self.textbox.toPlainText().rstrip("\n")
        msg = self.textbox.toPlainText()
        empty_sring = '                                                                 '

        # msg = self.textbox.toPlainText().replace("\n", empty_sring)
        print(msg)
        if not msg and not self.send_file:
            self.showdialog(EMPTY_MSG)
            return
        elif self.send_file and not self.attach_file_path:
            self.showdialog(EMPTY_FILE_MSG)
        elif self.send_image and not self.attach_image_path:
            self.showdialog(EMPTY_IMF_MSG)
        else:
            global P
            self.close()
            status = P.send_message_to_list(val=self.selected_contact_group, msg=msg, image_path=self.attach_image_path,
                file_path=self.attach_file_path, start=self.start_contact_index, end= self.end_contact_index)
            if status:
                self.showdialog("All messages has been sent successfully!")

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

    def add_item_to_combo_box(self, box, itemslist):
        for index, item in enumerate(itemslist):
            box.addItem(str(index + 1) + ". " + item)
            box.setFont(QFont('Times', 10))

    def add_item_to_combo_box_reverse(self, box, itemlist):
        length = len(itemlist)
        for index, item in enumerate(reversed(itemlist)):
            box.addItem(str(length - index) + ". " + item)
            box.setFont(QFont('Times', 10))

    def on_change_start(self, text):
        self.start_contact_index = int(re.search(r'\d+', text)[0]) - 1
        print(self.start_contact_index)

    def on_change_end(self, text):
        self.end_contact_index = int(re.search(r'\d+', text)[0]) - 1
        print(self.end_contact_index)



class MenuBarDemo(QMainWindow):
    all_contacts = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Whats App Utility')
        self.setFixedWidth(720)
        self.setFixedHeight(480)

        self.menuBar = self.menuBar()
        self.top_lable = self.add_label('Whats App Utility', 500, 100, 240, 25, 20)

        self.scan_qr_lable = self.add_label('Scan QR Code and Press OKAY', 500, 100, 240, 25, 15)
        self.message_type_label = self.add_label('Select Message Type', 500, 100, 280, 25, 15)

        self.launch_whatsApp_button = self.add_button('Launch Whats App', 250, 80, 240, 200, 15,
                                                      self.on_click_launch_whats_app)
        self.ok_button = self.add_button('Okay', 250, 80, 240, 200, 15, self.on_click_ok_button)
        self.send_message_button = self.add_button('Send Text Message', 150, 40, 280, 150, 8,
                                                   self.on_click_send_message)
        self.send_message_with_image_button = self.add_button('Send Message With Image', 150, 40, 280, 220, 7,
                                                              self.on_click_send_message_with_image)
        self.send_file_button = self.add_button('Send Files', 150, 40, 280, 290, 9,
                                                self.on_click_send_message_with_file)

        self.start_app()

        self.show()

        # menu items...
        fileMenu = self.menuBar.addMenu('File')
        exit_action = QAction('Exit App', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(lambda: QApplication.quit())
        fileMenu.addAction(exit_action)

        view_menu = self.menuBar.addMenu('View')
        contact_menu_action = view_menu.addAction('Contact Names')
        group_menu_action = view_menu.addAction('Group Names')
        bulk_contacts_action = view_menu.addAction("Bulk Contact Names")
        # button press calls

        contact_menu_action.triggered.connect(self.on_click_view_contacts)
        group_menu_action.triggered.connect(self.on_click_View_groups)
        bulk_contacts_action.triggered.connect(self.on_click_View_bulk_contacts)

        add_menu = self.menuBar.addMenu('Add')
        contact_menu_action_add = add_menu.addAction('New Contact')
        group_menu_action_add = add_menu.addAction('New Group')

        contact_menu_action_add.triggered.connect(self.on_click_add_contact)
        group_menu_action_add.triggered.connect(self.on_click_add_group)

        import_menu = self.menuBar.addMenu('import')
        import_contact = import_menu.addAction('Import Contacts From CSV')
        import_bulk_contacts = import_menu.addAction('Import Bulk Contacts From CSV')

        import_contact.triggered.connect(self.on_click_import_contacts_btn)
        import_bulk_contacts.triggered.connect(self.on_click_import_bulkt_conctact_btn)

        export_menu = self.menuBar.addMenu('Export')
        export_file = export_menu.addAction('Generate Google Contacts CSV From Numbers')
        export_file.triggered.connect(self.export_csv_file)

        # end of menu

    def on_click_view_contacts(self):
        self.send_message_dialgo = ContactBox(self, read_contacts_data()['Contacts'], "Contacts")
        self.send_message_dialgo.show()

    def on_click_View_bulk_contacts(self):
        self.send_message_dialgo = ContactBox(self, read_contacts_data()['Bulk Contacts'], "Bulk Contacts")
        self.send_message_dialgo.show()

    def on_click_View_groups(self):
        self.send_message_dialgo = ContactBox(self, read_contacts_data()['Groups'], "Whata App Groups")
        self.send_message_dialgo.show()

    def on_click_add_contact(self):
        self.send_message_dialgo = AddNewContact(self, NEW_CONTACT, CONTACT_MSG, EMPTY_CONTACT_MSG, 'contact')
        self.send_message_dialgo.show()

    def on_click_add_group(self):
        self.send_message_dialgo = AddNewContact(self, NEW_GROUP, GROUP_MSG, EMPTY_GROUP_MSG, 'group')
        self.send_message_dialgo.show()

    def on_click_launch_whats_app(self):
        self.launch_whatsApp_button.setHidden(True)
        self.ok_button.setHidden(False)
        self.scan_qr_lable.setHidden(False)
        self.top_lable.setHidden(True)
        global P
        P = WhatsApp()

    def on_click_ok_button(self):
        self.scan_qr_lable.setHidden(True)
        self.send_file_button.setHidden(False)
        self.send_message_with_image_button.setHidden(False)
        self.send_message_button.setHidden(False)
        self.ok_button.setHidden(True)
        self.message_type_label.setHidden(False)

    def on_click_send_message(self):
        self.send_message_dialgo = CalendarDialog(self, file_at_btn=False, img_at_btn=False)
        self.send_message_dialgo.show()

    def on_click_send_message_with_image(self):
        self.send_message_dialgo = CalendarDialog(self, file_at_btn=False, img_at_btn=True)
        self.send_message_dialgo.show()

    def on_click_send_message_with_file(self):
        self.send_message_dialgo = CalendarDialog(self, file_at_btn=True, img_at_btn=False)
        self.send_message_dialgo.show()

    def on_click_import_contacts_btn(self):
        imported_file = self.import_csv()
        data = write_contact_names_to_file(imported_file, CONTACT_FILE_PATH)
        popup_msg = str(data[0]) + "New Contacts Added"
        if not data[1]:
            popup_msg = 'Invalid or Data'
        print(popup_msg)
        self.show_message_box(popup_msg)

    def on_click_import_bulkt_conctact_btn(self):
        imported_file = self.import_csv()
        data = write_contact_names_to_file(imported_file, BULK_CONTACT_FILE_PATH)
        popup_msg = str(data[0])+"New Contacts Added"
        if not data[1]:
            popup_msg = 'Invalid or Data'
        self.show_message_box(popup_msg)

    def export_csv_file(self):
        imported_file = self.import_csv()
        msg = generate_google_contacts_from_numbers(imported_file, 'export_file.csv')
        self.show_message_box("CSV File Generated for "+str(msg)+" Numbers")

    def show_message_box(self, message):
        self.success_msg = SuccessMessage(message)
        self.success_msg.show()

    def import_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Image Files (*.csv)", options=options)
        if fileName:
            self.attach_file_path = fileName
            return fileName

    def start_app(self):
        self.scan_qr_lable.setHidden(True)
        self.message_type_label.setHidden(True)
        self.send_file_button.setHidden(True)
        self.send_message_with_image_button.setHidden(True)
        self.send_message_button.setHidden(True)
        self.ok_button.setHidden(True)

    def add_label(self, text, size_x, size_y, pos_x, pos_y, font_size):
        label = QLabel(text, self)
        label.resize(size_x, size_y)
        label.move(pos_x, pos_y)
        label.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold, pointSize=font_size))
        return label

    def add_button(self, text, size_x, size_y, pos_x, pos_y, font_size, function):
        button = QPushButton(text, self)
        button.resize(size_x, size_y)
        button.move(pos_x, pos_y)
        button.setFont(QFont('Times', font_size))
        button.clicked.connect(function)
        return button


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = MenuBarDemo()
    demo.show()

    sys.exit(app.exec_())
