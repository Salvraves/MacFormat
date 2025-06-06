import tkinter as tk
from tkinter import ttk
import pyperclip
import re
import requests


# Функция для проверки, является ли строка MAC-адресом
def is_valid_mac(mac_address):
    # Регулярное выражение для проверки MAC-адреса в любом из форматов
    mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}$')
    return bool(mac_pattern.match(mac_address))


# Функция для получения информации о вендоре по MAC-адресу (первое 3 байта)
def get_vendor(mac_address):
    # Извлекаем первые 6 символов (3 байта) для OUI
    oui = mac_address.replace(":", "")[:6].upper()
    try:
        # Запрос к базе данных OUI для получения вендора
        response = requests.get(f'https://api.macvendors.com/{oui}')
        return response.text if response.status_code == 200 else "Vendor not found"
    except:
        return "Error fetching vendor"


# Функция для отображения MAC-адреса из буфера обмена
def update_mac_address():
    mac_address = pyperclip.paste()

    # Проверяем, если это MAC-адрес
    if is_valid_mac(mac_address):
        mac_label.config(text=f"Mac: {mac_address}")
        vendor_info.config(text=f"Vendor: {get_vendor(mac_address)}")
    else:
        mac_label.config(text="Mac address not found")
        vendor_info.config(text="Vendor: N/A")


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

# Устанавливаем стиль для приложения с темной темой
style = ttk.Style()
style.theme_use('clam')  # Используем встроенную тему "clam", которая подходит для темной темы

# Настройки темной темы
style.configure('TButton',
                font=('Arial', 12),
                padding=10,
                relief="flat",
                background="#333333",  # Темный фон
                foreground="white",  # Белый текст
                highlightthickness=2,  # Толщина контура
                highlightbackground="green",  # Зеленый контур при наведении
                highlightcolor="green",  # Зеленый контур при активации
                activebackground="#333333",  # Темный фон при нажатии
                activeforeground="white",  # Белый текст при нажатии
                focuscolor="green")  # Цвет фокуса, зеленый

style.configure('TLabel',
                font=('Arial', 12),
                padding=10,
                background="#333333",  # Темный фон
                foreground="white")  # Белый текст

style.configure('TFrame',
                background="#333333")  # Темный фон для фрейма

# Устанавливаем фон для всего окна
root.configure(bg="#333333")

# Создаем вертикальный Frame для всех элементов
frame = ttk.Frame(root, padding=20)
frame.pack(padx=20, pady=20)

# Метка для вывода MAC-адреса из буфера обмена
mac_label = ttk.Label(frame, text="Mac: ", anchor="w")
mac_label.pack(pady=10, fill="both", expand=True)

# Метка для вывода информации о вендоре
vendor_info = ttk.Label(frame, text="Vendor: N/A", anchor="w")
vendor_info.pack(pady=5, fill="both", expand=True)

# Ряд 1: Кнопки для преобразования в различные форматы (вертикально)
left_frame = ttk.Frame(frame)
left_frame.pack(side="top", pady=10, fill="both", expand=True)

cisco_button = ttk.Button(left_frame, text="Cisco", command=lambda: change_mac_format_and_copy(convert_mac_cisco))
cisco_button.pack(pady=5, fill="both", expand=True)

dlink_button = ttk.Button(left_frame, text="D-Link", command=lambda: change_mac_format_and_copy(convert_mac_dlink))
dlink_button.pack(pady=5, fill="both", expand=True)

tplink_button = ttk.Button(left_frame, text="TP-Link", command=lambda: change_mac_format_and_copy(convert_mac_tplink))
tplink_button.pack(pady=5, fill="both", expand=True)

# Ряд 2: Кнопки для преобразования в другие форматы (вертикально)
right_frame = ttk.Frame(frame)
right_frame.pack(side="top", pady=10, fill="both", expand=True)

routeros_button = ttk.Button(right_frame, text="RouterOS",
                             command=lambda: change_mac_format_and_copy(convert_mac_routeros))
routeros_button.pack(pady=5, fill="both", expand=True)

zte_button = ttk.Button(right_frame, text="ZTE", command=lambda: change_mac_format_and_copy(convert_mac_zte))
zte_button.pack(pady=5, fill="both", expand=True)

huawei_button = ttk.Button(right_frame, text="Huawei", command=lambda: change_mac_format_and_copy(convert_mac_huawei))
huawei_button.pack(pady=5, fill="both", expand=True)

# Кнопка "Get Vendor MAC Address" перемещена вниз, под кнопками
vendor_button = ttk.Button(frame, text="Get Vendor MAC Address", command=update_mac_address)
vendor_button.pack(pady=20, fill="both", expand=True)

# Обновляем MAC-адрес сразу после старта программы
update_mac_address()

# Привязка горячих клавиш для обновления MAC-адреса с Alt+Insert
root.bind('<Alt-Insert>', lambda event: update_mac_address())

# Запуск приложения
root.mainloop()
