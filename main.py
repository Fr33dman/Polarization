import sys
import traceback
from PyQt5 import QtWidgets, QtGui, Qt
import gui
from graphics import Waves, Spiral, Circle, Graph


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    #import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, 'Error', text)
    quit()
sys.excepthook = log_uncaught_exceptions


class Application(QtWidgets.QMainWindow, gui.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.box_lambda.setValue(380)
        self.box_Ex_Ey.setValue(1.00)
        self.box_delta_fi.setValue(0.50)
        self.btn_refresh.clicked.connect(self.refresh)
        self.Ex_Ey = self.box_Ex_Ey.value()
        self.delta_fi = self.box_delta_fi.value()
        self.lamda = self.box_lambda.value()
        self.circle_path = 'circle.gif'
        self.waves_path = 'waves.gif'
        self.polarization_path = 'polarization.gif'
        self.circle = Circle(self.circle_path, 1, 0.5, 380)
        self.polarization = Spiral(self.polarization_path)
        self.waves = Waves(self.waves_path)
        self.start()

    def start(self):
        self.gif_polarization = QtGui.QMovie(self.polarization_path)
        self.polarization_view.setMovie(self.gif_polarization)
        self.gif_polarization.start()
        self.gif_circle = QtGui.QMovie(self.circle_path)
        self.projection_view.setMovie(self.gif_circle)
        self.gif_circle.start()
        self.gif_waves = QtGui.QMovie(self.waves_path)
        self.waves_view.setMovie(self.gif_waves)
        self.gif_waves.start()

    def stop(self):
        self.gif_waves.stop()
        self.gif_circle.stop()
        self.gif_polarization.stop()

    def refresh(self):
        self.stop()
        Ex_Ey = self.box_Ex_Ey.value()
        self.waves.set_Ex_Ey(Ex_Ey)
        self.polarization.set_Ex_Ey(Ex_Ey)
        delta_fi = self.box_delta_fi.value()
        self.waves.set_delta_fi(delta_fi)
        self.polarization.set_delta_fi(delta_fi)
        lamda = self.box_lambda.value()
        self.waves.set_lambda(lamda)
        self.polarization.set_lambda(lamda)
        self.circle = Circle(self.circle_path, Ex_Ey, delta_fi, lamda)
        '''self.circle.refresh()'''
        self.waves.refresh()
        self.polarization.refresh()
        self.start()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
