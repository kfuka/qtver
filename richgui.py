import sys
from PyQt5 import QtWidgets
import pydicom
from remoa import Ui_MainWindow
import numpy as np
from open_file import openDirectory, get_wave_dicoms, openDicoms
import pyqtgraph as pg
import wave_analysis

pg.setConfigOptions(imageAxisOrder='row-major')

"""
.uiファイルをつくったら
pyuic5 remoa.ui -o remoa.py
でpythonファイルにしてしまう
"""

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)
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
            self.sub1 = openDicoms(folder_dict, parent=self)
        self.sub1.show()
        
    def get_open_dicoms(self, dicoms):
        # ここで開くべきDicom Filesを返してもらう．
        # dictionalyになっている．
        # [file, [time, UID, beam direction]]
        # 表示するところまでこの関数で行う
        self.open_dicom_list = dicoms
        for a in dicoms:
            if a[1][2] == "V":
                self.dicom_file_1 = a[0]
            elif a[1][2] == "H":
                self.dicom_file_2 = a[0]
            else:
                print(a)
        self.init_graphics()
        

    def init_graphics(self):
        self.array1 = pydicom.dcmread(self.dicom_file_1).pixel_array
        self.graphicsView.setImage(self.array1[0],
                          autoRange=False,
                          autoLevels=True,
                          autoHistogramRange=False,
                          levelMode="mono")
        self.array2 = pydicom.dcmread(self.dicom_file_2).pixel_array
        self.graphicsView_2.setImage(self.array2[0],
                          autoRange=False,
                          autoLevels=True,
                          autoHistogramRange=False,
                          levelMode="mono")
        # self.imv.autoLevels()
        hist = self.graphicsView.getImageItem().getHistogram()
        mid_x = hist[0][np.argmax(hist[1][:len(hist[1])//2])]
        min_x = hist[0][0]
        max_x = (mid_x - min_x) * 3 + mid_x
        self.graphicsView.setLevels(min_x,max_x)
        hist = self.graphicsView_2.getImageItem().getHistogram()
        mid_x = hist[0][np.argmax(hist[1][:len(hist[1])//2])]
        min_x = hist[0][0]
        max_x = (mid_x - min_x) * 3 + mid_x
        self.graphicsView_2.setLevels(min_x,max_x)

        # wave をplotする
        self.wave1, self.wave_time1 = wave_analysis.wave_analysis(pydicom.dcmread(self.dicom_file_1))
        self.wave2, self.wave_time2 = wave_analysis.wave_analysis(pydicom.dcmread(self.dicom_file_2))
        self.plot_wave()

    def plot_wave(self):
        self.graphicsView_3.addLegend()
        self.graphicsView_4.addLegend()
        self.graphicsView_3.plot(self.wave_time1, self.wave1, pen=pg.mkPen(color="r"), antialias=True, name="Resp.", symbolBrush = "r", symbol="o", symbolPen="r", symbolSize=5)
        self.graphicsView_3.setLabel("bottom", text="time (sec.)")
        self.graphicsView_3.setLabel("left", text="Resp. Phase (%)")
        self.graphicsView_4.plot(self.wave_time2, self.wave2, pen=pg.mkPen(color="r"), antialias=True, name="Resp.", symbolBrush = "r", symbol="o", symbolPen="r", symbolSize=5)
        self.graphicsView_4.setLabel("bottom", text="time (sec.)")
        self.graphicsView_4.setLabel("left", text="Resp. Phase (%)")
        
        





    def attach_tree(self):
        path = "../"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(path)
        self.model.setNameFilters(["*.dcm"])
        self.model.setNameFilterDisables(False)



def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()