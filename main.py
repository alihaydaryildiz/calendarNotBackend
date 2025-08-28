from tracemalloc import start
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from database import DBConnection
from eventsModel import Events
from bson import ObjectId
import shutil, os
from fastapi.responses import JSONResponse

DBConnection.initialize()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/endpoint/save_event")
async def create_event(request: Request):
    try:
        data = await request.json()
        print("Gelen veri:", data)
        
        # Dönüştürme işlemi
        event_dict = jsonable_encoder(data)
        print("Mongo'ya eklenecek veri:", event_dict)

        result = DBConnection.insert("events", event_dict)  # ASENKRON OLMADIĞI İÇİN AWAIT YOK

        return {"id": str(result.inserted_id), "message": "Etkinlik eklendi"}
    except Exception as e:
        print("HATA:", e)
        return {"Hata": str(e)}

@app.get("/api/endpoint/eventslist")
async def get_events():
    events = []
    cursor = DBConnection.find("events", {})
    for event in cursor:
        event["_id"] = str(event["_id"])  # ObjectId dönüşümü
        events.append(event)
    return events

@app.delete("/api/endpoint/delete/{event_id}")
async def delete_event(event_id: str):
    try:
        deleted = DBConnection.delete("events", {"_id": ObjectId(event_id)})
        if deleted.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
        return {"message": "Etkinlik başarıyla silindi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")
    
@app.get("/api/endpoint/events-with-file")
async def get_events_with_file():
    events = []
    cursor = DBConnection.find("events", {"file_path": {"$exists": True}})
    for event in cursor:
        event["_id"] = str(event["_id"])
        events.append(event)
    return events



@app.post("/api/endpoint/save-event-file")
async def create_event_file(
    title: str = Form(...),
    start: str = Form(...),
    end: str = Form(...),
    attachment: UploadFile = File(None)
):
    try:
        event_data = {
            "title": title,
            "start": start,
            "end": end,
        }

        if attachment:
            upload_dir = "uploaded_files"
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, attachment.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(attachment.file, buffer)

            event_data["file_path"] = file_path  
        result = DBConnection.insert("events", event_data)

        return JSONResponse(
            status_code=200,
            content={
                "id": str(result.inserted_id),
                "message": "Etkinlik başarıyla kaydedildi" +
                (" ve dosya eklendi" if attachment else "")
            }
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
