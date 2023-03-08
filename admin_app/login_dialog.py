from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests


BASE_URL = "http://127.0.0.1:8001"


class LoginDialog(QtWidgets.QDialog):
    global USERNAME, PASSWORD
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.resize(250, 150)

        layout = QtWidgets.QVBoxLayout(self)

        self.username_label = QtWidgets.QLabel("Username:", self)
        self.username_edit = QtWidgets.QLineEdit(self)

        self.password_label = QtWidgets.QLabel("Password:", self)
        self.password_edit = QtWidgets.QLineEdit(self)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_button = QtWidgets.QPushButton("Login", self)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.accept)

    

    def get_credentials(self):
        return self.username, self.password

    def accept(self):
        self.username = self.get_username()
        self.password = self.get_password()

        self.session = requests.Session()
        url = f"{BASE_URL}/api/users"
        headers = {
        'X-AUTH-USER': self.username,
        'X-AUTH-TOKEN': self.password
        }
        response = self.session.get(url, headers=headers)
    
        if response.status_code == 200:
            self.done(1)

        elif response.status_code == 403:
            QMessageBox.warning(self, "Login Failed", "Invalid Login Credentials")
        else:
            QMessageBox.warning(self, "Login Failed", f"Error While Trying To Login. Status Code was {response.status_code}")

    def get_username(self):
        return self.username_edit.text()

    def get_password(self):
        return self.password_edit.text()
