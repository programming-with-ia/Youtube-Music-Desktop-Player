import sys
import logging
from typing import TYPE_CHECKING

import pywinstyles
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from qfluentwidgets import MessageBox


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
        self.SwitchButton.setChecked(self.window.app_settings.save_last_win_geometry)
        self.SwitchButton_4.setChecked(self.window.app_settings.open_last_url_at_startup)
        self.SwitchButton_3.setChecked(self.window.app_settings.ad_blocker)
        self.SwitchButton_5.setChecked(self.window.app_settings.fullscreen_mode_support)
        self.SwitchButton_6.setChecked(self.window.app_settings.support_animated_scrolling)
        self.SwitchButton_2.setChecked(self.window.app_settings.save_last_pos_of_mp)
        self.SwitchButton_8.setChecked(self.window.app_settings.save_last_zoom_factor)
        self.SwitchButton_7.setChecked(self.window.app_settings.discord_rpc)
        self.SwitchButton_11.setChecked(self.window.app_settings.win_thumbmail_buttons)
        self.SwitchButton_12.setChecked(self.window.app_settings.tray_icon)
        self.ComboBox.setCurrentIndex(self.proxy_types.index(self.window.app_settings.proxy_type))
        self.toggle_proxy_config()
        if self.window.app_settings.proxy_host_name is not None:
            self.LineEdit.setText(self.window.app_settings.proxy_host_name)
        if self.window.app_settings.proxy_port is not None:
            self.LineEdit_2.setText(str(self.window.app_settings.proxy_port))
        if self.window.app_settings.proxy_login is not None:
            self.LineEdit_3.setText(self.window.app_settings.proxy_login)
        if self.window.app_settings.proxy_password is not None:
            self.PasswordLineEdit.setText(self.window.app_settings.proxy_password)
        self.SwitchButton_13.setChecked(self.window.app_settings.track_change_notificator)
        self.SwitchButton_14.setChecked(self.window.app_settings.hotkey_playback_control)
        self.SwitchButton_15.setChecked(self.window.app_settings.only_audio_mode)
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

        self.SwitchButton.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_4.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_3.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_5.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_6.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_2.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_8.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_7.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_11.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_12.checkedChanged.connect(self.check_if_settings_changed)
        self.ComboBox.currentIndexChanged.connect(self.check_if_settings_changed)
        self.LineEdit.textChanged.connect(self.check_if_settings_changed)
        self.LineEdit_2.textChanged.connect(self.check_if_settings_changed)
        self.LineEdit_3.textChanged.connect(self.check_if_settings_changed)
        self.PasswordLineEdit.textChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_13.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_14.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_15.checkedChanged.connect(self.check_if_settings_changed)
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
        self.window.app_settings.save_last_win_geometry = int(self.SwitchButton.isChecked())
        self.window.app_settings.open_last_url_at_startup = int(self.SwitchButton_4.isChecked())
        self.window.app_settings.ad_blocker = int(self.SwitchButton_3.isChecked())
        self.window.app_settings.fullscreen_mode_support = int(self.SwitchButton_5.isChecked())
        self.window.app_settings.support_animated_scrolling = int(self.SwitchButton_6.isChecked())
        self.window.app_settings.save_last_pos_of_mp = int(self.SwitchButton_2.isChecked())
        self.window.app_settings.save_last_zoom_factor = int(self.SwitchButton_8.isChecked())
        self.window.app_settings.discord_rpc = int(self.SwitchButton_7.isChecked())
        self.window.app_settings.win_thumbmail_buttons = int(self.SwitchButton_11.isChecked())
        self.window.app_settings.tray_icon = int(self.SwitchButton_12.isChecked())
        self.window.app_settings.proxy_type = self.ComboBox.currentText()
        self.window.app_settings.proxy_host_name = self.LineEdit.text()
        port_text = self.LineEdit_2.text()
        self.window.app_settings.proxy_port = int(port_text) if port_text else None
        self.window.app_settings.proxy_login = self.LineEdit_3.text()
        self.window.app_settings.proxy_password = self.PasswordLineEdit.text()
        self.window.app_settings.track_change_notificator = int(self.SwitchButton_13.isChecked())
        self.window.app_settings.hotkey_playback_control = int(self.SwitchButton_14.isChecked())
        self.window.app_settings.only_audio_mode = int(self.SwitchButton_15.isChecked())
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
        if (self.SwitchButton.isChecked() != self.window.save_last_win_geometry_setting or
            self.SwitchButton_4.isChecked() != self.window.open_last_url_at_startup_setting or
            self.SwitchButton_3.isChecked() != self.window.ad_blocker_setting or
            self.SwitchButton_5.isChecked() != self.window.fullscreen_mode_support_setting or
            self.SwitchButton_6.isChecked() != self.window.support_animated_scrolling_setting or
            self.SwitchButton_2.isChecked() != self.window.save_last_pos_of_mp_setting or
            self.SwitchButton_8.isChecked() != self.window.save_last_zoom_factor_setting or
            self.SwitchButton_7.isChecked() != self.window.discord_rpc_setting or
            self.SwitchButton_11.isChecked() != self.window.win_thumbmail_buttons_setting or
            self.SwitchButton_12.isChecked() != self.window.tray_icon_setting or
            self.ComboBox.currentText() != self.window.proxy_type_setting or
            self.LineEdit.text() != self.window.proxy_host_name_setting or
            self.LineEdit_2.text() != (str(self.window.proxy_port_setting) if self.window.proxy_port_setting is not None else "") or
            self.LineEdit_3.text() != self.window.proxy_login_setting or
            self.PasswordLineEdit.text() != self.window.proxy_password_setting or
            self.SwitchButton_13.isChecked() != self.window.track_change_notificator_setting or
            self.SwitchButton_14.isChecked() != self.window.hotkey_playback_control_setting or
            self.SwitchButton_15.isChecked() != self.window.only_audio_mode_setting or
            self.ComboBox_3.currentText() != self.window.opengl_enviroment_setting):

            self.PrimaryPushButton.setEnabled(True)
            self.PushButton_2.setText("Restart && Save")
        else:
            self.PrimaryPushButton.setEnabled(False)
            self.PushButton_2.setText("Restart")

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