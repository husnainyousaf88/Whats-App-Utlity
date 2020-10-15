from PyQt5.QtWidgets import QListWidget, QGridLayout, QDialog


class ContactBox(QDialog):

    def __init__(self, parent, contacts, title):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(400, 400)
        layout = QGridLayout()
        self.setLayout(layout)
        self.listwidget = QListWidget()
        index = len(contacts)
        for item in reversed(contacts):
            self.listwidget.insertItem(0, str(index) +".  "+ str(item))
            index -= 1
        layout.addWidget(self.listwidget)
