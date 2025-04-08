# src/utils/logger.py
import os
import logging
from datetime import datetime

def setup_logger():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Set up logger with timestamp in filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"logs/game_{timestamp}.log"
    
    # Configure logger
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    return logging.getLogger('game_logger')

# Global logger instance
logger = setup_logger()