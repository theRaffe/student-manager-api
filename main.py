
from fastapi import FastAPI
from routers import student_router, teacher_router

app = FastAPI()
app.include_router(student_router.router)
app.include_router(teacher_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
