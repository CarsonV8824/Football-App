import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_container_widget = QWidget()
        main_layout = QVBoxLayout()
        main_container_widget.setLayout(main_layout)

        test_btn = QPushButton("test")
        test_btn.setMaximumSize(QSize(200, 200))
        test_btn.clicked.connect(lambda: print("works"))
        main_layout.addWidget(test_btn)

        self.setCentralWidget(main_container_widget)