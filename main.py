from fastapi import FastAPI
from old_routes import auth_routers
from routes import fastapi_auth_routes
from fastapi.routing import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi.exceptions import HTTPException
import uvicorn

app = FastAPI()

# # Добавить функционал очистки БД
# @app.on_event('startup')
# def start_up():
#     pass

# app.include_router(auth_routers)

app.include_router(fastapi_auth_routes)


# if __name__ == "__main__":
#     uvicorn.run("master:app", host='127.0.0.1', port=8000, reload=True)