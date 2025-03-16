from PySide6.QtWidgets import QMainWindow, QApplication, QToolBar, QListWidget, QMenuBar, QMenu
from PySide6.QtGui import QAction, QIcon
from calc import Calculator

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator_widget = Calculator()
        self.setCentralWidget(self.calculator_widget)

        self.historico = QListWidget()
        self.historico.setStyleSheet('''
                                     font-size: 20px;
                                     item::select::background-color: rgb(40, 237, 0)''') 

        main_tool = QMenuBar()
        file_tool = QMenu('File')
        button_exit = QAction(QIcon('1f4db.png'), 'Sair', self)
        button_exit.triggered.connect(lambda: exit())
        button_historic = QAction(QIcon('1f4c4.png'), 'Histórico', self)
        button_historic.triggered.connect(lambda: self.Show_history())
        main_tool.addMenu(file_tool)
        file_tool.addActions([button_exit, button_historic])
        self.setMenuBar(main_tool)


    def Show_history(self):
        for c in self.calculator_widget.recent_operations:
            self.historico.addItem(str(c))
        self.historico.show()


if __name__ == '__main__':
    app = QApplication()
    app.setWindowIcon(QIcon(r'761194630024790036.png'))
    window = Window()
    window.setWindowTitle('Minha Calculadora')
    window.setWindowIcon(QIcon(r'761194630024790036.png'))
    window.show()
    app.exec()