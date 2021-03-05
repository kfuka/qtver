from PyQt5.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton, QTextEdit,QAction,QFileDialog,QApplication, QVBoxLayout, QWidget, QCheckBox, QLabel, QGridLayout)
from PyQt5.QtGui import QIcon
import sys
import glob
import pydicom
 
wave_colors = ['magenta', 'blue', 'red', 'green', 'cyan', 'yellow', 'black']

class openDirectory(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.initUI()
        self.show()
 
    def initUI(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.folder = folder

    def get(self):
        self.close()
        return self.folder


class openDicoms(QWidget):
    def __init__(self, folder_dict):
        super().__init__()
        self.folder_dict = folder_dict
        self.setStyleSheet("background-color: black;")
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.initUI()
        

    def initUI(self):
        positions = [i for i in range(len(self.folder_dict))]
        for n, a_file in enumerate(self.folder_dict):
            checkBox = QCheckBox(str(
                a_file[1][0][:2] + ":" + a_file[1][0][2:4] + ":" + a_file[1][0][4:6]))
            label = QLabel(str(a_file[0]).split("/")[-1])
            vorh = QLabel(str(a_file[1][2]))
            checkBox.setStyleSheet("QCheckBox{ color : " + wave_colors[int(n/2.0)] + "; }")
            label.setStyleSheet("QLabel{ color : " + wave_colors[int(n/2.0)] + "; }")
            vorh.setStyleSheet("QLabel{ color : " + wave_colors[int(n/2.0)] + "; }")
            self.layout.addWidget(checkBox, n, 0)
            self.layout.addWidget(vorh, n, 1)
            self.layout.addWidget(label, n, 2)
        openbtn = QPushButton("Open")
        openbtn.setStyleSheet("color: white")
        openbtn.setStyleSheet("background-color: gray")
        self.layout.addWidget(openbtn, n+1, 0)
        openbtn.clicked.connect(self.get)


    def get(self):
        print("good")
        self.close()

 

 
def get_wave_dicoms(folder_name):
    """
    get dicom with wave data
    :param folder_name: folder path
    :return: dictionary of dicom file path and acquisition time sorted with the time
    """
    dicom_list = glob.glob(folder_name + "/*.dcm")
    time_and_dicom = {}
    for a_dicom in dicom_list:
        dicom_data = pydicom.dcmread(a_dicom)
        if len(dicom_data[0x5400, 0x0100][0][0x5400, 0x1010].value) > 10:
            # print(dicom_data[0x0008, 0x0018].value)
            if dicom_data[0x0008, 0x1010].value == "H-SIM1":
                direction = "H"
            else:
                direction = "V"
            time_and_dicom[a_dicom] = [dicom_data.AcquisitionTime, dicom_data[0x0008, 0x0018].value, direction]

    sorted_t_d = sorted(time_and_dicom.items(), key=lambda x: x[1], reverse=True)
    return sorted_t_d

 
if __name__ == '__main__':
    print("goo")
