from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LtrustRx AI Security Scanner is running 🚀"}
