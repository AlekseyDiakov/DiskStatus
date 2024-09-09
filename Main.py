import sys
import shutil
import psutil
from PyQt5 import QtWidgets, uic


# Функция получения свободного места на диске в гигабайтах
def get_disk_space_gb(disk, space_type):
    # Получение размера свободного/занятого/общего места на диске в байтах
    space_bytes = getattr(shutil.disk_usage(disk), space_type)
    # Перевод размера из байтов в гигабайты
    return space_bytes / (1024**3)

# Функция получения списка доступных дисков
def get_disk_list():
    # Получение списка разделов дисков
    disk_drives = [drive.mountpoint for drive in psutil.disk_partitions()]
    return disk_drives

# Получение списка доступных дисков
disk_drives = get_disk_list()

# Цикл по каждому диску
for disk in disk_drives:
    # Получение свободного, занятого и общего места на диске
    free_space = get_disk_space_gb(disk, 'free')
    total_space = get_disk_space_gb(disk, 'total')
    used_space = get_disk_space_gb(disk, 'used')
    # Вывод информации о каждом диске
    print(f'Диск: {disk}, Свободно: {free_space:.2f} Гб, Всего: {total_space:.2f} Гб, Занято: {used_space:.2f} Гб')

if __name__ == "__main__":

    # Создание приложения
    app = QtWidgets.QApplication(sys.argv)
    # Загрузка интерфейса
    winapp = uic.loadUi("TstFrSpc.ui")

    # Обработка клика по кнопке "Общий объем"
    winapp.Btn_total.clicked.connect(lambda: winapp.textBrowser.setText(
        "\n".join(f"Диск {key}: Общий объем: {get_disk_space_gb(key, 'total'):.2f} Гб" for key in get_disk_list())
    ))
    # Обработка клика по кнопке "Занято"
    winapp.Btn_usage.clicked.connect(lambda: winapp.textBrowser.setText(
        "\n".join(f"Диск {key}: Занято: {get_disk_space_gb(key, 'used'):.2f} Гб" for key in get_disk_list())
    ))
    # Обработка клика по кнопке "Свободно"
    winapp.Btn_free.clicked.connect(lambda: winapp.textBrowser.setText(
        "\n".join(f"Диск {key}: Свободно: {get_disk_space_gb(key, 'free'):.2f} Гб" for key in get_disk_list())
    ))

    # Показ интерфейса
    winapp.show()
    # Закрытие приложения
    sys.exit(app.exec_())
