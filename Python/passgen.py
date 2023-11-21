import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIntValidator
import secrets
import string
import qdarkstyle

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Password Generator')
        self.setGeometry(300, 300, 400, 200)

        self.label = QLabel('Password Length:', self)
        self.entry = QLineEdit(self)
        self.generate_button = QPushButton('Generate Password', self)
        self.result_label = QLabel('', self)

        # Set validator to accept only integers
        self.entry.setValidator(QIntValidator())

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_label)

        self.generate_button.clicked.connect(self.generate_password)

        self.setLayout(layout)

    def generate_password(self):
        try:
            length = int(self.entry.text())
            if length <= 0:
                raise ValueError("Password length must be a positive integer")
            elif length > 60:
                raise ValueError("Please type an amount under 60 characters")

            password = self.generate_secure_password(length)
            self.result_label.setText(f"Generated Password: {password}")
        except ValueError as e:
            self.show_error(str(e))

    def generate_secure_password(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
