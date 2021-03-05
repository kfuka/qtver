import sys
from PyQt5 import QtWidgets

from remoa import Ui_MainWindow
from open_file import openDirectory, get_wave_dicoms, openDicoms

"""
.uiファイルをつくったら
pyuic5 remoa.ui -o remoa.py
でpythonファイルにしてしまう
"""

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.sub1 = None
        self.setupUi(self)
        self.attach_tree()
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.openfile)

    def openfile(self):
        getdicomclass = openDirectory()
        dicom_dir = getdicomclass.get()
        folder_dict = get_wave_dicoms(dicom_dir)
        if self.sub1 is None:
            self.sub1 = openDicoms(folder_dict)
        self.sub1.show()


    def attach_tree(self):
        path = "../"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(path)
        self.model.setNameFilters(["*.dcm"])
        self.model.setNameFilterDisables(False)
        view = self.treeView
        view.setModel(self.model)
        view.setRootIndex(self.model.index(path))
        view.setColumnWidth(0,200)
        view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()