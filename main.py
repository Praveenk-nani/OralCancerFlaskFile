from fastapi import FastAPI,File,UploadFile
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

MODEL =  tf.keras.models.load_model("OralCancerModel.keras") # type: ignore
CLASSES = ["Normal","OSCC"]


@app.get("/")
async def hello():
    return {"hello":"Praveenkumar"}


def read_image(data)->np.ndarray:
    try:
        image = np.array(Image.open(BytesIO(data)))
        return image
    except Exception as e:
        return np.array(e)


@app.post("/predictions")
async def predict(file:UploadFile=File(...)):
    try:
        bytes = await file.read()
        img = read_image(bytes)
        img_batch = np.expand_dims(img,0)
        result_list = []

        prediction = MODEL.predict(img_batch)
        confidence = np.argmax(prediction)
        result = CLASSES[confidence]
        result_list = [result,str(prediction[0][confidence])]
        return {"Result":result_list[0],
                "Accuracy":result_list[1]}
    except:
        return {"Result":"Error",
                "Accuracy":"Error"}