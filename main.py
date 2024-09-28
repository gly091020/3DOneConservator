import os
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.abspath("platforms/")
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5 import QtCore, QtWidgets, QtGui
import ui
import function

old_path = os.getcwd()


def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


cd = source_path('')
os.chdir(cd)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ui.Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.is_start = False
    ui.lineEdit_2.setFocusPolicy(QtCore.Qt.NoFocus)
    ui.pushButton_2.setEnabled(False)
    ui.pushButton_3.setEnabled(False)
    ui.lineEdit.setText(function.path)
    try:
        function.clear_temp()
    except PermissionError as e:
        print(e.args)
        pai_chu = function.get_all_file()
    except FileNotFoundError:
        os.makedirs(function.path)
        pai_chu = []
    else:
        pai_chu = []
    function.pai_chu = pai_chu
    print(function.pai_chu)

    def update_file():
        if ui.is_start:
            if ui.lineEdit_2.text() == "未找到":
                f = function.get_is_have_file()
                if f:
                    ui.lineEdit_2.setText(f)
                    ui.pushButton_3.setEnabled(True)
                    mb = QMessageBox(QMessageBox.Icon(1), '提示', '捕获到文件！',
                                     QMessageBox.Yes, ui.centralwidget)
                    mb.button(QMessageBox.Yes).setText("好")
                    mb.exec_()
                else:
                    ui.lineEdit_2.setText("未找到")
                    ui.pushButton_3.setEnabled(False)

    def start():
        global pai_chu
        if not os.path.isdir(function.path):
            mb = QMessageBox(QMessageBox.Icon(1), '提示', '未找到3D One缓存文件夹',
                             QMessageBox.Yes, ui.centralwidget)
            mb.button(QMessageBox.Yes).setText("好")
            mb.exec_()
            return
        try:
            function.clear_temp()
        except PermissionError as e:
            print(e.args)
            pai_chu = function.get_all_file()
        except FileNotFoundError:
            os.makedirs(function.path)
            pai_chu = []
        else:
            pai_chu = []
        function.pai_chu = pai_chu
        ui.is_start = True
        ui.progressBar.setMaximum(0)
        ui.pushButton.setEnabled(False)
        ui.pushButton_2.setEnabled(True)
        ui.lineEdit_2.setText("未找到")
        ui.pushButton_3.setEnabled(False)

    def change_path():
        if not os.path.isdir(ui.lineEdit.text()):
            ui.lineEdit.setText(function.get_temp_path())
        else:
            function.path = ui.lineEdit.text()

    def stop():
        ui.progressBar.setMaximum(1)
        ui.is_start = False
        ui.pushButton.setEnabled(True)
        ui.pushButton_2.setEnabled(False)
        ui.lineEdit_2.setText("未找到")
        ui.pushButton_3.setEnabled(False)

    def dao_chu():
        global pai_chu
        file_name_choose, filetype = QFileDialog.getSaveFileName(ui.centralwidget, "文件保存", "C:/", "3D One 文件 (*.Z1)")
        if file_name_choose:
            with open(file_name_choose, "wb+") as file, open(ui.lineEdit_2.text(), "rb") as file1:
                file.write(file1.read())
            pai_chu.append(os.path.split(ui.lineEdit_2.text())[1])
            function.pai_chu = pai_chu
            ui.lineEdit_2.setText("未找到")
            ui.pushButton_3.setEnabled(False)
            mb = QMessageBox(QMessageBox.Icon(1), '提示', '保存成功！',
                             QMessageBox.Yes, ui.centralwidget)
            mb.button(QMessageBox.Yes).setText("好")
            mb.exec_()

    ui.pushButton.clicked.connect(start)
    ui.pushButton_3.clicked.connect(dao_chu)
    ui.pushButton_2.clicked.connect(stop)
    ui.lineEdit.editingFinished.connect(change_path)
    timer = QtCore.QTimer()
    timer.timeout.connect(update_file)
    timer.start(500)
    MainWindow.setWindowIcon(QtGui.QIcon("3DOne.ico"))
    MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    os.chdir(old_path)

    MainWindow.show()
    sys.exit(app.exec_())
