from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, QVBoxLayout, 
    QPushButton, 
    QGridLayout,
    QLineEdit
)
from PySide6.QtCore import QSize, Qt

class ManageTab(QWidget):
    def __init__(self) -> QWidget:
        super().__init__()
        main_container_layout = QGridLayout(self)
        main_layout = QVBoxLayout()
        main_container_layout.addLayout(main_layout, 0, 0, alignment=Qt.AlignCenter)