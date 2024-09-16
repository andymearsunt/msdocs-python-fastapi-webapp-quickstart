from fastapi import FastAPI, Form, Request, status, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from typing import List, Optional



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@app.post('/hello', response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    if name:
        print('Request for hello page received with name=%s' % name)
        return templates.TemplateResponse('hello.html', {"request": request, 'name':name})
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)

# Sample data
companies = [
    {"id": 1, "name": "Company One", "address": "123 Main St, City, Country"},
    {"id": 2, "name": "Company Two", "address": "456 Elm St, City, Country"},
    {"id": 3, "name": "Company Three", "address": "789 Oak St, City, Country"},
    {"id": 4, "name": "Company Four", "address": "101 Pine St, City, Country"},
    {"id": 5, "name": "Company Five", "address": "202 Maple St, City, Country"},
]

class Company(BaseModel):
    id: int
    name: str
    address: str

@app.get("/api/v1/companies", response_model=List[Company])
def get_companies():
    return companies

@app.get("/api/v1/companies/{id}", response_model=Company)
def get_company(id: int):
    company = next((company for company in companies if company["id"] == id), None)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.get("/api/v1/companies/{id}/address")
def get_company_address(id: int):
    company = next((company for company in companies if company["id"] == id), None)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"address": company["address"]}

@app.get("/api/v1/companies/summary")
def get_companies_summary():
    summary = [{"id": company["id"], "name": company["name"]} for company in companies]
    return summary

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

