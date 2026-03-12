from fastapi import APIRouter

router = APIRouter(
    prefix="/media",
    tags=['media'],
    responses={404: {"description": "Not found"}}
)