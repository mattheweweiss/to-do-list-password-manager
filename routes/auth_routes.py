from schemas.auth_schemas import User
from services.auth_service import find_user, create_user

from fastapi import APIRouter, Request

users = APIRouter()



# Creates account
# Creates user and user hash and user salt and stores in database
@users.post('/create_account')
async def create_account(user: User):

    try:
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        password = user.password


        # Only create accounts if email address is not used yet
        if not find_user(email):
            return create_user(first_name, last_name, email, password)
        else:
            raise Exception("The email address is already in-use")

    except Exception as e:
        print(e)
        return e