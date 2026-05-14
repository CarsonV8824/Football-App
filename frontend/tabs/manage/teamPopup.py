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

class TeamDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Team")

        layout = QFormLayout()

        # Inputs
        self.team_name = QLineEdit()
        self.team_year = QLineEdit()

        layout.addRow("Team Name:", self.team_name)
        layout.addRow("Starting_year", self.team_year)

        # OK / Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setLayout(layout)