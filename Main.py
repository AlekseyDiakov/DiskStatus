from PyQt5 import QtWidgets, uic
import sys
import shutil
import psutil

def get_free_disk_space_gb(disk):
    free_space_bytes = shutil.disk_usage(disk).free
    return free_space_bytes / (1024**3)

def get_total_disk_space_gb(disk):
    total_space_bytes = shutil.disk_usage(disk).total
    return total_space_bytes / (1024**3)

def get_used_disk_space_gb(disk):
    used_space_bytes = shutil.disk_usage(disk).used
    return used_space_bytes / (1024**3)

def get_disk_list():
    disk_drives = [drive.mountpoint for drive in psutil.disk_partitions()]
    return disk_drives

disk_drives = get_disk_list()
total_disk_space_dict = {disk: get_total_disk_space_gb(disk) for disk in disk_drives}
used_disk_space_dict = {disk: get_used_disk_space_gb(disk) for disk in disk_drives}
free_disk_space_dict = {disk: get_free_disk_space_gb(disk) for disk in disk_drives}

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    winapp = uic.loadUi("TstFrSpc.ui")

    winapp.Btn_total.clicked.connect(lambda: winapp.textBrowser.setText("\n".join(f"Disk {key}: Total space: {value:.2f} Gb" for key, value in total_disk_space_dict.items())))
    winapp.Btn_usage.clicked.connect(lambda: winapp.textBrowser.setText("\n".join(f"Disk {key}: Used space: {value:.2f} Gb" for key, value in used_disk_space_dict.items())))
    winapp.Btn_free.clicked.connect(lambda: winapp.textBrowser.setText("\n".join(f"Disk {key}: Free space: {value:.2f} Gb" for key, value in free_disk_space_dict.items())))


    winapp.show()
    sys.exit(app.exec_())