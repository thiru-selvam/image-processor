from fastapi import FastAPI

from app.database.database import engine
from .routers import img_process
from .database import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Image Processor from CSV')

app.include_router(img_process.router)


@app.get('/')
async def home_url():
    return {'message': 'welcome to image processing'}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
