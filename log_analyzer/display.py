import logging
logger = logging.getLogger("parser")

def print_summary(linenum, totalerrornum, totalwarningnum): # Prints a summary of total errors and warnings detected
    logger.info(f"------------Summary------------")
    logger.info(f"Total line parsed: {linenum}")
    logger.info(f"Total errors: {totalerrornum}")
    logger.info(f"Total warnings: {totalwarningnum}")

def print_errors(errorline, errorlinenum): # Prints out the errors detected
    logger.info("------------Errors------------")
    for line, num in zip(errorline, errorlinenum):
        logger.info(f"Error message: {line}\nLine number: {num}")

def print_warnings(warningline, warninglinenum): # Prints out the warnings detected
    logger.info("------------Warnings------------")
    for line, num in zip(warningline, warninglinenum):
        logger.info(f"Warning message: {line}\nLine number: {num}")