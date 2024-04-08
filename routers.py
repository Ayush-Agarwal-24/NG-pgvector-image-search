from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_db_connection
from imgbeddings import imgbeddings
from PIL import Image
from typing import List
import cv2
import numpy as np
from fastapi.responses import RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="templates")
conn = get_db_connection()
cursor = conn.cursor()


@router.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})


@router.post("/upload_input_data")
def upload_input_data(files: List[UploadFile] = File(...)):
    try:
        for file in files:
            image_path = f"static/images/{file.filename}"
            with open(image_path, "wb") as buffer:
                buffer.write(file.file.read())

            img = Image.open(image_path)
            ibed = imgbeddings()
            embedding = ibed.to_embeddings(img)[0]

            cursor.execute('INSERT INTO image_search(image_name, embeddings) values (%s,%s)',
                           (file.filename, embedding.tolist()))
            conn.commit()
        return RedirectResponse(url=f"/?message=Dataset%20Uploaded%20Successfully",
                                status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/search_embedding")
def search_embedding(request: Request, file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    try:
        alg = "haarcascade_frontalface_default.xml"
        haar_cascade = cv2.CascadeClassifier(alg)
        contents = file.file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        faces = haar_cascade.detectMultiScale(img, scaleFactor=1.05, minNeighbors=2, minSize=(100, 100))
        for x, y, w, h in faces:
            cropped_image = img[y: y + h, x: x + w]
            ibed = imgbeddings()
            cropped_image = Image.fromarray(cropped_image, mode='L')
            img_embedding = ibed.to_embeddings(cropped_image)

        string_rep = "".join(str(x) for x in img_embedding.tolist())
        cursor.execute("SELECT image_name FROM image_search ORDER BY embeddings <-> %s LIMIT 5;",
                       (string_rep,))
        results = cursor.fetchall()
        conn.commit()
        if len(results) > 0:
            return templates.TemplateResponse("search_results.html", {"request": request, "results": results})
        else:
            return templates.TemplateResponse("no_results.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
