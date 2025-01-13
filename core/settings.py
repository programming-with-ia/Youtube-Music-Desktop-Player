from dataclasses import dataclass, MISSING, Field
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QSettings

from core.heplers import Helper


def do_nothing(v):
    return v


class Defaults:
    initialized = False
    qsettings: QSettings = None


@dataclass
class AppSettings:
    ad_blocker: int = 1
    save_last_win_geometry: int = 1
    open_last_url_at_startup: int = 1
    last_url: str = "https://music.youtube.com/"
    fullscreen_mode_support: int = 1
    support_animated_scrolling: int = 0
    save_last_pos_of_mp: int = 1
    last_win_geometry: do_nothing = QRect(Helper.get_centered_geometry(1000, 580))
    save_last_zoom_factor: float = 1
    last_zoom_factor: float = 1.0
    last_download_folder: do_nothing = ""  # set default `current_dir` later
    discord_rpc: int = 0
    save_geometry_of_mp: int = 1
    geometry_of_mp: do_nothing = QRect(Helper.get_centered_geometry(360, 150))
    win_thumbmail_buttons: int = 1
    tray_icon: int = 1
    proxy_type: str = "NoProxy"
    proxy_host_name: str = ""
    proxy_port: str = ""
    proxy_login: str = ""
    proxy_password: str = ""
    track_change_notificator: int = 0
    hotkey_playback_control: int = 1
    only_audio_mode: int = 0
    opengl_enviroment: str = "Auto"

    def __post_init__(self):

        for key, field in self.__dataclass_fields__.items():
            validator = field.type
            value = self.__dict__[key]
            try:
                if value is None:
                    raise ValueError
                validator(value)
            except:
                self.__dict__[key] = field.default  # set default value

        Defaults.initialized = True

    @classmethod
    def load_setting(cls, setting: QSettings):
        Defaults.qsettings = setting
        mapped_setting = dict()

        for key in cls.__dataclass_fields__.keys():
            mapped_setting[key] = setting.value(key)

        return cls(**mapped_setting)

    # @classmethod
    # def getDefault(cls, key):
    #     field = cls._get_field(key)
    #     if field is None or field.default is MISSING:
    #         return
    #     return field.default

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        #! also use validator if needed
        if not Defaults.initialized or name not in self.__dataclass_fields__:
            return

        Defaults.qsettings.setValue(name, value)

    @classmethod
    def validate_value(cls, key: str, value):
        field = cls._get_field(key)
        validator = field.type

        if value is None:
            return field.default

        try:
            return validator(value)
        except:
            return field.default

    @classmethod
    def _get_field(cls, key: str) -> Field:
        return cls.__dataclass_fields__.get(key)
