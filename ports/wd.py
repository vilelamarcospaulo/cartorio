from lib.processor import proccess_file

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 

import logging
import os
import time

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        proccess_file(event.src_path)

class WatchdogRunner:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.observer = Observer()
        logging.info(f'Running by :: {type(self.observer)}')  

    def start(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        logging.info(f"Watching: {self.path}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
