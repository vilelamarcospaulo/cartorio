import logging

class GuiLogHandler(logging.Handler):
    """Custom logging handler that redirects logs to the GUI"""
    
    def __init__(self, log_signal):
        super().__init__()
        self.log_signal = log_signal
        
        # Set up formatting
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        self.setFormatter(formatter)
    
    def emit(self, record):
        """Emit a log record to the GUI"""
        try:
            msg = self.format(record)

            # Use the signal to send the message to the GUI thread
            self.log_signal.emit(msg)

        except Exception:
            # If something goes wrong, don't crash the application
            pass
