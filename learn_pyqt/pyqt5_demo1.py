import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
import math
from PyQt5.QtWidgets import QMessageBox

class Calculator(QMainWindow):
    def about(self):
        QMessageBox.about(self, "About Scientific Calculator", "Version 1.0")
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scientific Calculator')
        self.setGeometry(100, 100, 400, 400)
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

        self.buttons = QGridLayout()
        self.layout.addLayout(self.buttons)

        buttons = [
            '7', '8', '9', '/', 'sqrt',
            '4', '5', '6', '*', 'pow',
            '1', '2', '3', '-', 'log',
            '0', '.', '=', '+', 'sin',
            'cos', 'tan', '(', ')', 'C'
        ]

        row, col = 0, 0
        for button in buttons:
            self.addButton(button, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def addButton(self, text, row, col):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.onButtonClick(text))
        self.buttons.addWidget(button, row, col)

    def onButtonClick(self, text):
        if text == 'C':
            self.display.clear()
        elif text == '=':
            try:
                expression = self.display.text()
                result = eval(expression)
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText('Error')
        elif text in ['sqrt', 'pow', 'log', 'sin', 'cos', 'tan']:
            self.display.setText(self.display.text() + 'math.' + text + '(')
        else:
            self.display.setText(self.display.text() + text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())