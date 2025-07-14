from PySide6.QtCore import QThread, Signal

import logging
import os, time

from lib import processor

class FileProcessorThread(QThread):
    """Thread to process files without blocking the UI"""
    file_processed = Signal(str)   # Signal when a file is processed
    finished_processing = Signal() # Signal when all processing is done

    # Get the root logger and add our handler
    def __init__(self, files_to_process):
        super().__init__()
        self.files_to_process = files_to_process
        self.is_running = True

    def run(self):
        """Process each file in the list"""
        for file_path in self.files_to_process:
            if not self.is_running:
                break
                
            try:
                self.process_file(file_path)
                self.file_processed.emit(file_path)
                processor.proccess_file(file_path)
                
                # Small delay to simulate processing time
                time.sleep(1)
                
            except Exception as e:
                logging.error(f'Error processing {file_path}: {str(e)}')
        
        self.finished_processing.emit()
    
    def process_file(self, file_path):
        """
        Replace this with your actual file processing function
        This is just a demo that returns file size
        """
        file_size = os.path.getsize(file_path)
        return f"Size: {file_size} bytes"
    
    def stop(self):
        """Stop the processing thread"""
        self.is_running = False
