from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi

BASE_URL = "http://127.0.0.1:8001"


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox
import requests


# class SelectUserDialog(QDialog):
#     def __init__(self, parent, username, password):
#         super().__init__(parent)

#         self.user_list = self.get_user_list(username, password)

#         self.layout = QVBoxLayout()
#         self.username = username
#         self.password = password

#         # Add label
#         self.label = QLabel()
#         self.label.setText("Select User:")
#         self.layout.addWidget(self.label)

#         # Add combo box
#         self.user_combo = QComboBox()
#         for user in self.user_list:
#             self.user_combo.addItem(str(user['username']), str(user['id']))
#         self.layout.addWidget(self.user_combo)

#         # Add buttons
#         self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#         self.layout.addWidget(self.buttons)

#         self.buttons.accepted.connect(self.accept)
#         self.buttons.rejected.connect(self.reject)

#         self.setLayout(self.layout)

#     def get_user_list(self, username, password):
#         self.session = requests.Session()
#         url = f"{BASE_URL}/api/users"
#         headers = {
#         'X-AUTH-USER': username,
#         'X-AUTH-TOKEN': password
#         }
#         response = self.session.get(url, headers=headers)
    
#         if response.status_code == 200:
#             users = [f"{i['id']} - {i['username']}" for i in response.json()]
#             return users
#         else:
#             return []

#     def get_selected_user_id(self):
#         return self.user_combo.currentData()



class SelectUserDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, username='', password=''):
        super().__init__(parent)
        self.setWindowTitle("Select User")
        self.resize(250, 150)

        layout = QtWidgets.QVBoxLayout(self)

        self.username = username
        self.password = password

        self.user_list = QtWidgets.QListWidget(self)
        layout.addWidget(self.user_list)

        self.select_button = QtWidgets.QPushButton("Select", self)
        layout.addWidget(self.select_button)

        self.select_button.clicked.connect(self.accept)

        self.load_user_list()


    def load_user_list(self):
    
        self.session = requests.Session()
        url = f"{BASE_URL}/api/users"
        headers = {
        'X-AUTH-USER': self.username,
        'X-AUTH-TOKEN': self.password
        }
        response = self.session.get(url, headers=headers)
    
        if response.status_code == 200:
            users = [f"{i['id']} - {i['username']}" for i in response.json()]
            self.user_list.addItems(users)
            
        elif response.status_code == 403:
            print(self.username, self.password)
            QMessageBox.warning(self, "Login Failed", "Invalid Login Credentials")
        else:
            QMessageBox.warning(self, "Login Failed", f"Error While Trying To Login. Status Code was {response.status_code}")

    def get_selected_user(self):
        return self.user_list.currentItem().text()
