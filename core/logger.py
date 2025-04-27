import logging
import os
import sys
from datetime import datetime

# Determine the directory of the executable (or script)
if getattr(sys, 'frozen', False):  # Running as a PyInstaller executable
    # Use the directory where the .exe is located
    base_dir = os.path.dirname(sys.executable)
else:
    # Use the directory of the script (for development)
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Set the log directory relative to the base directory
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

# Name the log file with the current date
log_file = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Set up the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file, encoding="utf-8")]
)

logger = logging.getLogger("WinFixerLogger")

# Simple function to log messages
def log(message, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)