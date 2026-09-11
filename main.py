import argparse
import log_analyzer.display as display
from log_analyzer import log_parser
from log_analyzer import consecutive_error_check
from database import sqlupload
import logging
from unique_file_path import unique_file_path
from pathlib import Path

def main(filename):
    logger = logging.getLogger("parser")
    LOG_FILE = Path("./parser.log")
    dest = unique_file_path(LOG_FILE)
    logging.basicConfig(filename=dest, level=logging.INFO)
    logger.info("Running log parser.")

    results = log_parser(filename) # Kicks off the script to read and parse the log file into digested return results
    
    # This prints out the captured errors and warnings from the parser
    display.print_summary(results["total_lines"], len(results["error_lines"]), len(results["warning_lines"]))

    # These legacy lines used to print all errors and warnings parsed from the log file and print in the terminal. It has been upgraded to print using the logging function, but deemed unnecessary to print all out in the log file anymore.
    # display.print_errors(results["error_lines"], results["error_linenums"])
    # display.print_warnings(results["warning_lines"], results["warning_linenums"])

    # Checks if there are many errors happening in a row in a short period of time, potentially a security issue (DDoS, multiple failed authentication within a short period of time)
    consecutive_errors_data = consecutive_error_check(results["error_datetime"])
    if consecutive_errors_data is not None:
        for error_count, error_time in zip(consecutive_errors_data["consecutive_error_count"], consecutive_errors_data["consecutive_error_time"]):
            logger.error(f"Urgent! Many errors detected ({error_count} errors) detected within 30 seconds starting at time {error_time}")
    
    logger.info("Uploading to sqlite database")
    sqlupload(results, consecutive_errors_data, filename)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Provide the file name to be parsed"
    )

    parser.add_argument(
        "-f", "--file", metavar="filename",
        required=True, help="the logfile for the parser to look through"
    )

    args = parser.parse_args() # Reads in the filename provided in the args
    main(args.file)