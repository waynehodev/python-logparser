LOG ANALYZER -- Last updated (2026-06-24)

PROBLEM STATEMENT: 
- Engineers often spend a significant amount of time manually review large log files to identify failures. This project automates log analysis by detecting error and warning patterns, generating summary reports, accelerating the debugging process.

FEATURES:
- Parse and analyze log files for error and warning patterns.
- Display summary reports of detected errors and warnings.
- Detects potential threats or issues such as:
    - Consecutive errors happening within a short time frame (More than 5 errors within 30 seconds)
- Upload collected errors, warnings and threats into an SQLite DB
- Include unit tests covering core parsing and analysis logic.

INSTALLATION:
```bash
git clone https://github.com/hochuanwei/python-logparser.git
cd python-logparser
pip install -r requirements.txt
```

USAGE:
``` bash
py main.py -f sample.log
```

sample.log:
05/01/2026 00:00:01 EVENT - Running file test_contents.add
05/01/2026 00:13:23 WARNING - File template_output.txt already exists. Overwriting file with new output.
05/01/2026 00:30:45 ERROR - Input data not sufficient to create output. Terminating test.
05/01/2026 00:30:51 ERROR - Return value is 1. Test terminated. Awaiting review.
05/01/2026 00:30:52 ERROR - File unreadable
05/01/2026 00:30:53 ERROR - File unreadable
05/01/2026 00:30:54 ERROR - File unreadable
05/01/2026 00:30:55 ERROR - File unreadable

Expected output:
Running log parser.

------------
Summary
------------

Total line parsed: 8
Total errors: 6
Total warnings: 1

------------
Errors
------------
Error message: Input data not sufficient to create output. Terminating test.
Line number: 3

Error message: Return value is 1. Test terminated. Awaiting review.
Line number: 4

Error message: File unreadable
Line number: 5

Error message: File unreadable
Line number: 6

Error message: File unreadable
Line number: 7

Error message: File unreadable
Line number: 8

------------
Warnings
------------

Warning message: File template_output.txt already exists. Overwritting file with new output.
Line number: 2

Urgent! Many errors detected (8 errors) detected within 30 seconds starting at time 2026-05-01 00:30:51
Uploading to sqlite database
Errors uploaded succesfully
Warnings uploaded succesfully
Threats uploaded succesfully

TESTS:
To run, use the commands:
pip install pytest
py -m pytest tests/

TEST COVERAGE:
Unit tests validate the core parsing and analysis functionality of the application:
- Error detection
- Warning detection
- False positive detection
- Partial log line formatting detection
- Whitespace removal in log lines
- Consecutive errors detection
- Multiple consecutive errors detection

ROADMAP:
- Export analysis results into CSV format
- Web dashboard
