from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import urllib.request


class MacFormatterApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.oui_map = {}
        self.setupUi()
        self.download_oui_database()

    def setupUi(self):
        self.setWindowTitle("Mac Formatter")
        self.resize(500, 600)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setStyleSheet("background-color: rgb(33, 33, 33); color: white;")

        font = QtGui.QFont("Corus", 14)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Масштабируемый фон
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setScaledContents(True)
        self.background.setPixmap(QtGui.QPixmap("gora_vershina_zasnezhennyj_130941_3840x2160.jpg"))
        self.background.setGeometry(0, 0, self.width(), self.height())

        # Vendor
        self.label_vendor = QtWidgets.QLabel("Vendor:", self.centralwidget)
        self.label_vendor.setGeometry(QtCore.QRect(10, 20, 441, 41))
        self.label_vendor.setFont(QtGui.QFont("Corus", 16))
        self.label_vendor.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white;")

        # Your MAC
        self.label_mac = QtWidgets.QLabel("Your mac:", self.centralwidget)
        self.label_mac.setGeometry(QtCore.QRect(10, 60, 441, 41))
        self.label_mac.setFont(font)
        self.label_mac.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white;")

        # Кнопки вендоров
        self.TP_linkButton = self.make_button("TP-Link", 30, 130, lambda: self.format_mac("TP-Link"))
        self.D_linkButton = self.make_button("D-Link", 190, 130, lambda: self.format_mac("D-Link"))
        self.HuaweiButton = self.make_button("Huawei", 30, 200, lambda: self.format_mac("Huawei"))
        self.ZTEButton = self.make_button("ZTE", 190, 200, lambda: self.format_mac("ZTE"))

        self.background.lower()

        # Трей
        self.tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icon.png"), self)
        self.tray_icon.setToolTip("MAC Formatter")
        tray_menu = QtWidgets.QMenu()
        show_action = tray_menu.addAction("Показать окно")
        show_action.triggered.connect(self.show_window)
        exit_action = tray_menu.addAction("Выход")
        exit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Горячая клавиша Alt+Insert
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Alt+Insert"), self)
        self.shortcut.activated.connect(self.show_window)

        # Таймер для автообновления MAC из буфера
        self.clipboard_timer = QtCore.QTimer(self)
        self.clipboard_timer.timeout.connect(self.check_clipboard_change)
        self.clipboard_timer.start(1000)

        self.last_clipboard_text = ""
        self.show_mac_from_clipboard()

    def resizeEvent(self, event):
        self.background.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def make_button(self, title, x, y, callback):
        btn = QtWidgets.QPushButton(title, self.centralwidget)
        btn.setGeometry(QtCore.QRect(x, y, 140, 51))
        btn.setFont(QtGui.QFont("Corus", 14))
        btn.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: rgba(45, 50, 80, 120); color: white; border: none; }"
            "QPushButton:hover { background-color: rgb(66, 70, 105); }"
        )
        btn.setFocusPolicy(QtCore.Qt.StrongFocus)  # Поддержка Tab
        btn.clicked.connect(lambda _, cb=callback: (cb(), self.hide()))  # Enter = формат и скрыть
        return btn

    def normalize_mac(self, mac):
        mac = mac.strip().upper().replace("-", "").replace(":", "").replace(".", "")
        if len(mac) != 12 or not all(c in "0123456789ABCDEF" for c in mac):
            return None
        return mac

    def format_mac(self, vendor):
        clipboard = QtWidgets.QApplication.clipboard()
        raw = clipboard.text()
        mac = self.normalize_mac(raw)
        if not mac:
            self.label_mac.setText("Your mac: Not mac address")
            self.label_vendor.setText("Vendor: Not Supported")
            return

        if vendor == "TP-Link":
            formatted = ":".join([mac[i:i + 2] for i in range(0, 12, 2)])
        elif vendor == "Huawei":
            formatted = "-".join([mac[i:i + 4] for i in range(0, 12, 4)])
        elif vendor == "D-Link":
            formatted = "-".join([mac[i:i + 2] for i in range(0, 12, 2)])
        elif vendor == "ZTE":
            formatted = ".".join([mac[i:i + 2] for i in range(0, 12, 2)])
        else:
            formatted = mac

        clipboard.setText(formatted)

    def show_mac_from_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        raw = clipboard.text()
        mac = self.normalize_mac(raw)
        if mac:
            formatted_mac = ":".join([mac[i:i + 2] for i in range(0, 12, 2)])
            vendor = self.get_vendor(mac)
            self.label_mac.setText(f"Your mac: {formatted_mac}")
            self.label_vendor.setText(f"Vendor: {vendor}")
        else:
            self.label_mac.setText("Your mac: Not mac address")
            self.label_vendor.setText("Vendor: Not Supported")

    def check_clipboard_change(self):
        clipboard = QtWidgets.QApplication.clipboard()
        current_text = clipboard.text()
        if current_text != self.last_clipboard_text:
            self.last_clipboard_text = current_text
            self.show_mac_from_clipboard()

    def get_vendor(self, mac):
        oui = ":".join([mac[i:i + 2] for i in range(0, 6, 2)])
        return self.oui_map.get(oui, "Unknown")

    def download_oui_database(self):
        try:
            url = "https://standards-oui.ieee.org/oui/oui.txt"
            response = urllib.request.urlopen(url)
            data = response.read().decode("utf-8")
            for line in data.splitlines():
                if "(hex)" in line:
                    parts = line.split("(hex)")
                    oui = parts[0].strip().replace("-", ":")
                    vendor = parts[1].strip()
                    self.oui_map[oui] = vendor
        except Exception as e:
            print("Failed to download OUI database:", e)

    def show_window(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MacFormatterApp()
    window.show()
    sys.exit(app.exec_())
