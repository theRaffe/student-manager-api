
from fastapi import FastAPI
from routers import student_router, teacher_router, catalog_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    expose_headers=["*"],
    # https://stackoverflow.com/questions/65635346/how-can-i-enable-cors-in-fastapi
    allow_methods=['*'], allow_headers=['*']

)

app.include_router(student_router.router)
app.include_router(teacher_router.router)
app.include_router(catalog_router.router)



@app.get("/")
async def root():
    return {"message": "Hello, Student Manager"}
