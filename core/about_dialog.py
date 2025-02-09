import logging
import webbrowser

import pywinstyles
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = parent

        self.load_ui()
        self.setup_connect()
        self.setup_content()

    def setup_content(self):
        self.BodyLabel_2.setText(self.window.version)

    def setup_connect(self):
        self.PrimaryPushButton.clicked.connect(self.close)
        self.PushButton.clicked.connect(self.go_to_github)

    def go_to_github(self):
        webbrowser.open("https://github.com/deeffest/Youtube-Music-Desktop-Player")

    def load_ui(self):
        loadUi(f'{self.window.current_dir}/core/ui/about_dialog.ui', self)
        try:
            pywinstyles.apply_style(self, "dark")
        except Exception as e:
            logging.error("Failed to apply dark style: " + str(e))

        self.setWindowTitle("About")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/about.png"))

        self.setFixedSize(self.size())

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.window.show()
        event.accept()