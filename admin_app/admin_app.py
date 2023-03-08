import os
import subprocess
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from .login_dialog import LoginDialog, BASE_URL 
from .select_user_dialog import SelectUserDialog
import requests


class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_file = os.path.join(os.path.dirname(__file__), 'admin_app.ui')
        loadUi(ui_file, self)

        self.login_button.clicked.connect(self.login)
        self.logout_button.clicked.connect(self.logout)
        self.select_user_button.clicked.connect(self.select_user)
        self.generate_service_button.clicked.connect(self.generate_service)

        self.logout_button.setEnabled(False)
        self.select_user_button.setEnabled(False)
        self.generate_service_button.setEnabled(False)


    def login(self):
        login_dialog = LoginDialog()
        result = login_dialog.exec_()
        self.username, self.password = login_dialog.get_credentials()

        if result == QDialog.Accepted:
            self.login_button.setEnabled(False)
            self.logout_button.setEnabled(True)
            self.select_user_button.setEnabled(True)
            self.login_button.setText(f"Welcome {self.username}..!")

    def logout(self):
        self.login_button.setEnabled(True)
        self.logout_button.setEnabled(False)
        self.select_user_button.setEnabled(False)
        self.generate_service_button.setEnabled(False)

    def select_user(self):
        select_user_dialog = SelectUserDialog(self, self.username, self.password)
        result = select_user_dialog.exec_()

        if result == QDialog.Accepted:
            self.generate_service_button.setEnabled(True)
            
            self.selected_user = select_user_dialog.get_selected_user()
            self.employee_id, self.employee_username = self.selected_user.split(" - ")
            print(self.employee_id, self.employee_username)

    def generate_service(self):
        selected_user = self.selected_user

        if not os.path.isdir(selected_user):
            os.mkdir(selected_user)

        subprocess.run(['cp', '-r', 'service', selected_user])

        service_dir = os.path.join(selected_user, 'service')
        os.rename(os.path.join(service_dir, 'service.py'), os.path.join(service_dir, f'{selected_user}_service.py'))

        subprocess.run(['pyinstaller', '--name', f'{selected_user}_service', '--hidden-import', 'win32timezone', '--onefile', f'{selected_user}_service.py'], cwd=service_dir)

        os.rename(os.path.join(service_dir, 'dist', f'{selected_user}_service.exe'), os.path.join(selected_user, f'{selected_user}_service.exe'))
        subprocess.run(['rm', '-rf', 'build', 'dist'], cwd=service_dir)

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setText(f'Service for user {selected_user} successfully generated!')
        message_box.exec_()
