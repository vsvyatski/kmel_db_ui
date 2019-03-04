import glob
import os
from typing import List

import kmeldb_cli.kmeldb.mounts


class UsbDriveInfo:
    def __init__(self, mount_point: str = None, device: str = None):
        self.__mount_point = mount_point
        self.__device = device

    @property
    def mount_point(self) -> str:
        return self.__mount_point

    @mount_point.setter
    def mount_point(self, value: str):
        self.__mount_point = value

    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, value: str):
        self.__device = value

    @property
    def label(self):
        if self.__mount_point is None:
            return None

        last_slash_index = self.__mount_point.rfind('/')
        if last_slash_index == -1:
            return None

        return self.__mount_point[last_slash_index + 1:]


def is_usb_device(device_path: str) -> bool:
    for dev_link in glob.glob('/dev/disk/by-id/usb*'):
        if os.path.realpath(dev_link) == device_path:
            return True
    return False


def get_fat_usb_mounts() -> List[UsbDriveInfo]:
    usb_drives = []
    for fat_mount in kmeldb_cli.kmeldb.mounts.get_fat_mounts():
        if is_usb_device(fat_mount[2]):
            usb_drives.append(UsbDriveInfo(fat_mount[0], fat_mount[2]))
    return usb_drives
