from PySide6.QtWidgets import (QWidget, QGridLayout, QPushButton, QLineEdit, QLabel, QApplication,
                               QVBoxLayout, QMenu)
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt
from typing import Callable

class Calculator(QWidget):
    def __init__(self, parent=None):

        self.recent_operations = []
        self.memory = []

        super().__init__(parent)
        self.setWindowTitle('Calculadora')
        main_but_box = QGridLayout()
        upper_box = QVBoxLayout()
        self.setLayout(main_but_box)
        main_but_box.addLayout(upper_box, 0, 1, 1, 4)
        line_info = QLabel()
        line_info.setAlignment(Qt.AlignmentFlag(2))
        line_info.setStyleSheet('font-size: 25px')
        upper_box.addWidget(line_info)
        line_editor = QLineEdit()
        line_editor.setStyleSheet('font-size: 25px')
        line_editor.setAlignment(Qt.AlignmentFlag(2))
        line_editor.setReadOnly(True)
        upper_box.addWidget(line_editor)

        buttons: dict[str, QPushButton] = {}
        button_number = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, '.', 'Del']]
        for x, line in enumerate(button_number, start=2):
            for y, column in enumerate(line, start=1):
                buttons[f'but_{x, y}'] = self.add_button_layout(main_but_box, line_editor, line_info, str(column), True, x, y)
                if column == 'Del':
                    buttons[f'but_{x, y}'] = self.add_clear_button(main_but_box, line_editor, 'Del', x, y)
        
        buttons_op: dict[str, QPushButton] = {}
        symbols = ['+', '-', 'x', '÷']
        for xop, op in enumerate(symbols, start=2):
            buttons_op[f'but_{op}'] = self.add_button_layout(main_but_box, line_editor, line_info, op, False, xop, 4)
        
        special_buttons = {
            'but_equal': self.add_special_button(main_but_box, line_editor, line_info, '=', self.equal, 1, 1, 1, 2),
            'but_ac': self.add_special_button(main_but_box, line_editor, line_info, 'AC', self.clear, 1, 3, 1, 2)
        }
        
        for kb, b in buttons.items():
            b.setStyleSheet('font-size: 20px')
            print(kb)
        for kb, b in buttons_op.items(): 
            b.setStyleSheet('font-size: 20px; background-color: #0000f7')
            print(kb)
        for kb, b in special_buttons.items():
            b.setStyleSheet('font-size: 20px; background-color: #0000f7')
            print(kb)
        
    
    def add_button_layout(self, layout: QGridLayout, line_editor: QLineEdit, line_fix: QLabel, 
                          txt: str, is_number: bool, *coordinates: int):
        button = QPushButton(txt)
        if is_number:
            button.clicked.connect(lambda: self.click_number(line_editor, txt))
        else:
            button.clicked.connect(lambda: self.click_sign(line_editor, line_fix, txt))
        layout.addWidget(button, *coordinates)
        return button
    

    def add_special_button(self, layout: QGridLayout, line_editor: QLineEdit, line_fix: QLabel, 
                           txt: str, function: Callable, *coordinates):
        button = QPushButton(txt)
        args = [line_fix, line_editor]
        button.clicked.connect(lambda: function(*args))
        layout.addWidget(button, *coordinates)
        return button


    def add_clear_button(self, layout: QGridLayout, line_editor: QLineEdit, txt, *coordinates):
        button = QPushButton(txt)
        button.clicked.connect(lambda: line_editor.clear())
        layout.addWidget(button, *coordinates)
        return button


    def click_number(self, line: QLineEdit, number: str):
        line.insert(number)
    

    def click_sign(self, line: QLineEdit, line_fix: QLabel, sign: str):
        is_addsign = True
        if not line.text():
            if self.memory:
                if not isinstance(self.memory[-1], (int, float)):
                    print('Ja existe um sinal')
                    return
            else:
                print('Você não digitou nada')
                return
            self.memory.append(sign)
            self.update_text(line_fix)
            return
        if self.memory and isinstance(self.memory[-1], (int, float)):
            self.memory.append(sign)
            is_addsign = False
        try:
            self.memory.append(int(line.text()))
        except:
            self.memory.append(float(line.text()))
        finally:
            self.memory.append(sign)
            if len(self.memory) >= 3:
                self.calcalate(sign, addsign = is_addsign)
            self.update_text(line_fix)
            line.clear()
            print(self.memory)
    

    def calcalate(self, sign, is_equal = False, addsign = True):
        self.recent_operations.append(self.memory.copy())
        result = self.memory[0]
        if self.memory[1] == '+':
            result += self.memory[2]
        elif self.memory[1] == '-':
            result -= self.memory[2]
        elif self.memory[1] == '÷':
            result /= self.memory[2]
        elif self.memory[1] == 'x':
            result *= self.memory[2]
        self.memory.clear()
        self.memory.append(result)
        self.recent_operations.append(result)
        if not is_equal and addsign:
            self.memory.append(sign)
    

    def equal(self, line_fix: QLabel, line: QLineEdit):
        if not line.text():
            print('espaço em branco')
            return
        try:
            self.memory.append(int(line.text()))
        except:
            self.memory.append(float(line.text()))
        finally:
            line.clear()
            if len(self.memory) >= 3:
                self.calcalate(self.memory[1], True)
                self.update_text(line_fix)
        return
    

    def clear(self, line_fix: QLabel, line: QLineEdit):
        self.memory.clear()
        line_fix.clear()
        line.clear()
        return


    def update_text(self, line_fix: QLabel):
        new_text = ''
        for t in self.memory:
            new_text += str(t)
        line_fix.setText(new_text)
        
if __name__ == '__main__':

    app = QApplication()
    calculator_widget = Calculator()
    calculator_widget.show()
    app.exec()
