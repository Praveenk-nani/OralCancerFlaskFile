from fastapi import FastAPI,File,UploadFile
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware
import cv2
import logging


app = FastAPI(timeout = 600)



logging.basicConfig(level=logging.INFO)



origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:3000",
    "http://localhost:3000"
],  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

MODEL =  tf.keras.models.load_model("OralCancerModel.keras") # type: ignore
CLASSES = ["Normal","OSCC"]


@app.get("/")
async def hello():
    return {"hello":"Praveenkumar"}


def read_image(data)->list:
    try:
        image = np.array(Image.open(BytesIO(data)))
        new_img = cv2.resize(image,(224,224))

        return [new_img,False]
    except Exception as e:
        return [e,True]


@app.post("/predictions")
async def predict(file:UploadFile=File(...)):
    try:
        bytes = await file.read()
        img = read_image(bytes)
        logging.info(f"image file was received {file.filename}")
        if img[1]:
            logging.info(f"error has been occurred while converting the image")
            return {"Result":f"Error {img[0]}",
                    "Accuracy":"image not supported"}
        else:
            img_batch = np.expand_dims(img[0],0)
            result_list = []

            prediction = MODEL.predict(img_batch)
            confidence = np.argmax(prediction)
            result = CLASSES[confidence]
            result_list = [result,str(prediction[0][confidence])]
            logging.info(f"prediction was successful")
            return {"Result":result_list[0],
                    "Accuracy":result_list[1]}
        # return {"Result":"successfully opened",
        #         "Accuracy":file.filename}
    except Exception as e:
        return {"Result":"Error",
                "Accuracy":e}