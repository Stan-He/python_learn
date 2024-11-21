# 基本控件
# QWidget：所有窗口部件的基类。
# QLabel：用于显示文本或图像的标签。 --> layout.addWidget
# QPushButton：按钮控件。
# QLineEdit：单行文本输入框。
# QTextEdit：多行文本输入框。
# QComboBox：下拉列表框。
# QCheckBox：复选框。
# QRadioButton：单选按钮。
# QSlider：滑动条。
# QProgressBar：进度条。
# 容器控件
# QMainWindow：主窗口，包含菜单栏、工具栏、状态栏等。
# QDialog：对话框窗口。
# QGroupBox：分组框，用于将多个控件分组。
# QTabWidget：选项卡控件。
# QStackedWidget：堆叠窗口部件，每次只显示一个子窗口部件。
# QScrollArea：滚动区域，用于显示超出窗口大小的内容。
# 布局管理器
# QVBoxLayout：垂直布局，将窗口部件从上到下垂直排列。
# QHBoxLayout：水平布局，将窗口部件从左到右水平排列。
# QGridLayout：网格布局，将窗口部件按网格排列。
# QFormLayout：表单布局，每一行包含一个标签和一个输入控件。
# 高级控件
# QTreeView：树视图控件，用于显示分层数据。
# QTableView：表视图控件，用于显示表格数据。
# QListView：列表视图控件，用于显示列表数据。
# QCalendarWidget：日历控件。
# QDateEdit：日期编辑控件。
# QTimeEdit：时间编辑控件。
# QDateTimeEdit：日期时间编辑控件。

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,QLineEdit
from PyQt5.QtGui import QIcon,QPixmap,QImage

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Widgets Example')
        self.setGeometry(100, 100, 400, 300)
        img = QImage('/home/starblaze/Desktop/python_learn/learn_pyqt/orange_button.png')
        pixmap = QPixmap.fromImage(img)
        self.setWindowIcon(QIcon(pixmap)) #设置窗状态栏图标

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        label = QLabel('Hello, PyQt5!', self)
        label1 = QLabel('Hello1, PyQt5!', self)
        label2 = QLabel('Hello2, PyQt5!', self)
        button = QPushButton('Click Me', self)
        button.setIcon(QIcon(pixmap))

        linedit = QLineEdit('', self)
        linedit.setPlaceholderText('type in your name again..')


        layout.addWidget(label)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(button)
        layout.addWidget(linedit)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())