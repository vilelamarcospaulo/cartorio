from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QWidget, QLineEdit, QPushButton)

import os

class PathSelector(QWidget):
    def __init__(self, on_selected, label_text="Folder:", placeholder="Select a folder to process files from..."):
        super().__init__()

        self.on_selected = on_selected

        layout = QHBoxLayout(self)
        
        # Label
        self.label = QLabel(label_text)
        layout.addWidget(self.label)
        
        # Path input
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(placeholder)
        layout.addWidget(self.path_input)
        
        # Browse butt.n
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)
    
    def browse_folder(self):
        """Open folder dialog"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_input.setText(folder)
            self.on_selected(folder)
    

def scan_path(path, predicate):
    """Scan the selected folder for files"""
    if not path or not os.path.exists(path):
        return

    # Scan for files
    files_found = [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if predicate(os.path.join(root, file))
    ]

    return files_found
