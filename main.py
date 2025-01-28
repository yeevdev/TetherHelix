import uvicorn
from api.transaction import router as transaction_router 
from fastapi import FastAPI

app = FastAPI()

app.include_router(transaction_router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
