import sqlite3
from contextlib import closing
from config import settings

# DB_PATH = './db/securitylogs.db'
VALID_TABLES = {'errors', 'threats', 'warnings'}

def _fetch_table(table: str, limit, offset, filename, since) -> list[dict]:
    if table not in VALID_TABLES:
        raise ValueError(f"Invalid table name: {table}")
    with closing(sqlite3.connect(settings.db_path)) as conn:
        conn.row_factory = sqlite3.Row
        query = f"SELECT * FROM {table} WHERE 1=1 "
        params = []

        if filename:
            query += "AND filename = ?"
            params.append(filename)

        if since:
            query += "AND timestamp >= ?"
            params.append(since)

        query += "LIMIT ? OFFSET ?"
        params += [limit, offset]

        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

def retrieve_all_logs(limit, offset, filename, since):
    return _fetch_table("errors", limit, offset, filename, since)

def retrieve_threat_logs(limit, offset, filename, since):
    return _fetch_table("threats", limit, offset, filename, since)

def retrieve_warning_logs(limit, offset, filename, since):
    return _fetch_table("warnings", limit, offset, filename, since)

if __name__ == "__main__":
    data = retrieve_all_logs()
    print(data)
