from fastapi import FastAPI
from router.router import todo_api_router, user_api_router


app = FastAPI()

app.include_router(todo_api_router)
app.include_router(user_api_router)

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI Intern Assesment Project"}
