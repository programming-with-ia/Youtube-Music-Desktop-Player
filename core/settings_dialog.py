import sys
import logging
from typing import TYPE_CHECKING

import pywinstyles
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from qfluentwidgets import MessageBox

from core.settings import AppSettings as DefaultAppSetting


if TYPE_CHECKING:
    from core.main_window import MainWindow


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.load_ui()
        self.setup_content()
        self.set_connect()
        self.configure_tabs()
        self.setup_settings()

        self.PillPushButton_4.setIcon(self.window.icon_folder+"/plugins.png")

    def setup_content(self):
        self.PillPushButton.setChecked(True)
        int_validator = QIntValidator()
        self.LineEdit_2.setValidator(int_validator)
        self.proxy_types = ["HttpProxy", "Socks5Proxy", 
                            "DefaultProxy", "NoProxy"]
        self.ComboBox.addItems(self.proxy_types)
        self.opengl_enviroments = ["Desktop", "Angle",
                                   "Software", "Auto"]
        self.ComboBox_3.addItems(self.opengl_enviroments)

    def setup_settings(self):
        self._foreach_switchButton(
            lambda switchButton, settingKey: switchButton.setChecked(
                getattr(self.window.app_settings, settingKey)
            )
        )

        self.ComboBox.setCurrentIndex(self.proxy_types.index(self.window.app_settings.proxy_type))
        self.toggle_proxy_config()
        if self.window.app_settings.proxy_host_name:
            self.LineEdit.setText(self.window.app_settings.proxy_host_name)
        if self.window.app_settings.proxy_port:
            self.LineEdit_2.setText(str(self.window.app_settings.proxy_port))
        if self.window.app_settings.proxy_login:
            self.LineEdit_3.setText(self.window.app_settings.proxy_login)
        if self.window.app_settings.proxy_password:
            self.PasswordLineEdit.setText(self.window.app_settings.proxy_password)
        self.ComboBox_3.setCurrentIndex(self.opengl_enviroments.index(self.window.app_settings.opengl_enviroment))

        self.check_if_settings_changed()

    def set_connect(self):
        self.PillPushButton.clicked.connect(self.configure_tabs)
        self.PillPushButton_2.clicked.connect(self.configure_tabs)
        self.PillPushButton_3.clicked.connect(self.configure_tabs)
        self.PillPushButton_4.clicked.connect(self.configure_tabs)
        self.PushButton_2.clicked.connect(self.restart_app)
        self.PrimaryPushButton.clicked.connect(self.save_and_close)
        self.PushButton.clicked.connect(self.close)
        self.ComboBox.currentIndexChanged.connect(self.toggle_proxy_config)

        self._foreach_switchButton(
            lambda switchButton, settingKey: switchButton.checkedChanged.connect(
                self.check_if_settings_changed
            )
        )

        self.ComboBox.currentIndexChanged.connect(self.check_if_settings_changed)
        self.LineEdit.textChanged.connect(self.check_if_settings_changed)
        self.LineEdit_2.textChanged.connect(self.check_if_settings_changed)
        self.LineEdit_3.textChanged.connect(self.check_if_settings_changed)
        self.PasswordLineEdit.textChanged.connect(self.check_if_settings_changed)
        self.ComboBox_3.currentIndexChanged.connect(self.check_if_settings_changed)

    def restart_app(self):
        msg_box = None

        if self.window.video_state == "VideoPlaying":
            msg_box = MessageBox(
                "Restart Confirmation",
                (
                    "Restarting now will stop the current playback and close the application.\n"
                    "Do you want to restart now?"
                ),
                self
            )
            msg_box.yesButton.setText("Restart")
            msg_box.cancelButton.setText("Cancel")

        if not msg_box or msg_box.exec_():
            self.window.save_settings()
            self.save_and_close()
            QApplication.quit()
            QProcess.startDetached(sys.executable, sys.argv)

    def save_and_close(self):
        self._foreach_switchButton(
            lambda switchButton, settingKey: setattr(
                self.window.app_settings, settingKey, switchButton.isChecked()
            )
        )

        self.window.app_settings.proxy_type = self.ComboBox.currentText()
        self.window.app_settings.proxy_host_name = self.LineEdit.text()
        port_text = self.LineEdit_2.text()
        self.window.app_settings.proxy_port = int(port_text) if port_text else DefaultAppSetting.proxy_port
        self.window.app_settings.proxy_login = self.LineEdit_3.text()
        self.window.app_settings.proxy_password = self.PasswordLineEdit.text()
        self.window.app_settings.opengl_enviroment = self.ComboBox_3.currentText()

        self.close()

    def configure_tabs(self):
        self.frame.hide()
        self.frame_2.hide()
        self.frame_3.hide()
        self.frame_4.hide()
        self.frame_5.hide()

        icon_path = self.window.icon_folder + "/plugins.png"

        if self.PillPushButton.isChecked():
            self.frame.show()
            self.ScrollArea.verticalScrollBar().setValue(0)
        elif self.PillPushButton_2.isChecked():
            self.frame_2.show()
        elif self.PillPushButton_3.isChecked():
            self.frame_3.show()        
        else:
            self.frame_4.show()
            self.ScrollArea.verticalScrollBar().setValue(0)
            icon_path = self.window.icon_folder + "/plugins-black.png"

        self.PillPushButton_4.setIcon(icon_path)

    def toggle_proxy_config(self):
        proxy_type = self.ComboBox.currentText()
        should_show = proxy_type in ["HttpProxy", "Socks5Proxy"]

        self.BodyLabel_10.setVisible(should_show)
        self.LineEdit.setVisible(should_show)
        self.BodyLabel_14.setVisible(should_show)
        self.LineEdit_2.setVisible(should_show)
        self.BodyLabel_16.setVisible(should_show)
        self.LineEdit_3.setVisible(should_show)
        self.BodyLabel_17.setVisible(should_show)
        self.PasswordLineEdit.setVisible(should_show)

    def check_if_settings_changed(self):
        SwitchButtonChanges = []
        self._foreach_switchButton(
            lambda switchButton, settingKey: SwitchButtonChanges.append(
                switchButton.isChecked() != getattr(self.window.app_settings, settingKey)
            )
        )
        if (any(SwitchButtonChanges) or
            self.ComboBox.currentText() != self.window.app_settings.proxy_type or
            self.LineEdit.text() != self.window.app_settings.proxy_host_name or
            self.LineEdit_2.text() != (str(self.window.app_settings.proxy_port) if self.window.app_settings.proxy_port is not None else "") or
            self.LineEdit_3.text() != self.window.app_settings.proxy_login or
            self.PasswordLineEdit.text() != self.window.app_settings.proxy_password or
            self.ComboBox_3.currentText() != self.window.app_settings.opengl_enviroment):

            self.PrimaryPushButton.setEnabled(True)
            self.PushButton_2.setText("Restart && Save")
        else:
            self.PrimaryPushButton.setEnabled(False)
            self.PushButton_2.setText("Restart")

    def _foreach_switchButton(self, func):
        switch_buttons_mapped = {
            "SwitchButton": "save_last_win_geometry",
            "SwitchButton_4": "open_last_url_at_startup",
            "SwitchButton_3": "ad_blocker",
            "SwitchButton_5": "fullscreen_mode_support",
            "SwitchButton_6": "support_animated_scrolling",
            "SwitchButton_2": "save_last_pos_of_mp",
            "SwitchButton_8": "save_last_zoom_factor",
            "SwitchButton_7": "discord_rpc",
            "SwitchButton_11": "win_thumbmail_buttons",
            "SwitchButton_12": "tray_icon",
            "SwitchButton_13": "track_change_notificator",
            "SwitchButton_14": "hotkey_playback_control",
            "SwitchButton_15": "only_audio_mode",
        }

        for attrName, settingKey in switch_buttons_mapped.items():
            switchButton = getattr(self, attrName)
            func(switchButton, settingKey)

    def load_ui(self):
        loadUi(f'{self.window.current_dir}/core/ui/settings_dialog.ui', self)
        try:
            pywinstyles.apply_style(self, "dark")
        except Exception as e:
            logging.error("Failed to apply dark style: " + str(e))

        self.setWindowTitle("Settings")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/settings.png"))

        self.setFixedSize(self.size())

    def closeEvent(self, event):
        self.window.show()
        event.accept()
