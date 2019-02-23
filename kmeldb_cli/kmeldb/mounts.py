import os
try:
    import psutil
except ImportError:
    HAVE_PSUTIL = False
else:
    HAVE_PSUTIL = True


def get_fat_mounts():

    fat_mounts = []

    if HAVE_PSUTIL:
        partitions = psutil.disk_partitions()
        for part in partitions:
            lower_fstype = part.fstype.lower()
            if ('fat' in lower_fstype or 'msdos' in lower_fstype) and os.access(part.mountpoint, os.R_OK | os.W_OK):
                fat_mounts.append((part.mountpoint, part.fstype, part.device))
    else:
        mounts = os.popen('mount')
        for line in mounts.readlines():
            # device, ign1, mountpoint, ign2, filesystem, options = line.split()
            parts = line.split()
            device = parts[0]
            mountpoint = parts[2]
            if ('fat' in line or 'msdos' in line) and os.access(mountpoint, os.R_OK | os.W_OK):
                fat_mounts.append((mountpoint, 'vfat', device))
        mounts.close()
    return fat_mounts


def main():
    global HAVE_PSUTIL

    mounts1 = get_fat_mounts()
    for mount in mounts1:
        print(mount)

    if HAVE_PSUTIL:
        HAVE_PSUTIL = False
        mounts2 = get_fat_mounts()
        for mount in mounts2:
            print(mount)

        if mounts1 != mounts2:
            print('MOUNTS DIFFER')


if __name__ == '__main__':
    main()
