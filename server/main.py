from fastapi import FastAPI
import uvicorn

from auth.routes import auth_router
from pdf.routes import pdfRouter
from chat.routes import chatRouter

app = FastAPI()

app.include_router(auth_router)
app.include_router(pdfRouter)
app.include_router(chatRouter)

@app.get("/")
async def index():
    return {"message": "hello world"}

if __name__ == '__main__':
    uvicorn.run(port=8000)