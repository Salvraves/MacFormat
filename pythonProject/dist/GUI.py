import tkinter as tk
import pyperclip
import re


# Функция для проверки, является ли строка MAC-адресом
def is_valid_mac(mac_address):
    # Регулярное выражение для проверки MAC-адреса в любом из форматов
    mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}$')
    return bool(mac_pattern.match(mac_address))


# Функция для отображения MAC-адреса из буфера обмена
def update_mac_address():
    mac_address = pyperclip.paste()

    # Проверяем, если это MAC-адрес
    if is_valid_mac(mac_address):
        mac_label.config(text=f"Mac: {mac_address}")
    else:
        mac_label.config(text="Mac address not found")


# Функция для обработки кнопок и копирования преобразованного MAC в буфер обмена
def change_mac_format_and_copy(format_function):
    mac_address = pyperclip.paste()
    if is_valid_mac(mac_address):
        converted_mac = format_function(mac_address)
        pyperclip.copy(converted_mac)
        root.after(500, root.iconify)  # Скрываем окно через 500 миллисекунд
    else:
        mac_label.config(text="Mac address not found")


# Функции преобразования MAC-адреса в нужные форматы

def convert_mac_cisco(mac_address):
    return mac_address.replace(":", "")[:4] + "-" + mac_address.replace(":", "")[4:8] + "-" + mac_address.replace(":",
                                                                                                                  "")[
                                                                                              8:]


def convert_mac_dlink(mac_address):
    return mac_address.replace(":", "")[:6] + "-" + mac_address.replace(":", "")[6:10] + "-" + mac_address.replace(":",
                                                                                                                   "")[
                                                                                               10:]


def convert_mac_tplink(mac_address):
    return mac_address.replace(":", "")[:4] + "-" + mac_address.replace(":", "")[4:8] + "-" + mac_address.replace(":",
                                                                                                                  "")[
                                                                                              8:]


def convert_mac_routeros(mac_address):
    return mac_address.replace(":", "")[:4] + "-" + mac_address.replace(":", "")[4:8] + "-" + mac_address.replace(":",
                                                                                                                  "")[
                                                                                              8:]


def convert_mac_zte(mac_address):
    return mac_address.replace(":", "")[:4] + "-" + mac_address.replace(":", "")[4:8] + "-" + mac_address.replace(":",
                                                                                                                  "")[
                                                                                              8:]


# Функция для преобразования в формат Huawei
def convert_mac_huawei(mac_address):
    return mac_address.replace(":", "")[:6] + "-" + mac_address.replace(":", "")[6:12] + "-" + mac_address.replace(":",
                                                                                                                   "")[
                                                                                               12:]


# Создаем GUI
root = tk.Tk()
root.title("Преобразование MAC-адреса")

# Метка для вывода MAC-адреса из буфера обмена
mac_label = tk.Label(root, text="Mac: ")
mac_label.pack(pady=10)

# Ряд 1: Кнопки для преобразования в различные форматы (вертикально)
left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=10)

cisco_button = tk.Button(left_frame, text="Cisco", command=lambda: change_mac_format_and_copy(convert_mac_cisco))
cisco_button.pack(pady=5)

dlink_button = tk.Button(left_frame, text="D-Link", command=lambda: change_mac_format_and_copy(convert_mac_dlink))
dlink_button.pack(pady=5)

tplink_button = tk.Button(left_frame, text="TP-Link", command=lambda: change_mac_format_and_copy(convert_mac_tplink))
tplink_button.pack(pady=5)

# Ряд 2: Кнопки для преобразования в другие форматы (вертикально)
right_frame = tk.Frame(root)
right_frame.pack(side="left", padx=10)

routeros_button = tk.Button(right_frame, text="RouterOS",
                            command=lambda: change_mac_format_and_copy(convert_mac_routeros))
routeros_button.pack(pady=5)

zte_button = tk.Button(right_frame, text="ZTE", command=lambda: change_mac_format_and_copy(convert_mac_zte))
zte_button.pack(pady=5)

huawei_button = tk.Button(right_frame, text="Huawei", command=lambda: change_mac_format_and_copy(convert_mac_huawei))
huawei_button.pack(pady=5)

# Обновляем MAC-адрес сразу после старта программы
update_mac_address()

# Запуск приложения
root.mainloop()
