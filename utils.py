from PyQt5.QtWidgets import QFileDialog


def import_file():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName("QFileDialog.getOpenFileName()", "",
                                              "Image Files (*.doc *.pdf)", options=options)
    if fileName:
        attach_file_path = fileName
    return fileName
