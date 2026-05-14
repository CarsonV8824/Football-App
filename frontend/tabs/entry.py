from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, QVBoxLayout, 
    QPushButton, 
    QGridLayout,
    QLineEdit
)
from PySide6.QtCore import QSize, Qt

class EntryTab(QWidget):
    def __init__(self) -> QWidget:
        super().__init__()
        main_container_layout = QGridLayout(self)
        main_layout = QVBoxLayout()
        main_container_layout.addLayout(main_layout, 0, 0, alignment=Qt.AlignCenter)

        name_entry = QLineEdit()
        name_entry.setMaximumSize(QSize(600, 200))
        main_layout.addWidget(name_entry, 1, alignment=Qt.AlignHCenter | Qt.AlignTop)

        test_btn = QPushButton("test")
        test_btn.setMaximumSize(QSize(200, 200))
        test_btn.clicked.connect(lambda: print("works"))
        main_layout.addWidget(test_btn, 1, alignment=Qt.AlignHCenter | Qt.AlignTop)