from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
import logging

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()
logger = logging.getLogger("uvicorn.error")

def unique_file_path(dest: Path) -> Path:
    if not dest.exists():
        return dest

    stem, suffix, parent = dest.stem, dest.suffix, dest.parent
    counter = 1

    while True:
        new_dest = parent / f"{stem}_{counter}{suffix}"
        if not new_dest.exists():
            return new_dest
        counter += 1

@app.get("/")
def home():
    return {"Status": "Test Upload File"}

@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    logger.info(f"Upload started: {file.filename}")
    dest = unique_file_path(UPLOAD_DIR / file.filename)

    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        logger.info(f"Upload to {str(dest)}")

    return {"filename": file.filename, 
            "saved_to": str(dest)
    }
    