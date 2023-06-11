## SmartCamp IoT Node - Real-time Data Visualization

This repository contains the source codes used in the SmartCamp IoT project, including both the Arduino and Python scripts. 

### Arduino Script

The Arduino script was used for collecting real-time sensor data from a custom IoT node, including solar voltage, current drawn, temperature, and load status. This data was subsequently sent to a Google Spreadsheet using the ESP32's built-in WiFi capability. 

The Arduino code involves three main steps:
1. Gathering sensor data from the environment.
2. Sending this data wirelessly to the ESP32 microcontroller.
3. Formatting and uploading the data to a Google Spreadsheet.

An important feature of this Arduino script is the ability to handle fluctuating WiFi connections. If the WiFi connection gets interrupted, the ESP32 will attempt to reconnect until a stable connection is established.

### Python Script

This Python script, built with PyQt5 and pyqtgraph, retrieves sensor data from a Google Spreadsheet. The data is displayed in real-time through an interactive GUI, creating a user-friendly way to monitor the status of the SmartCamp IoT node. 

Additionally, the Python script offers the functionality to save the data in CSV format. The saved data can then be used for further analysis, making it a valuable tool for researchers and developers. 

Main functionalities of the Python script:
1. Fetching sensor data from the Google Spreadsheet.
2. Real-time data visualization using pyqtgraph.
3. Saving the displayed data in a CSV file for future analysis.

### Usage

This code was developed as a part of the SmartCamp IoT project, aiming to aid displaced communities in Pakistan by providing sustainable, AI-driven electricity solutions. The data visualized by these scripts directly reflects the performance of the IoT nodes, allowing developers to monitor the effectiveness of the SmartCamp system and make necessary improvements.

### Collaborators

This project was made possible by a collaboration between Coventry University and NUST Pakistan IoT Lab SEECS in a course offered by the former university. The diligent guidance and expertise of Dr. Elena and Dr. Alison significantly contributed to the successful execution of this project.

### Installation & Setup

Detailed installation and setup instructions will guide you through running the scripts on your own system. The instructions include steps for installing necessary libraries and setting up hardware and software environments.

The long description, as well as the short description, provide an inclusive understanding of the codes in the repository, their purpose, usage, and collaborative efforts that made this project possible. Remember to regularly update your README as your project evolves.

**MEDIA**
https://github.com/mahadkhaliq/floodreset/assets/38165958/c1b7d9d3-f8f6-4fa4-b238-272a40e50f6a
https://github.com/mahadkhaliq/floodreset/assets/38165958/a0b21634-c082-4434-891b-219ed8da527c
https://github.com/mahadkhaliq/floodreset/assets/38165958/e7da6cff-728f-4561-acf3-98b2fc1098e9

https://github.com/mahadkhaliq/floodreset/assets/38165958/1383fb9b-1a9d-4277-8227-da11a7dbeeb2
