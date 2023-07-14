import sys
from math import log, sqrt, exp
from scipy.stats import norm
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
import argparse
import json

class BlackScholesCalculator(QMainWindow):
    def __init__(self, default_values):
        super().__init__()
        self.default_values = default_values
        self.entry_s = None
        self.entry_r = None
        self.entry_q = None
        self.entry_t = []
        self.entry_sigma = []
        self.entry_k = []
        self.option_buttons = []
        self.entry_quantity = []
        self.entry_implied_strike = []
        self.table_widget = None
        self.total_price_label = None
        self.total_price = None
        self.target_total_price = None
        self.saved_data = {}

        self.setWindowTitle("Black-Scholes Calculator")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout()
        hbox_total_price = QHBoxLayout()

        # Create input row for current price, risk-free rate, and dividend yield
        hbox_inputs = QHBoxLayout()

        label_s = QLabel("Current Price (S):")
        self.entry_s = QLineEdit()
        self.entry_s.setText(str(self.default_values['current_price']))

        label_r = QLabel("Risk-Free Rate (r):")
        self.entry_r = QLineEdit()
        self.entry_r.setText(str(self.default_values['risk_free_rate']))

        label_q = QLabel("Dividend Yield (q):")
        self.entry_q = QLineEdit()
        self.entry_q.setText(str(self.default_values['dividend_yield']))

        hbox_inputs.addWidget(label_s)
        hbox_inputs.addWidget(self.entry_s)
        hbox_inputs.addWidget(label_r)
        hbox_inputs.addWidget(self.entry_r)
        hbox_inputs.addWidget(label_q)
        hbox_inputs.addWidget(self.entry_q)

        vbox.addLayout(hbox_inputs)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(["Quantity", "Strike Price (K)", "Calculate Strike", "Time to Expiration (t)",
                                                     "Volatility (σ)", "Option Price", "Option Total Price", "Type"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.table_widget)

        for row in range(4):
            self.table_widget.insertRow(row)

            quantity_item = QTableWidgetItem("0")
            strike_item = QTableWidgetItem(str(self.default_values['strike_price']))
            calculate_strike_button = QPushButton("Calculate")
            calculate_strike_button.clicked.connect(lambda _, i=row: self.calculate_implied_strike(i))
            t_item = QTableWidgetItem(str(self.default_values['time_to_expiry']))
            sigma_item = QTableWidgetItem(str(self.default_values['volatility']))
            option_price_item = QTableWidgetItem("")
            option_total_price_item = QTableWidgetItem("")
            option_type_item = QTableWidgetItem("Call")

            self.table_widget.setItem(row, 0, quantity_item)
            self.table_widget.setItem(row, 1, strike_item)
            self.table_widget.setCellWidget(row, 2, calculate_strike_button)
            self.table_widget.setItem(row, 3, t_item)
            self.table_widget.setItem(row, 4, sigma_item)
            self.table_widget.setItem(row, 5, option_price_item)
            self.table_widget.setItem(row, 6, option_total_price_item)
            self.table_widget.setItem(row, 7, option_type_item)

        calculate_button = QPushButton("Calculate Total")
        calculate_button.clicked.connect(self.calculate_prices)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_values)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_data)
        load_button = QPushButton("Reload")
        load_button.clicked.connect(self.load_data)

        hbox_total_price.addWidget(QLabel("Target Total Price:"))
        self.target_total_price = QLineEdit()
        hbox_total_price.addWidget(self.target_total_price)
        hbox_total_price.addStretch(1)

        self.total_price_label = QLabel("Total Price: 0.0000")
        self.total_price = 0.0

        vbox.addWidget(calculate_button)
        vbox.addWidget(reset_button)
        vbox.addLayout(hbox_total_price)
        vbox.addWidget(self.total_price_label)
        vbox.addWidget(save_button)
        vbox.addWidget(load_button)

        central_widget.setLayout(vbox)

    def calculate_prices(self):
        S = float(self.entry_s.text())
        r = float(self.entry_r.text())
        q = float(self.entry_q.text())

        total_price = 0.0

        for row in range(4):
            quantity_item = self.table_widget.item(row, 0)
            strike_item = self.table_widget.item(row, 1)
            t_item = self.table_widget.item(row, 3)
            sigma_item = self.table_widget.item(row, 4)
            option_price_item = self.table_widget.item(row, 5)
            option_total_price_item = self.table_widget.item(row, 6)
            option_type_item = self.table_widget.item(row, 7)

            quantity = int(quantity_item.text())
            K = float(strike_item.text())
            t = float(t_item.text())
            sigma = float(sigma_item.text())
            option_type = option_type_item.text()

            d1 = (log(S / K) + (r - q + 0.5 * sigma ** 2) * t) / (sigma * sqrt(t))
            d2 = d1 - sigma * sqrt(t)

            if option_type == 'Call':
                option_price = S * exp(-q * t) * norm.cdf(d1) - K * exp(-r * t) * norm.cdf(d2)
            elif option_type == 'Put':
                option_price = K * exp(-r * t) * norm.cdf(-d2) - S * exp(-q * t) * norm.cdf(-d1)
            else:
                option_price = 0.0

            option_total_price = option_price * quantity
            total_price += option_total_price

            option_price_item.setText("{:.4f}".format(option_price))
            option_total_price_item.setText("{:.4f}".format(option_total_price))

        self.update_total_price(total_price)

    def calculate_implied_strike(self, row):
        S = float(self.entry_s.text())
        r = float(self.entry_r.text())
        q = float(self.entry_q.text())
        t_item = self.table_widget.item(row, 3)
        sigma_item = self.table_widget.item(row, 4)
        option_type_item = self.table_widget.item(row, 7)
        implied_strike_button = self.table_widget.cellWidget(row, 2)

        t = float(t_item.text())
        sigma = float(sigma_item.text())
        option_type = option_type_item.text()

        target_price = float(self.target_total_price.text())

        epsilon = 0.01
        lower_strike = 0.0
        upper_strike = 200.0  # Adjust the upper limit based on the expected range of strike prices

        while abs(self.total_price - target_price) > epsilon:
            implied_strike = (lower_strike + upper_strike) / 2.0

            d1 = (log(S / implied_strike) + (r - q + 0.5 * sigma ** 2) * t) / (sigma * sqrt(t))
            d2 = d1 - sigma * sqrt(t)

            if option_type == 'Call':
                option_price = S * exp(-q * t) * norm.cdf(d1) - implied_strike * exp(-r * t) * norm.cdf(d2)
            elif option_type == 'Put':
                option_price = implied_strike * exp(-r * t) * norm.cdf(-d2) - S * exp(-q * t) * norm.cdf(-d1)
            else:
                option_price = 0.0

            self.table_widget.item(row, 1).setText("{:.2f}".format(implied_strike))
            self.table_widget.item(row, 5).setText("{:.4f}".format(option_price))
            self.calculate_prices()

            if self.total_price < target_price:
                lower_strike = implied_strike
            else:
                upper_strike = implied_strike

    def update_total_price(self, total_price):
        self.total_price = total_price
        self.total_price_label.setText("Total Price: {:.4f}".format(total_price))

    def reset_values(self):
        self.entry_s.setText(str(self.default_values['current_price']))
        self.entry_r.setText(str(self.default_values['risk_free_rate']))
        self.entry_q.setText(str(self.default_values['dividend_yield']))

        for row in range(4):
            quantity_item = self.table_widget.item(row, 0)
            strike_item = self.table_widget.item(row, 1)
            t_item = self.table_widget.item(row, 3)
            sigma_item = self.table_widget.item(row, 4)
            option_price_item = self.table_widget.item(row, 5)
            option_total_price_item = self.table_widget.item(row, 6)
            option_type_item = self.table_widget.item(row, 7)

            quantity_item.setText("0")
            strike_item.setText(str(self.default_values['strike_price']))
            t_item.setText(str(self.default_values['time_to_expiry']))
            sigma_item.setText(str(self.default_values['volatility']))
            option_price_item.setText("")
            option_total_price_item.setText("")
            option_type_item.setText("Call")

    def save_data(self):
        data = {
            'current_price': self.entry_s.text(),
            'risk_free_rate': self.entry_r.text(),
            'dividend_yield': self.entry_q.text(),
            'option_data': []
        }

        for row in range(4):
            quantity_item = self.table_widget.item(row, 0)
            strike_item = self.table_widget.item(row, 1)
            t_item = self.table_widget.item(row, 3)
            sigma_item = self.table_widget.item(row, 4)
            option_type_item = self.table_widget.item(row, 7)

            option_data = {
                'quantity': quantity_item.text(),
                'strike_price': strike_item.text(),
                'time_to_expiry': t_item.text(),
                'volatility': sigma_item.text(),
                'option_type': option_type_item.text()
            }

            data['option_data'].append(option_data)

        self.saved_data = data
        with open('saved_data.json', 'w') as file:
            json.dump(data, file)
        print("Data saved successfully.")

    def load_data(self):
        try:
            with open('saved_data.json', 'r') as file:
                data = json.load(file)
                self.saved_data = data
                self.entry_s.setText(data['current_price'])
                self.entry_r.setText(data['risk_free_rate'])
                self.entry_q.setText(data['dividend_yield'])

                for row, option_data in enumerate(data['option_data']):
                    quantity_item = self.table_widget.item(row, 0)
                    strike_item = self.table_widget.item(row, 1)
                    t_item = self.table_widget.item(row, 3)
                    sigma_item = self.table_widget.item(row, 4)
                    option_type_item = self.table_widget.item(row, 7)

                    quantity_item.setText(option_data['quantity'])
                    strike_item.setText(option_data['strike_price'])
                    t_item.setText(option_data['time_to_expiry'])
                    sigma_item.setText(option_data['volatility'])
                    option_type_item.setText(option_data['option_type'])

                print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")


# Parse command-line arguments to set default values
parser = argparse.ArgumentParser()
parser.add_argument("--current_price", type=float, default=100.0, help="Default current price (S)")
parser.add_argument("--risk_free_rate", type=float, default=0.05, help="Default risk-free rate (r)")
parser.add_argument("--dividend_yield", type=float, default=0.0, help="Default dividend yield (q)")
parser.add_argument("--strike_price", type=float, default=100.0, help="Default strike price (K)")
parser.add_argument("--time_to_expiry", type=float, default=1.0, help="Default time to expiry (t)")
parser.add_argument("--volatility", type=float, default=0.2, help="Default volatility (σ)")
args = parser.parse_args()

# Create the application instance
app = QApplication(sys.argv)

# Create an instance of the BlackScholesCalculator class
default_values = {
    'current_price': args.current_price,
    'risk_free_rate': args.risk_free_rate,
    'dividend_yield': args.dividend_yield,
    'strike_price': args.strike_price,
    'time_to_expiry': args.time_to_expiry,
    'volatility': args.volatility
}
calculator = BlackScholesCalculator(default_values)

# Show the calculator window
calculator.show()

# Start the event loop
sys.exit(app.exec_())
