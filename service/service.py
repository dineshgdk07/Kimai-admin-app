import os
import sys
import time
import requests
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QGuiApplication, QScreen
from PyQt5.QtCore import QThread, pyqtSignal, Qt


class KimaiService(QThread):
    data_required = pyqtSignal(bool)
    skip_warning = pyqtSignal(str)

    def __init__(self, user_id, api_url, api_username, api_password, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.api_url = api_url
        self.api_username = api_username
        self.api_password = api_password
        self.data_required_flag = False
        self.skip_warning_reason = None

    def run(self):
        while True:
            if self.data_required_flag:
                self.check_kimai_timesheet()
            time.sleep(900)

    def check_kimai_timesheet(self):
        headers = {'X-AUTH-USER': self.api_username, 'X-AUTH-TOKEN': self.api_password}
        # yesterday = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        yesterday = yesterday.strftime("%Y-%m-%d")
        url = f'{self.api_url}/api/timesheets?user={user_id}&begin={yesterday}T00:00:00&end={yesterday}T23:59:59'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if not data:
                self.data_required.emit(True)
            else:
                self.data_required.emit(False)
        else:
            print('Error:', response.status_code, response.reason)

    def set_data_required_flag(self, flag):
        self.data_required_flag = flag

    def set_skip_warning_reason(self, reason):
        self.skip_warning_reason = reason
        self.skip_warning.emit(reason)


class WarningWindow(QGuiApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = None

    def show_warning(self):
        if self.window is None:
            self.window = WarningDialog()
            self.window.showFullScreen()
        else:
            self.window.show()

    def hide_warning(self):
        if self.window is not None:
            self.window.hide()


class WarningDialog(QGuiApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.screen = QGuiApplication.primaryScreen()
        self.width = self.screen.size().width()
        self.height = self.screen.size().height()
        self.setQuitOnLastWindowClosed(False)

        self.setStyleSheet("background-color: red;")

        self.window = None

        self.show_warning()

    def show_warning(self):
        if self.window is None:
            self.window = WarningMessage()
            self.window.showFullScreen()
        else:
            self.window.show()

    def hide_warning(self):
        if self.window is not None:
            self.window.hide()

    def resizeEvent(self, event):
        self.width = self.screen.size().width()
        self.height = self.screen.size().height()

        self.window.resize(self.width, self.height)


class WarningMessage(QGuiApplication):
    def __init__(self):
        super().__init__(sys.argv)

        self.screen = QGuiApplication.primaryScreen()
        self.width = self.screen.size().width()
        self.height = self.screen.size().height()

        self.setStyleSheet("background-color: red;")

        self.window = None

        self.show_warning()

    def show_warning(self):
        if self.window is None:
            self.window = PyQtWarning(self.width, self.height)
            self.window.show()
        else:
            self.window.show()

    def hide_warning(self):
        if self.window is not None:
            self.window.hide()

    def resizeEvent(self, event):
        self.width = self.screen.size().width()
        self.height = self.screen.size().height()

        self.window.resize(self.width, self.height)


class PyQtWarning(QGuiApplication):
    def __init__(self, width, height):
        super().init(sys.argv)
        self.setStyleSheet("background-color: red;")
        self.setQuitOnLastWindowClosed(False)

        self.setGeometry(0, 0, width, height)

        self.show_warning()

    def show_warning(self):
        message = "Please fill in yesterday's timesheet."
        self.label = self.create_label(message, 40)
        self.label.move(int(self.width() / 2 - self.label.width() / 2),
                        int(self.height() / 2 - self.label.height() / 2))

        self.showFullScreen()

    def create_label(self, message, font_size):
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"font-size: {font_size}px; color: white;")
        label.adjustSize()
        return label


class KimaiApp():
    def __init__(self, user_id, api_url, api_username, api_password):
        self.user_id = user_id
        self.api_url = api_url
        self.api_username = api_username
        self.api_password = api_password

        self.service = KimaiService(self.user_id, self.api_url, self.api_username, self.api_password)
        self.warning = WarningWindow()
        self.service.data_required.connect(self.warning.show_warning)
        self.service.skip_warning.connect(self.warning.hide_warning)

    def start(self):
        self.service.start()

    def stop(self):
        self.service.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_id = 1
    api_url = 'http://127.0.0.1'
    api_username = "admin"
    api_password = 'As12df.,'

    kimai_app = KimaiApp(user_id, api_url, api_username, api_password)
    kimai_app.start()

    sys.exit(app.exec_())

