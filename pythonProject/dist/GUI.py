import tkinter as tk
import pyperclip

# Функции преобразования MAC-адреса в нужные форматы

def convert_mac_cisco(mac_address):
    return mac_address.replace(":", "")[:4] + "-" + mac_address.replace(":", "")[4:8] + "-" + mac_address.replace(":", "")[8:]

def convert_mac_dlink(mac_address):
    return mac_address.replace(":", "")[:6] + "-" + mac_address.replace(":", "")[6:10] + "-" + mac_address.replace(":", "")[10:]

def convert_mac_tplink(mac_address):
    return mac_address.replace(":", "")[:4] + "-" + mac_address.replace(":", "")[4:8] + "-" + mac_address.replace(":", "")[8:]

def convert_mac_routeros(mac_address):
    return mac_address.replace(":", "")[:4] + "-" + mac_address.replace(":", "")[4:8] + "-" + mac_address.replace(":", "")[8:]

def convert_mac_zte(mac_address):
    return mac_address.replace(":", "")[:4] + "-" + mac_address.replace(":", "")[4:8] + "-" + mac_address.replace(":", "")[8:]

# Функция для получения MAC-адреса из буфера обмена и его отображения
def get_mac_address():
    mac_address = pyperclip.paste()
    mac_label.config(text=f"Mac: {mac_address}")

# Функции для обработки кнопок и копирования преобразованного MAC в буфер обмена
def change_mac_format_and_copy(format_function):
    mac_address = pyperclip.paste()
    if len(mac_address) == 17 and mac_address.count(":") == 5:
        converted_mac = format_function(mac_address)
        pyperclip.copy(converted_mac)
        result_label.config(text=f"Преобразованный MAC: {converted_mac}")
    else:
        result_label.config(text="Неверный формат MAC-адреса")

# Создаем GUI
root = tk.Tk()
root.title("Преобразование MAC-адреса")

# Метка для вывода MAC-адреса из буфера обмена
mac_label = tk.Label(root, text="Mac: ")
mac_label.pack(pady=10)

# Кнопки для преобразования в различные форматы
cisco_button = tk.Button(root, text="Cisco", command=lambda: change_mac_format_and_copy(convert_mac_cisco))
cisco_button.pack(pady=5)

dlink_button = tk.Button(root, text="D-Link", command=lambda: change_mac_format_and_copy(convert_mac_dlink))
dlink_button.pack(pady=5)

tplink_button = tk.Button(root, text="TP-Link", command=lambda: change_mac_format_and_copy(convert_mac_tplink))
tplink_button.pack(pady=5)

routeros_button = tk.Button(root, text="RouterOS", command=lambda: change_mac_format_and_copy(convert_mac_routeros))
routeros_button.pack(pady=5)

zte_button = tk.Button(root, text="ZTE", command=lambda: change_mac_format_and_copy(convert_mac_zte))
zte_button.pack(pady=5)

# Метка для вывода преобразованного MAC
result_label = tk.Label(root, text="Преобразованный MAC: ")
result_label.pack(pady=10)

# Кнопка для получения MAC-адреса из буфера обмена
get_mac_button = tk.Button(root, text="Получить MAC из буфера обмена", command=get_mac_address)
get_mac_button.pack(pady=10)

# Запуск приложения
root.mainloop()
