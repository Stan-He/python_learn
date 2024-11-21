import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QPushButton,QHBoxLayout,QGridLayout,QFormLayout


#QWidget 是 PyQt5 中所有用户界面对象的基类。它是一个通用的窗口部件，可以用来创建各种类型的窗口和控件
#笔记：要有QApplication，然后Qwidget->QVBoxLayout->QLabel
"""
setLayout(layout: QLayout): 设置窗口部件的布局管理器。
setWindowTitle(title: str): 设置窗口的标题。
setGeometry(x: int, y: int, width: int, height: int): 设置窗口的位置和大小。 
resize(width: int, height: int): 调整窗口的大小。
move(x: int, y: int): 移动窗口到指定位置。
setFixedSize(width: int, height: int): 设置窗口的固定大小。
setMinimumSize(width: int, height: int): 设置窗口的最小大小。
setMaximumSize(width: int, height: int): 设置窗口的最大大小。
setStyleSheet(styleSheet: str): 设置窗口的样式表，用于自定义窗口的外观。
setWindowIcon(icon: QIcon): 设置窗口的图标。
setToolTip(text: str): 设置窗口部件的工具提示文本。
setStatusTip(text: str): 设置窗口部件的状态栏提示文本。
setCursor(cursor: QCursor): 设置窗口部件的光标形状。
setEnabled(enabled: bool): 启用或禁用窗口部件。
setVisible(visible: bool): 显示或隐藏窗口部件。

QWidget self.setLayout(QVBoxLayout()) #设置窗口部件的布局管理器。
"""
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Window Example') # 设置窗口标题

        #layout = QVBoxLayout() # 创建一个垂直布局
        layout = QHBoxLayout() # 创建一个水平布局
        layout = QGridLayout() # 创建一个表格布局

        label = QLabel('Hello, PyQt5!', self) # 创建一个标签
        layout.addWidget(label,0,0)

        button = QPushButton('Click me', self) 
        layout.addWidget(button,1,1)

        self.setLayout(layout) # 设置窗口布局

        self.setGeometry(0, 100, 800, 900) # 设置窗口位置和大小 
        self.move(200,400)

        self.setMaximumSize(800, 800) #设置窗口可以被拖动的最大最小尺寸
        
        self.resize(100, 20) # 强制设置窗口大小
        self.resize(1000, 200)

        self.setToolTip('This is a QWidget') #鼠标悬停在窗口上时显示的提示信息


        

# if __name__ == '__main__':
#     app = QApplication(sys.argv) # 创建应用程序对象
#     window = MyWindow() # 创建窗口对象
#     window.show()
#     sys.exit(app.exec_())



#堆叠布局---适合与下一步下一步的操作
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QStackedLayout, QPushButton, QVBoxLayout

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('QStackedLayout Example')  # 设置窗口标题
        self.setGeometry(100, 100, 400, 200)  # 设置窗口的位置和大小

        self.stacked_layout = QStackedLayout()  # 创建一个堆叠布局

        page1 = QWidget()
        page1_layout = QVBoxLayout()
        page1_layout.addWidget(QLabel('This is page 1'))
        page1.setLayout(page1_layout)

        page2 = QWidget()
        page2_layout = QVBoxLayout()
        page2_layout.addWidget(QLabel('This is page 2'))
        page2.setLayout(page2_layout)

        self.stacked_layout.addWidget(page1)
        self.stacked_layout.addWidget(page2)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.stacked_layout)

        button = QPushButton('Switch Page')
        button.clicked.connect(self.switch_page)
        main_layout.addWidget(button)

        self.setLayout(main_layout)  # 设置窗口布局

    def switch_page(self):
        current_index = self.stacked_layout.currentIndex()
        next_index = (current_index + 1) % self.stacked_layout.count()
        self.stacked_layout.setCurrentIndex(next_index)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)  # 创建应用程序对象
#     window = MyWindow()  # 创建窗口对象
#     window.show()
#     sys.exit(app.exec_())

#Form布局，一行表示一个标签和输入控件
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QFormLayout

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('QFormLayout Example')  # 设置窗口标题
        self.setGeometry(100, 100, 400, 200)  # 设置窗口的位置和大小

        layout = QFormLayout()  # 创建一个表单布局

        layout.addRow('Name:', QLineEdit())  # 添加一行，包含标签和输入框
        layout.addRow('Age:', QLineEdit())  # 添加一行，包含标签和输入框

        self.setLayout(layout)  # 设置窗口布局

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    window = MyWindow()  # 创建窗口对象
    window.show()
    sys.exit(app.exec_())