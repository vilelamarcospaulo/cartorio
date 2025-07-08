import win32serviceutil
import win32service
import win32event

from watchdog.observers import Observer
from ports.wd import Handler

import logging
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "watchdog_service.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

class WatchdogService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Cartorio"
    _svc_display_name_ = "Cartorio Renomeador de Arquivos"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.observer = Observer()

        logging.info(f'Running by :: {type(Observer())}')
        
        args = list(args)
        if len(args) != 1:
            raise Exception('No path provided') 

        self.path_to_watch = args[1] 
        self.path_to_watch = os.path.abspath(self.path_to_watch)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.observer.stop()
        self.observer.join()

    def SvcDoRun(self):
        logging.info(f"Starting Watchdog Service on {self.path_to_watch}")
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path_to_watch, recursive=True)
        self.observer.start()
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        logging.info("Watchdog Service stopped.")

