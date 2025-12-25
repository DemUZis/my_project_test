from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.dependencies import get_current_user
from app.schemes.user import UserInDB


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "current_user": current_user})


@router.get("/services", response_class=HTMLResponse)
async def services(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("services.html", {"request": request, "current_user": current_user})


@router.get("/masters", response_class=HTMLResponse)
async def masters(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("masters.html", {"request": request, "current_user": current_user})


@router.get("/booking", response_class=HTMLResponse)
async def booking(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("booking.html", {"request": request, "current_user": current_user})


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "current_user": current_user})


@router.get("/my-appointments", response_class=HTMLResponse)
async def my_appointments(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("my-appointments.html", {"request": request, "current_user": current_user})


@router.get("/master-schedule", response_class=HTMLResponse)
async def master_schedule(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("master-schedule.html", {"request": request, "current_user": current_user})


@router.get("/master-appointments", response_class=HTMLResponse)
async def master_appointments(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("master-appointments.html", {"request": request, "current_user": current_user})


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, current_user: UserInDB = Depends(get_current_user)):
    return templates.TemplateResponse("admin-dashboard.html", {"request": request, "current_user": current_user})