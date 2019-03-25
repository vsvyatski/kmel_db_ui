"""
Copyright (C) 2019  Vladimir Svyatski

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import glob
import os
from typing import List

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtDBus import QDBusInterface, QDBusConnection, QDBusMessage

import kmeldb_cli.kmeldb.mounts

_translate = QCoreApplication.translate


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


def unmount_usb_device(block_device: str):
    """
    Attempts to unmount a USB device via org.freedesktop.UDisks2.Filesystem D-Bus interface as described at
    http://storaged.org/doc/udisks2-api/latest/gdbus-org.freedesktop.UDisks2.Filesystem.html#gdbus-method-org-freedesktop-UDisks2-Filesystem.Unmount.

    :param block_device: a partition name to unmount, for example /dev/sdb1
    """
    if block_device is None:
        raise TypeError("'block_device' cannot be of type 'NoneType'")
    elif block_device == '':
        raise ValueError("'block_device' cannot be empty")

    path = block_device.replace('/dev', '/org/freedesktop/UDisks2/block_devices')
    file_system_interface = QDBusInterface('org.freedesktop.UDisks2', path, 'org.freedesktop.UDisks2.Filesystem',
                                           QDBusConnection.systemBus())
    if not file_system_interface.isValid():
        raise RuntimeError(_translate('DriveUtils', 'Invalid D-Bus interface'))

    reply = file_system_interface.call('Unmount', {})

    if reply.type() == QDBusMessage.ErrorMessage:
        raise RuntimeError(reply.errorMessage())
    elif reply.type() != QDBusMessage.ReplyMessage:
        raise RuntimeError(_translate('DriveUtils', 'Unexpected reply from Udisks'))
