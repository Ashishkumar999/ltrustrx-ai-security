from fastapi import APIRouter
from modules.llm_tester import scan_llm

router = APIRouter()

@router.get("/scan/llm")
def llm_scan():
    return scan_llm()
