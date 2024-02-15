from fastapi import FastAPI
from routes import fastapi_auth_routes
import uvicorn


app = FastAPI()


app.include_router(fastapi_auth_routes)


# if __name__ == "__main__":
#     uvicorn.run("master:app", host='127.0.0.1', port=8000, reload=True)