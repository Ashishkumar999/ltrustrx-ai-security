from fastapi import FastAPI
from app.routes.api_scan import router as api_router
from app.routes.llm_scan import router as llm_router

app = FastAPI()

app.include_router(api_router)
app.include_router(llm_router)

@app.get("/")
def home():
    return {"message": "LtrustRx AI Security Scanner is running 🚀"}
