from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import sql

app = FastAPI()
class LogFormat(BaseModel):
    id: int
    timestamp: datetime
    line_number: int
    detail: str
    filename: str

@app.get("/")
def home():
    return {"Status": "Connection successful. Use '/errors' to retrieve errors, '/threats' for threats, and '/warnings' for warnings"}

@app.get("/errors", response_model=list[LogFormat])
def error_logs(limit: int = Query(100, le=1000), offset: int = 0, filename: str | None = None, since: datetime | None = None):
    errors = sql.retrieve_all_logs(limit, offset, filename, since)
    return errors

@app.get("/threats")
def threat_logs(limit: int = Query(100, le=1000), offset: int = 0, filename: str | None = None, since: datetime | None = None):
    errors = sql.retrieve_threat_logs(limit, offset, filename, since)
    return errors

@app.get("/warnings")
def warning_logs(limit: int = Query(100, le=1000), offset: int = 0, filename: str | None = None, since: datetime | None = None):
    errors = sql.retrieve_warning_logs(limit, offset, filename, since)
    return errors
