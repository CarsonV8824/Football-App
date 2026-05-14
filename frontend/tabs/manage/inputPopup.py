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
        self.pos_input = QLineEdit()
        self.team_input = QLineEdit()

        layout.addRow("Name:", self.name_input)
        layout.addRow("Position:", self.pos_input)
        layout.addRow("Team:", self.team_input)

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
            pos_input = self.pos_input.text()
            team_input = self.team_input.text()
        except ValueError as e:
            QMessageBox.warning(self, "Wrong input", str(e))
            return None

        return {
            "name": name_input,
            "pos": pos_input,
            "week": team_input
        }

