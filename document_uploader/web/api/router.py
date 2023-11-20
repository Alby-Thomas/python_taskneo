from fastapi import APIRouter, FastAPI

from document_uploader.web.api import document, monitoring, user

app = FastAPI()

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(user.router)  # Include the user router
api_router.include_router(document.router)  # Include the document router

app.include_router(api_router, prefix="/api")
