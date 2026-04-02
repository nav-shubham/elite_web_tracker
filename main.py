from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List
from datetime import datetime
import database
import sqlite3
import csv
import io

class ExercisePayload(BaseModel):
    exercise_name: str
    set_number: int
    reps: int
    weight: float
    duration_seconds: int

class TemplateItem(BaseModel):
    name: str
    targetSets: int

class TemplatePayload(BaseModel):
    exercises: List[TemplateItem]

database.init_db()
app = FastAPI(title="Chronos System Tracker")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def serve_interface(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/api/track")
async def track_session(payload: ExercisePayload):
    current_date = datetime.now().strftime("%Y-%m-%d")
    database.log_session(current_date, payload.exercise_name, payload.set_number, payload.reps, payload.weight, payload.duration_seconds)
    return {"status": "success"}

@app.get("/api/routine/{day_name}")
async def fetch_routine(day_name: str):
    exercises = database.get_template(day_name)
    return {"day": day_name, "exercises": exercises}

@app.post("/api/routine/{day_name}")
async def save_routine(day_name: str, payload: TemplatePayload):
    database.save_template(day_name, [ex.dict() for ex in payload.exercises])
    return {"status": "success"}

@app.get("/api/history")
async def get_history():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT exercise_name, set_number, reps, weight, duration_seconds, timestamp FROM exercise_logs ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    return {"history": [{"split": f"{r[0]} (Set {r[1]}) [{r[2]}x{r[3]}]", "duration": r[4], "timestamp": r[5]} for r in rows]}

@app.delete("/api/history")
async def clear_history():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exercise_logs")
    conn.commit()
    conn.close()
    return {"status": "cleared"}

@app.get("/api/export")
async def export_csv():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT log_date, exercise_name, set_number, reps, weight, duration_seconds, timestamp FROM exercise_logs ORDER BY log_date DESC, timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Exercise Name", "Set Number", "Reps", "Weight", "Duration (Sec)", "Exact Timestamp"])
    for row in rows:
        writer.writerow(row)
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=chronos_analytics.csv"})