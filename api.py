import io
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from text_recognition.tesseract import get_string
import cv2

import numpy as np

app = FastAPI()
origins = [
    "https://unruffled-elion-7e9bda.netlify.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def get_text(item):
    return {"message": "received" }


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    img = file.file.read()
    x = np.fromstring(img, dtype='uint8')
    # decode the array into an image
    img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
    result = get_string(img, 1)
    print(result)
    return {"filename": result}