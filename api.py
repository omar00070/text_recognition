from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import uvicorn
import cv2
import numpy as np


import cv2
import pytesseract
import numpy as np
import os

# ================================ image recognition
def apply_threshold(img, argument):
    switcher = {
        1: cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        2: cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        3: cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        4: cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        5: cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        6: cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        7: cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
    }
    return switcher.get(argument, "Invalid method")

def crop_image(img, start_x, start_y, end_x, end_y):
    cropped = img[start_y:end_y, start_x:end_x]
    return cropped


def get_string(img, method):

    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

    # Convert to gray
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)
    # img = cv2.erode(img, kernel, iterations=1)

    #  Apply threshold to get image with only black and white
    # img = apply_threshold(img, method)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img, lang="eng")

    return result


if __name__ == "__main__":
    for i in range(1, 8):
        data = get_string('./Spar-Receipt-W.jpeg', 1)
        print(data)



# ==================== app
app = FastAPI()
origins = [
    # "https://unruffled-elion-7e9bda.netlify.app/",
    # "http://localhost:3000",
    # "http://127.0.0.1:3000"
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/api/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    img = file.file.read()
    x = np.fromstring(img, dtype='uint8')
    # decode the array into an image
    img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
    # cv2.imwrite('1.jpeg', img)
    result = get_string(img, 1)
    print(result)
    return {"text": result}

if __name__ == "__main__":
    uvicorn.run("api:app",
                host="0.0.0.0",
                port=8000,
                reload=True
                )