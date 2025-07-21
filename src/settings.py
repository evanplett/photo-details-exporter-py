from pathlib import Path
from typing import List
from PySide6.QtCore import QCoreApplication, QSettings

QCoreApplication.setApplicationName("Photo Details Exporter")
QCoreApplication.setOrganizationName("Plett")


settings = QSettings()

THIS_DIR = str(Path().absolute())
READ_DIRECTORY = "read-directory"


def get_read_directory() -> str:
    return settings.value(READ_DIRECTORY, THIS_DIR)

def set_read_directory(directory: str) -> None:
    settings.setValue(READ_DIRECTORY, directory)

def get_supported_extensions() -> List[str]:
    return [".JPG"]