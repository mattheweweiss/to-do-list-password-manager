from routes.auth_routes import users

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import os


load_dotenv()

port = os.environ.get("PORT")
# Converts to integer
port = int(port)


app = FastAPI()
app.include_router(users)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=port)