# file: test_screen_calculator.py
import pytest
from PyQt5.QtCore import Qt
from screen_calculator import DerivativeCalculator

@pytest.fixture
def calculator(qtbot):
    widget = DerivativeCalculator()
    qtbot.addWidget(widget)
    return widget

def test_calculate_button_click(qtbot, calculator):
    # Arrange
    calculator.inputField.setText("2.0")
    
    # Act
    qtbot.mouseClick(calculator.calculateButton, Qt.LeftButton)
    
    # Assert
    assert calculator.outputField.text() == "4.0"
