from fastapi import FastAPI
from routes import auth_routers
import uvicorn


app = FastAPI()

# # Добавить функционал очистки БД
# @app.on_event('startup')
# def start_up():
#     pass

app.include_router(auth_routers)


# if __name__ == "__main__":
#     uvicorn.run("master:app", host='127.0.0.1', port=8000, reload=True)