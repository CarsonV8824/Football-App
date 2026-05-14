import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow

from frontend.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Fantasy Football App")
    style_path = os.path.join("frontend", "assets", "style.css")
    with open(style_path, "r") as f:
        _style = f.read()
    
    app.setStyleSheet(_style)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()