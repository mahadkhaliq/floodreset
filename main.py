import sys
import pandas as pd
import numpy as np
import pytz
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import datetime

# Custom AxisItem to handle the conversion from timestamp to string
class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        timezone = pytz.timezone('Asia/Karachi')
        labels = [timezone.localize(datetime.datetime.fromtimestamp(value)).strftime('%H:%M:%S') for value in values]
        labels = [datetime.datetime.strptime(label, '%H:%M:%S') - datetime.timedelta(hours=5) for label in labels]
        return [label.strftime('%H:%M:%S') for label in labels]

class ApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartCamp")
        self.setStyleSheet("background-color: #111111;")  # Darker background color
        self.data = pd.DataFrame()

        self.layout = QVBoxLayout(self)

        # Graphs setup
        self.graphs = {}
        self.colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]  # Contrasting colors
        for i, column in enumerate(["solar_voltage", "current_drawn", "temperature", "load_status"]):
            self.graphs[column] = pg.PlotWidget(background='k', axisItems={'bottom': TimeAxisItem(orientation='bottom')})
            self.graphs[column].setBackground('#222222')  # Darker background color for the graph
            self.graphs[column].setTitle(column.replace("_", " ").title(), color='w', size='20pt')
            self.graphs[column].setLabel('left', column[1], color='white', size='16pt')
            self.graphs[column].setLabel('bottom', 'Time', color='white', size='16pt')
            self.graphs[column].showGrid(x=True, y=True)
            self.graphs[column].setBackground('k')
            self.graphs[column].getAxis('left').setPen(pg.mkPen(color='w'))  # Set axis color to white
            self.graphs[column].getAxis('bottom').setPen(pg.mkPen(color='w'))  # Set axis color to white
            self.graphs[column].getAxis('left').setTextPen(pg.mkPen(color='w'))  # Set axis label color to white
            self.graphs[column].getAxis('bottom').setTextPen(pg.mkPen(color='w'))  # Set axis label color to white
            self.graphs[column].getPlotItem().getAxis('bottom').setStyle(tickTextOffset=12)  # Adjust tick text offset
            self.graphs[column].plotItem.getAxis('left').enableAutoSIPrefix(False)  # Disable automatic SI prefix scaling
            self.graphs[column].plotItem.getAxis('bottom').enableAutoSIPrefix(False)  # Disable automatic SI prefix scaling
            self.graphs[column].plotItem.showGrid(x=True, y=True, alpha=0.3)  # Adjust grid alpha
            self.graphs[column].plotItem.setTitle(color='w', size='16pt')  # Set title color and size
            self.graphs[column].plotItem.setLabel(axis='left', text=column, color='w', size='16pt')  # Set left axis label color and size
            self.graphs[column].plotItem.setLabel(axis='bottom', text='Time', color='w', size='16pt')  # Set bottom axis label color and size
            self.layout.addWidget(self.graphs[column])

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_refresh = QPushButton("Refresh")
        self.button_refresh.setFixedSize(100, 50)
        self.button_refresh.setStyleSheet("background-color: darkgreen; color: white; font-size: 18px;")
        self.button_refresh.clicked.connect(self.update_data)
        self.button_layout.addWidget(self.button_refresh)

        self.button_save = QPushButton("Save")
        self.button_save.setFixedSize(100, 50)
        self.button_save.setStyleSheet("background-color: darkblue; color: white; font-size: 18px;")
        self.button_save.clicked.connect(self.save_data)
        self.button_layout.addWidget(self.button_save)

        self.layout.addLayout(self.button_layout)

        self.update_data()

    def update_data(self):
        sheet_url = "https://docs.google.com/spreadsheets/d/1Q-XrfVgUEJAknRpV3xeVY5qc7lZRXkOOwUFCbYRNYas/edit#gid=0"
        url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
        self.data = pd.read_csv(url_1)
        self.data['datetime'] = pd.to_datetime(self.data['datetime'], format='%d/%m/%Y %H:%M:%S')
        self.data['time'] = [t.timestamp() for t in self.data['datetime']]

        # Replace non-numeric values in the current_drawn column with np.nan
        self.data['current_drawn'] = pd.to_numeric(self.data['current_drawn'], errors='coerce')

        for i, column in enumerate(["solar_voltage", "current_drawn", "temperature", "load_status"]):
            if column in self.data.columns:
                self.graphs[column].clear()
                self.graphs[column].plot(self.data['time'], self.data[column], pen=pg.mkPen(color=self.colors[i], width=2))
                self.graphs[column].plotItem.setLabel('left', text=column.replace("_", " ").title(), color='w', size='16pt')  # Set left axis label

    def save_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv)")
        if file_path:
            if not file_path.endswith(".csv"):
                file_path += ".csv"

            # Check if the file already exists
            file_exists = False
            try:
                existing_data = pd.read_csv(file_path)
                file_exists = True
            except FileNotFoundError:
                pass

            # Append or save the data accordingly
            if file_exists:
                combined_data = pd.concat([existing_data, self.data], ignore_index=True)
                combined_data.to_csv(file_path, index=False)
            else:
                self.data.to_csv(file_path, index=False)

if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    sys.exit(qapp.exec_())

