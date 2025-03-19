from PySide6.QtWidgets import (QWidget, QGridLayout, QPushButton, QLineEdit, QLabel, QApplication,
                               QVBoxLayout, QMessageBox)
from PySide6.QtGui import QKeyEvent, QFont
from PySide6.QtCore import Qt
from typing import Callable

class Calculator(QWidget):
    def __init__(self, parent=None):

        self.recent_operations = []
        self.memory = []

        super().__init__(parent)
        self.setWindowTitle('Calculadora')
        self.main_but_box = QGridLayout()
        upper_box = QVBoxLayout()
        self.setLayout(self.main_but_box)
        self.main_but_box.addLayout(upper_box, 0, 1, 1, 4)
        self.line_info = InfoLabel()
        upper_box.addWidget(self.line_info)
        self.line_editor = NumberLine()
        upper_box.addWidget(self.line_editor)

        buttons: dict[str, QPushButton] = {}
        button_number = [[1, 2, 3], 
                         [4, 5, 6], 
                         [7, 8, 9], 
                         [0, '.', 'Del']]
        for x, line in enumerate(button_number, start=2):
            for y, column in enumerate(line, start=1):
                if not column == 'Del':
                    buttons[f'but_{str(column)}'] = self.add_button_layout(str(column), True, x, y)
                else:
                    buttons[f'but_{column}'] = self.add_clear_button('Del', x, y,)
        
        buttons_op: dict[str, QPushButton] = {}
        symbols = ['+', '-', 'x', '÷']
        for xop, op in enumerate(symbols, start=2):
            buttons_op[f'but_{op}'] = self.add_button_layout(op, False, xop, 4)
        
        another_buttons = {
            'but_equal': self.add_special_button( '=', self.equal, 1, 1, 1, 2),
            'but_ac': self.add_special_button('AC', self.clear, 1, 3),
            'but_^': self.add_button_layout('^', False, 1, 4)
        }
        
        for kb, b in buttons.items():
            b.setStyleSheet('font-size: 20px')
            b.setMinimumSize(60, 50)
            print(kb)
        for kb, b in buttons_op.items(): 
            b.setStyleSheet('font-size: 20px; background-color: blue')
            b.setMinimumSize(60, 50)
        for kb, b in another_buttons.items():
            b.setStyleSheet('font-size: 20px; background-color: blue')
            b.setMinimumSize(60, 45)
        self.setFixedSize(300, 380)
        self.adjustSize()

        
    
    def add_button_layout(self, txt: str, is_number: bool, *coordinates: int):
        button = QPushButton(txt)
        if is_number:
            button.clicked.connect(lambda: self.click_number(txt))
        else:
            button.clicked.connect(lambda: self.click_sign(txt))
        self.main_but_box.addWidget(button, *coordinates)
        return button
    

    def add_special_button(self, txt: str, function: Callable, *coordinates):
        button = QPushButton(txt)
        button.clicked.connect(lambda: function())
        self.main_but_box.addWidget(button, *coordinates)
        return button


    def add_clear_button(self, txt, *coordinates):
        button = QPushButton(txt)
        button.clicked.connect(lambda: self.line_editor.clear())
        self.main_but_box.addWidget(button, *coordinates)
        return button


    def click_number(self, number: str):
        if number == '.' and '.' in self.line_editor.text():
            self.show_message(3)
            return
        self.line_editor.insert(number)
    

    def click_sign(self, sign: str):
        is_addsign = True
        if not self.line_editor.text():
            if self.memory:
                if not isinstance(self.memory[-1], (int, float)):
                    print('Ja existe um sinal')
                    self.show_message(2)
                    return
            else:
                print('Você não digitou nada')
                self.show_message(1)
                return
            self.memory.append(sign)
            self.update_text()
            return
        if self.memory and isinstance(self.memory[-1], (int, float)):
            self.memory.append(sign)
            is_addsign = False
        try:
            self.memory.append(int(self.line_editor.text()))
        except:
            self.memory.append(float(self.line_editor.text()))
        finally:
            self.memory.append(sign)
            if len(self.memory) >= 3:
                self.calculate_result(sign, addsign = is_addsign)
            self.update_text()
            self.line_editor.clear()
            print(self.memory)
    

    def calculate_result(self, sign, is_equal = False, addsign = True):
        # self.recent_operations.append(self.memory.copy())
        old_operation = [str(n) for n in self.memory.copy()]
        old_operation.append(' =')
        self.recent_operations.append(old_operation)
        result = self.memory[0]
        if self.memory[1] == '+':
            result += self.memory[2]
        elif self.memory[1] == '-':
            result -= self.memory[2]
        elif self.memory[1] == '÷':
            try:
                result /= self.memory[2]
            except ZeroDivisionError:
                self.show_message(0)
        elif self.memory[1] == 'x':
            result *= self.memory[2]
        elif self.memory[1] == '^':
            result **= self.memory[2]
        self.memory.clear()
        self.memory.append(result)
        self.recent_operations.append(str(result))
        if not is_equal and addsign:
            self.memory.append(sign)
    

    def equal(self):
        if not self.line_editor.text():
            print('espaço em branco')
            self.show_message(1)
            return
        try:
            self.memory.append(int(self.line_editor.text()))
        except:
            self.memory.append(float(self.line_editor.text()))
        finally:
            self.line_editor.clear()
            if len(self.memory) >= 3:
                self.calculate_result(self.memory[1], True)
                self.update_text()
        return
    

    def clear(self):
        self.memory.clear()
        self.line_info.clear()
        self.line_editor.clear()
        return


    def update_text(self):
        new_text = ''
        for t in self.memory:
            new_text += str(t)
        self.line_info.setText(new_text)
    

    def show_message(self, index: int):
        if index == 0:
            QMessageBox.warning(self, 'Erro de Divisão por Zero', 'O Número não pode ser dividido por zero')
        elif index == 1:
            QMessageBox.warning(self, 'Linha Vazia', 'Você não digitou nada')
        elif index == 2:
            QMessageBox.warning(self, 'Sinal já adicionado', 'Você já adicionou um operador à conta')
        elif index == 3:
            QMessageBox.warning(self, 'Ponto já adicionado', 'Você já adicinou um ponto no número')
      

class InfoLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setStyleSheet('font-size: 20px')


class NumberLine(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet('font-size: 25px')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setMinimumHeight(50)
        self.setReadOnly(True)

if __name__ == '__main__':

    app = QApplication()
    calculator_widget = Calculator()
    calculator_widget.show()
    app.exec()
