import sys
from PyQt5.QtWidgets import QApplication
from admin_app.admin_app import AdminApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_app = AdminApp()
    admin_app.show()
    sys.exit(app.exec_())