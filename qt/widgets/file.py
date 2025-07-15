from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QPushButton, QProgressBar, QWidget)
from PySide6.QtCore import Qt

import logging

from qt.processor import FileProcessorThread

class FileListProcessor(QWidget):

    # TODO :: RECEIVE THE PROCESS EACH FILE FN
    def __init__(self):
        super().__init__()

        self.files = []

        file_layout = QVBoxLayout(self)
        
        file_header = QHBoxLayout()
        file_header.addWidget(QLabel("Files to Process:"))

        self.file_count_label = QLabel("0 files")
        file_header.addWidget(self.file_count_label)
        file_layout.addLayout(file_header)
        
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_list)

        # Control buttons
        button_layout = QHBoxLayout()
        self.process_button = QPushButton("Process Files")
        self.process_button.clicked.connect(self.process_files)
        self.process_button.setEnabled(False)
        button_layout.addWidget(self.process_button)
        
        file_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        file_layout.addWidget(self.progress_bar)
        
    def set_files(self, files: list[str]):
        self.files = files

        self.file_list.clear()
        self.file_list.addItems(sorted(files))
        self._redraw()

    def remove_file(self, file: str):
        self.files.remove(file)

        items = self.file_list.findItems(file, Qt.MatchFlag.MatchExactly)
        for item in items:
            row = self.file_list.row(item)
            self.file_list.takeItem(row)

    def process_files(self):
        self.progress_bar.setMaximum(len(self.files))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.processed_files = 0

        self.process_button.setEnabled(False)

        self.processing_thread = FileProcessorThread(self.files)
        self.processing_thread.file_processed.connect(self.on_file_processed)
        self.processing_thread.finished_processing.connect(self.on_processing_finished)
        self.processing_thread.start()

        pass


    def on_file_processed(self, file):
        self.processed_files += 1
        self.progress_bar.setValue(self.processed_files)

        self.remove_file(file)


    def on_processing_finished(self):
        logging.info(f"Processing completed! Processed {self.processed_files} files.")
        if self.processing_thread:
            self.processing_thread.wait()
            self.processing_thread = None

        self._redraw()

    def _redraw(self):
        self.file_count_label.setText(f"{len(self.files)} files")


        self.progress_bar.setVisible(False)
        self.process_button.setEnabled(len(self.files) > 0)

