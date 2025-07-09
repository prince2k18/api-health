from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import aiosqlite

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/add", response_class=HTMLResponse)
async def add(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    async with aiosqlite.connect("data.db") as db:
        await db.execute("INSERT INTO users (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        await db.commit()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "msg": "Successfully Submitted"
    })

@app.get("/view", response_class=HTMLResponse)
async def view_data(request: Request):
    async with aiosqlite.connect("data.db") as db:
        cursor = await db.execute("SELECT name, email, message FROM users")
        rows = await cursor.fetchall()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "msg": "Data Loaded",
        "data": rows
    })
