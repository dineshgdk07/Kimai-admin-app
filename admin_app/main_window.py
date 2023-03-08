import sys
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from select_user_dialog import SelectUserDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kimai Admin App")
        self.resize(400, 300)

        layout = QtWidgets.QVBoxLayout()

        self.user_list = QtWidgets.QListWidget()
        layout.addWidget(self.user_list)

        self.select_user_button = QtWidgets.QPushButton("Select User")
        layout.addWidget(self.select_user_button)

        self.generate_installer_button = QtWidgets.QPushButton("Generate Installer")
        layout.addWidget(self.generate_installer_button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.select_user_button.clicked.connect(self.show_select_user_dialog)
        self.generate_installer_button.clicked.connect(self.generate_installer)

        self.load_user_list()

    def load_user_list(self):
        with open('user_list.txt', 'r') as f:
            users = f.read().splitlines()
            self.user_list.addItems(users)

    def show_select_user_dialog(self):
        dialog = SelectUserDialog(self)
        if dialog.exec_():
            selected_user = dialog.get_selected_user()
            self.user_list.setCurrentRow(self.user_list.findItems(selected_user, QtCore.Qt.MatchExactly)[0].row())

    def generate_installer(self):
        selected_user = self.user_list.currentItem().text()
        installer_name = f"{selected_user}_service_installer.exe"
        command = f"pyinstaller --onefile --name={installer_name} user_service.py"
        subprocess.run(command)

        QtWidgets.QMessageBox.information(self, "Installer Generated", f"Installer {installer_name} has been generated.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
