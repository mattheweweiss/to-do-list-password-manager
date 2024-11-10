from pydantic import BaseModel


class User(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str
    password: str