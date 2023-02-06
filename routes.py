from fastapi import APIRouter, UploadFile, File, Form, Request, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from os import getcwd, remove
from shutil import rmtree
from process import get_results
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from athletes import Athlete

router = APIRouter()
templates = Jinja2Templates(directory='templates')

models.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

athletes = [
    {
        "name": "60m",
        "genre": "male",
        "athletes": [
            {
                "position": 1,
                "name": "Ernesto Martinez Gomez",
                "birthday": "27/05/2004",
                "mark": "7.65",
                "license": "AB13"
            },
            {
                "position": 2,
                "name": "Alvaro De Leon Muñoz",
                "birthday": "17/09/2003",
                "mark": "7.68",
                "license": "AB11"
            },
            {
                "position": 3,
                "name": "David Rosa Torres",
                "birthday": "09/12/1980",
                "mark": "7.95",
                "license": "AB197"
            }
        ]
    },
]

@router.get('/ranking', response_class=HTMLResponse)
def ranking(request: Request):
    context = {'request': request, 'races': athletes}
    return templates.TemplateResponse('index.html', context)

@router.get('/athletes')
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Athlete).all()

@router.post('/athletes')
def create_athlete(athlete: Athlete, db: Session = Depends(get_db)):
    athlete_model = models.Athlete()
    athlete_model.name = athlete.name
    athlete_model.license = athlete.license
    athlete_model.birthday = athlete.birthday
    athlete_model.category = athlete.category

    db.add(athlete_model)
    db.commit()

@router.put('/athletes/{athlete_id}')
def read_api(athlete_id: int, athlete: Athlete, db: Session = Depends(get_db)):
    athlete_model = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()

    if athlete_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'ID {athlete_id} does not exist'
        )

    athlete_model.name = athlete.name
    athlete_model.license = athlete.license
    athlete_model.birthday = athlete.birthday
    athlete_model.category = athlete.category

    db.add(athlete_model)
    db.commit()
    return athlete

@router.delete('/athletes/{athlete_id}')
def read_api(athlete_id: int, db: Session = Depends(get_db)):
    athlete_model = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()

    if athlete_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'ID {athlete_id} does not exist'
        )

    db.query(models.Athlete).filter(models.Athlete.id == athlete_id).delete()
    db.commit()

@router.get('/view_competitions', response_class=HTMLResponse)
def view_competitions(request: Request):
    pdf_list = ['Antequera.pdf', 'control_albacete.pdf', 'GP Valencia.pdf']
    context = {'request': request, 'pdf_list': pdf_list}
    return templates.TemplateResponse('pdf.html', context)

@router.get('/', response_class=HTMLResponse)
def add_competition(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('add.html', context)

@router.post('/')
async def post_competition(file_name: UploadFile = File(), indoor: bool = Form(), localidad: str = Form()):
    with open(getcwd() + '/pdf/' + file_name.filename, 'wb') as myfile:
        content = await file_name.read()
        myfile.write(content)
    results = get_results(getcwd() + '/pdf/' + file_name.filename, indoor)

    return results

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    with open(getcwd() + '/pdf/' + file.filename, 'wb') as myfile:
        content = await file.read()
        myfile.write(content)
    return 'success'

@router.get('/file/{name_file}')
def get_file(name_file: str):
    return FileResponse(getcwd() + '/pdf/' + name_file)

@router.get('/download/{name_file}')
def download_file(name_file: str):
    return FileResponse(getcwd() + '/' + name_file, media_type="aplication/octet-stream", filename=name_file)

@router.delete('/delete/{name_file}')
def delete_file(name_file: str):
    try:
        remove(getcwd() + '/' + name_file)
        return JSONResponse(content={
            'removed': True,
        }, status_code=200)
    except:
        return JSONResponse(content={
            'removed': False,
            'message': 'File not found'
        }, status_code=404)

@router.delete("/folder")
def delete_folder(folder_name: str = Form()):
    rmtree(getcwd() + '/' + folder_name)
    return JSONResponse(content={
        'removed': True,
    }, status_code=200)


