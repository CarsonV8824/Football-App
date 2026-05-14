from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QFormLayout, QSizePolicy
from PySide6.QtCore import QSize, Qt

from frontend.tabs.inputPopup import PlayerDialog

class EntryTab(QWidget):
    def __init__(self) -> QWidget:
        super().__init__()
        main_container_layout = QGridLayout(self)
        side_widget = QWidget()
        side_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        side_widget.setObjectName("entryBar")
        side_widget_layout = QFormLayout(side_widget)
        main_layout = QVBoxLayout()
        main_container_layout.addLayout(main_layout, 0, 0, alignment=Qt.AlignLeft | Qt.AlignTop)
        main_layout.addWidget(side_widget)

        test_btn = QPushButton("input player")
        test_btn.setMaximumSize(QSize(200, 200))
        test_btn.clicked.connect(self.open_popup)
        side_widget_layout.addRow(test_btn)

        clear_btn = QPushButton("clear player")
        test_btn.setMaximumSize(QSize(200, 200))
        side_widget_layout.addRow(clear_btn)
    
    def open_popup(self):
        popup = PlayerDialog()
        if popup.exec():
            data = popup.get_data()
