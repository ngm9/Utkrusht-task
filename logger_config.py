import logging

# Set up logging configuration
LOGFILE = "agent_task_creator.log"

def setup_logger(name="infra_assessor"):
    """Create and configure a logger instance that can be imported by other modules."""
    logger = logging.getLogger(name)
    
    # Only add handlers if they haven't been added already
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create formatters
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler(LOGFILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

# Create the main logger instance
logger = setup_logger()

# Export the logger and setup function for use in other modules
__all__ = ['logger', 'setup_logger']
