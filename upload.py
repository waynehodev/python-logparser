from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

@app.get("/")
def home():
    return {"Status": "Test Upload File"}

@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    dest = UPLOAD_DIR / file.filename
    print("Opening file")

    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        print("copy done")

    return {"filename": file.filename, 
            "saved_to": str(dest)
    }
    # contents = await file.read()
    # return {
    #     "filename": file.filename,
    #     "content_type": file.content_type,
    #     "size": len(contents),
    # }
    