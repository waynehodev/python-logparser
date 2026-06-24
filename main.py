import argparse
import log_analyzer.display as display
from log_analyzer import log_parser
from log_analyzer import consecutive_error_check
from database import sqlupload


if __name__ == "__main__":
    print("\nRunning log parser.")

    parser = argparse.ArgumentParser(
        description="Provide the file name to be parsed"
    )

    parser.add_argument(
        "-f", "--file", metavar="filename",
        required=True, help="the logfile for the parser to look through"
    )

    args = parser.parse_args() # Reads in the filename provided in the args
    results = log_parser(args.file) # Kicks off the script to read and parse the log file into digested return results
    
    # This prints out the captured errors and warnings from the parser
    display.print_summary(results["total_lines"], len(results["error_lines"]), len(results["warning_lines"]))
    display.print_errors(results["error_lines"], results["error_linenums"])
    display.print_warnings(results["warning_lines"], results["warning_linenums"])

    # Checks if there are many errors happening in a row in a short period of time, potentially a security issue (DDoS, multiple failed authentication within a short period of time)
    consecutive_errors_data = consecutive_error_check(results["error_datetime"])
    if consecutive_errors_data is not None:
        for error_count, error_time in zip(consecutive_errors_data["consecutive_error_count"], consecutive_errors_data["consecutive_error_time"]):
            print(f"Urgent! Many errors detected ({error_count} errors) detected within 30 seconds starting at time {error_time}")
    
    print("Uploading to sqlite database")
    sqlupload(results, consecutive_errors_data, args.file)