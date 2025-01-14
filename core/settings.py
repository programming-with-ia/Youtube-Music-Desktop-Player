from dataclasses import dataclass, MISSING, Field, asdict
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QSettings

from core.heplers import Helper


def do_nothing(v):
    return v


class Defaults:
    initialized = False
    qsettings: QSettings = None


def raise_on(validator):
    def validate(value):
        if validator(value):
            return value
        raise ValueError(f"Validation failed for value: {value}")

    return validate


@dataclass
class AppSettings:
    ad_blocker: int = 1
    save_last_win_geometry: int = 1
    open_last_url_at_startup: int = 1
    last_url: str = "https://music.youtube.com/"
    fullscreen_mode_support: int = 1
    support_animated_scrolling: int = 0
    save_last_pos_of_mp: int = 1
    last_win_geometry: do_nothing = None  # set in load_setting()
    save_last_zoom_factor: int = 1
    last_zoom_factor: float = 1.0
    last_download_folder: do_nothing = ""  # set default `current_dir` later
    discord_rpc: int = 0
    save_geometry_of_mp: int = 1
    geometry_of_mp: do_nothing = None  # set in load_setting()
    win_thumbmail_buttons: int = 1
    tray_icon: int = 1
    proxy_type: str = "NoProxy"
    proxy_host_name: str = ""
    proxy_port: int = 8080
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
            self.__dict__[key] = field.default  # set default value

            if value in [None, str(None)]:
                continue

            try:
                self.__dict__[key] = validator(value)
            except:
                pass
        Defaults.initialized = True

    @classmethod
    def load_setting(
        cls,
        qsetting: QSettings,
        last_download_folder: str,
    ):
        Defaults.qsettings = qsetting
        mapped_setting = dict()

        for key in cls.__dataclass_fields__.keys():
            mapped_setting[key] = qsetting.value(key)

        def orSet(key: str, value):
            mapped_setting[key] = mapped_setting[key] or value

        orSet("last_download_folder", last_download_folder)
        orSet("last_win_geometry", QRect(Helper.get_centered_geometry(1000, 580)))
        orSet("geometry_of_mp", QRect(Helper.get_centered_geometry(360, 150)))

        return cls(**mapped_setting)

    def __setattr__(self, name, value):

        if Defaults.initialized and name in self.__dataclass_fields__:

            if value is None:  #* debug errors, please set default value
                raise ValueError(f"Invalid Value of {name} is None")

            value = self._get_field(name).type(value)

            if value == getattr(AppSettings, name):
                Defaults.qsettings.remove(name)
            else:
                Defaults.qsettings.setValue(name, value)

        super().__setattr__(name, value)

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
