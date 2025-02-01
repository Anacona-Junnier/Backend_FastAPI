from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



router = APIRouter(prefix="/basicauth",
                   tags=["basic_auth_info"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})


oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool
    

class UserDB(User):
    password: str


users_db = {
    "julian": {
        "username":"julian",
        "full_name": "Julian Duzan",
        "email": "julian@gmail.com",
        "disable": False,
        "password": "123456"
    },
    "camila": {
        "username":"camila",
        "full_name": "Camila Ortiz",
        "email": "camila@gmail.com",
        "disable": False,
        "password": "654321"
    }
}


async def current_user(token : str = Depends(oauth2)):
    user = search_user(token)
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado")
    
    return user


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_db(form.username)
    #user = users_db.get(form.username) # Otra forma de obtener un usuario, se accede así: user["password"]
    
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto")

    if not user_db.password == form.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta")
    
    return {"access_token": user_db.username, "token_type" : "bearer" }

@router.get("/user/me")
async def me(user : User = Depends(current_user)):
    return user



