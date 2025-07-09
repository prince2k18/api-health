from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import monitor

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    data = await monitor.check_all_apis()
    return templates.TemplateResponse("dashboard.html", {"request": request, "results": data})

@app.post("/add", response_class=HTMLResponse)
async def add_api(request: Request, url: str = Form(...)):
    await monitor.add_api(url)
    data = await monitor.check_all_apis()
    return templates.TemplateResponse("dashboard.html", {"request": request, "results": data})
