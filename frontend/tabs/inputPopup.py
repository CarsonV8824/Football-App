import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QDialogButtonBox,
    QMessageBox
)

class PlayerDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Player")

        layout = QFormLayout()

        # Inputs
        self.name_input = QLineEdit()
        self.week_input = QLineEdit()
        self.year_input = QLineEdit()

        layout.addRow("Name:", self.name_input)
        layout.addRow("Week:", self.week_input)
        layout.addRow("Year:", self.year_input)

        # OK / Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        try:
            name_input = self.name_input.text()
            week_input = int(self.week_input.text())
            year_input = int(self.year_input.text())
        except (ValueError, TypeError) as e:
            QMessageBox.warning(self, "Wrong input", str(e))
            return None

        return {
            "name": name_input,
            "week": week_input,
            "year": year_input,
        }

