from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
import logging
# from log_analyzer import log_parser, consecutive_error_check, display
from main import main
from unique_file_path import unique_file_path

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()
logger = logging.getLogger("uvicorn.error")

# def unique_file_path(dest: Path) -> Path:
#     if not dest.exists():
#         return dest

#     stem, suffix, parent = dest.stem, dest.suffix, dest.parent
#     counter = 1

#     while True:
#         new_dest = parent / f"{stem}_{counter}{suffix}"
#         if not new_dest.exists():
#             return new_dest
#         counter += 1

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

    logger.info(f"Starting log parsing")
    main(str(dest))

    return {"filename": file.filename, 
            "saved_to": str(dest)
    }
    