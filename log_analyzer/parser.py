from datetime import datetime
import logging
logger = logging.getLogger("parser")

def log_parser(filename):
    num = 0 # Line number counter as we continue to read the file
    errorline = [] # List of stored errors detected
    errorlinenum = [] # List of line number where errors are located
    errorlinedatetime = [] # List of the date and time the error are reported at
    warninglinedatetime = [] # List of the date and time the error are reported at
    warningline = [] # List of stored warnings
    warninglinenum = [] # List of line numbers where warnings are located

    try:
        with open(filename, "r") as f:
            for line in f:
                num += 1
                data_line = _line_breakdown(line)

                if data_line == None:
                    continue # Skip lines that doesn't follow the log format

                if str(data_line[1]).lower() == "error": # Stores the error date and time, message, and line number
                    errorlinedatetime.append(data_line[0])
                    errorline.append(data_line[2])
                    errorlinenum.append(num)
                elif str(data_line[1]).lower() == "warning": # Stores the warning message, and line number
                    warninglinedatetime.append(data_line[0])
                    warningline.append(data_line[2])
                    warninglinenum.append(num)
                else:
                    continue

    except FileNotFoundError:
        logger.info(f"File {filename} not found. Please check the file destination.")
        return

    return {
        "total_lines": num,
        "error_lines": errorline,
        "error_linenums": errorlinenum,
        "error_datetime": errorlinedatetime,
        "warning_lines": warningline,
        "warning_linenums": warninglinenum,
        "warning_datetime": warninglinedatetime
    }


def _line_breakdown(line): # Parses the error/warning line and break it down into a list

    try:
        processed_line = line.split("-", 1)
        processed_line[1] = processed_line[1].lstrip()
        processed_line[1] = processed_line[1].rstrip()
        date_time_status_line = processed_line[0].split()

        date_and_time_str = date_time_status_line[0] + " " + date_time_status_line[1]
        date_and_time = datetime.strptime(date_and_time_str, "%m/%d/%Y %H:%M:%S")
        status = date_time_status_line[2]
        message = str(processed_line[1]).strip('\n')

        line_list = [date_and_time, status, message]

        return line_list
    
    except (IndexError, ValueError):
        return None

if __name__ == "__main__":
    import argparse
    logger.info("Runing log parser.")

    parser = argparse.ArgumentParser(
        description="Provide the file name to be parsed"
    )

    parser.add_argument(
        "-f", "--file", metavar="filename",
        required=True, help="the logfile to parse"
    )

    args = parser.parse_args()
    log_parser(args.file)