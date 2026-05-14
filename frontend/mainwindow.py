import sys
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, QVBoxLayout, 
    QPushButton, 
    QGridLayout,
    QLineEdit,
    QTabWidget
)
from PySide6.QtCore import QSize, Qt

from frontend.tabs.manage.manage import ManageTab
from frontend.tabs.perdict.perdict import PerdictTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(700, 500)
        main_container_widget = QWidget()
        main_container_layout = QGridLayout(main_container_widget)
        main_layout = QVBoxLayout()
        main_container_layout.addLayout(main_layout, 0, 0, alignment=Qt.AlignCenter)

        main_tab_widget = QTabWidget()
        main_tab_widget.addTab(ManageTab(), "Manage")
        main_tab_widget.addTab(PerdictTab(), "Perdict")

        main_layout.addWidget(main_tab_widget)
        self.setCentralWidget(main_container_widget)
