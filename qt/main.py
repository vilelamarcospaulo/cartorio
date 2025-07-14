from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTextEdit)
import sys
import time

import logging

from lib import processor

from qt.logger import GuiLogHandler
from qt.widgets.file import FileListProcessor
from qt.widgets.folder import PathSelector, scan_path

class MainWindow(QMainWindow):
    log_signal = Signal(str)  # Signal to send log messages

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cartorio")
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        self.path_selector = PathSelector(self.load_folder)
        layout.addWidget(self.path_selector)

        self.file_list = FileListProcessor()
        layout.addWidget(self.file_list)

        # Output logger section
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        
        output_header = QHBoxLayout()
        output_header.addWidget(QLabel("Output Log:"))
        # self.clear_log_button = QPushButton("Clear Log")
        # self.clear_log_button.clicked.connect(self.clear_log)
        # output_header.addWidget(self.clear_log_button)
        output_layout.addLayout(output_header)
        
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        output_layout.addWidget(self.output_log)

        layout.addWidget(output_widget)
        
        self.show()
        self.setup_logging()

    def load_folder(self, path):
        files = scan_path(path, processor.should_rename)
        if not files:
            return 

        self.file_list.set_files(files)

    
    def clear_log(self):
        """Clear the output log"""
        self.output_log.clear()
    
    def log_message(self, message):
        """Add a message to the output log"""
        timestamp = time.strftime("%H:%M:%S")
        self.output_log.append(f"[{timestamp}] {message}")
        
        # Auto-scroll to bottom
        scrollbar = self.output_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def closeEvent(self, event):
        """Handle window close event"""
        processing_thread = self.file_list.processing_thread

        if processing_thread and processing_thread.isRunning():
           processing_thread.stop()
           processing_thread.wait()

        event.accept()

    def setup_logging(self):
        """Set up logging to redirect to GUI"""
        # Create a custom log handler that sends logs to the GUI
        self.log_signal.connect(self.log_message)
        self.gui_log_handler = GuiLogHandler(self.log_signal)
        
        # Get the root logger and add our handler
        root_logger = logging.getLogger()
        root_logger.addHandler(self.gui_log_handler)
        root_logger.setLevel(logging.INFO)
        
        # Log a test message
        logging.info("Logging system initialized - all logs will appear in the GUI")

app = QApplication(sys.argv)
window = MainWindow()

app.exec()
