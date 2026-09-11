import sqlite3
import logging
logger = logging.getLogger("parser")

def sqlupload(results, consecutive_errors, filename):
    with sqlite3.connect("./db/securitylogs.db") as connection:
        cursor = connection.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS errors(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                timestamp DATETIME NOT NULL,
                line_number INTEGER NOT NULL,
                detail text NOT NULL,
                filename varchar(50) NOT NULL,
                UNIQUE (timestamp, detail, filename)
            );
            
            CREATE TABLE IF NOT EXISTS warnings(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                timestamp DATETIME NOT NULL,
                line_number INTEGER NOT NULL,
                detail text NOT NULL,
                filename varchar(50) NOT NULL,
                UNIQUE (timestamp, detail, filename)
            );

            CREATE TABLE IF NOT EXISTS threats(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                timestamp DATETIME NOT NULL,
                threat varchar(50) NOT NULL,
                detail text NOT NULL,
                filename varchar(50) NOT NULL,
                UNIQUE (timestamp, threat, detail, filename)
            );
        """)
        try:
            for errorline, errorlinenum, errordatetime in zip(results["error_lines"], results["error_linenums"], results["error_datetime"]):
                cursor.execute("""
                    INSERT OR IGNORE INTO errors(timestamp, line_number, detail, filename)
                    VALUES(?, ?, ?, ?)               
                """, (errordatetime, errorlinenum, errorline, filename))
            
            connection.commit()
            logger.info(f"Errors uploaded succesfully")
        except Exception as e:
            connection.rollback()
            logger.info(f"Failed upload: {e}")

        try:
            for warningline, warninglinenum, warningdatetime in zip(results["warning_lines"], results["warning_linenums"], results["warning_datetime"]):
                cursor.execute("""
                    INSERT OR IGNORE INTO warnings(timestamp, line_number, detail, filename)
                    VALUES(?, ?, ?, ?)               
                """, (warningdatetime, warninglinenum, warningline, filename))
            
            connection.commit()
            logger.info(f"Warnings uploaded succesfully")
        except Exception as e:
            connection.rollback()
            logger.info(f"Failed upload: {e}")

        try:
            for errorcount, errortime, in zip(consecutive_errors["consecutive_error_count"], consecutive_errors["consecutive_error_time"]):
                errortext = f"A total of {errorcount} errors happened within 30 seconds starting here."
                # print(errorcount)
                # print(errortime)
                # print(errortext)
                cursor.execute("""
                    INSERT OR IGNORE INTO threats(timestamp, threat, detail, filename)
                    VALUES(?, ?, ?, ?)
                """, (errortime, "excessive_errors_in_short_time", errortext, filename))
            
            connection.commit()
            logger.info(f"Threats uploaded succesfully")
        except Exception as e:
            connection.rollback()
            logger.info(f"Failed upload: {e}")
