import sys

from PyQt5.QtWidgets import QMessageBox, QApplication


class SuccessMessage(QMessageBox):
    error_msg = ''

    def __init__(self, message):
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.move(240, 300)
        self.resize(250,180)
        self.setText(message)
        self.setWindowTitle("Success")
        self.setStandardButtons(QMessageBox.Ok)


def show_message_box(message):
    # app = QApplication(sys.argv)
    P = SuccessMessage(message)
    P.show()
    # sys.exit(app.exec_())


# show_message_box('You have Successfully added new Contact')