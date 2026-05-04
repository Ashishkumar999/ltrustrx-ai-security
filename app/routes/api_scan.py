from fastapi import APIRouter
from modules.api_scanner import scan_api

router = APIRouter()

@router.get("/scan/api")
def api_scan(url: str):
    return scan_api(url)
