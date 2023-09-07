# file: screen_calculator.py
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout
from your_analytics_package import calculate_derivative_price

class DerivativeCalculator(QWidget):
    def __init__(self):
        super(DerivativeCalculator, self).__init__()

        self.initUI()

    def initUI(self):
        self.calculateButton = QPushButton('Calculate', self)
        self.inputField = QLineEdit(self)
        self.outputField = QLineEdit(self)
        self.outputField.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.inputField)
        vbox.addWidget(self.calculateButton)
        vbox.addWidget(self.outputField)

        self.setLayout(vbox)

        self.calculateButton.clicked.connect(self.perform_calculation)

    def perform_calculation(self):
        input_value = float(self.inputField.text())
        calculated_price = calculate_derivative_price(input_value)
        self.outputField.setText(str(calculated_price))
