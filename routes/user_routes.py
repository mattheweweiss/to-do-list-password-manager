from fastapi import APIRouter

users = APIRouter()

@users.get('/confirm_user')
def confirm_user():
    return "work!"