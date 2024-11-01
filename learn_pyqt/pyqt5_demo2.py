import sys
import psutil
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class CPUUsageMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("CPU Usage Monitor")
        self.setGeometry(100, 100, 800, 500)
        self.timer = QTimer()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)

        self.cpu_usage_data = []

        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self.update_cpu_usage)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('CPU Usage (%)')
        self.line, = self.ax.plot([], [], 'r-')

        self.plot = None  # Placeholder for plot widget
        self.timer.start()

    def update_cpu_usage(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_usage_data.append(cpu_usage)
        self.line.set_data(range(len(self.cpu_usage_data)), self.cpu_usage_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
        if len(self.cpu_usage_data) > 60:  # Keep only the last 60 data points
            self.cpu_usage_data.pop(0)

        # Update plot data here if needed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CPUUsageMonitor()
    window.show()
    sys.exit(app.exec_())