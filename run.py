from routes.user_routes import users

import uvicorn
from fastapi import FastAPI

app = FastAPI()
app.include_router(users)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)