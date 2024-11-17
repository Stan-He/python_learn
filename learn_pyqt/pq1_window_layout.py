import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


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
"""
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Window Example') # 设置窗口标题

        layout = QVBoxLayout() # 创建一个垂直布局

        label = QLabel('Hello, PyQt5!', self) # 创建一个标签
        layout.addWidget(label)

        self.setLayout(layout) # 设置窗口布局

        self.setGeometry(0, 100, 800, 900) # 设置窗口位置和大小 
        self.move(200,400)

        self.setMaximumSize(800, 800) #设置窗口可以被拖动的最大最小尺寸
        
        self.resize(100, 20) # 强制设置窗口大小
        self.resize(1000, 200)
        

if __name__ == '__main__':
    app = QApplication(sys.argv) # 创建应用程序对象
    window = MyWindow() # 创建窗口对象
    window.show()
    sys.exit(app.exec_())

