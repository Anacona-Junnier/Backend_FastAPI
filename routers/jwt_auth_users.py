from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError


router = APIRouter(prefix="/jwtauth",
                   tags=["jwt_auth_info"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})


oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


# contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])


# ejecutar: openssl rand -hex 32 para obtener una clave secreta
SECRET = "08dd2d1b87376fbdbaca8db5173dc296740f9c5de96159b212ecdf891c814061"
ALGORITHM = "HS256" # algoritmo de encriptación
ACCESS_TOKEN_EXPIRE_MINUTES = 1 #tiempo de expiracion del token


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
        "password": "$2a$12$sE/WK9JbINFoJBBWzEN12.e1mU5UQ6L2dH2ddX9VDfwSM.7TZ7cMO"
    },
    "camila": {
        "username":"camila",
        "full_name": "Camila Ortiz",
        "email": "camila@gmail.com",
        "disable": True,
        "password": "$2a$12$fR47UcybtFB19LqH8BPoM.708a5vz4k61bqHjoqaY/RQ0kyZwBEpq"
    }
}


async def verify_token(token : str = Depends(oauth2)):
    exceptionMessage = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado",
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exceptionMessage
    except InvalidTokenError:
        raise exceptionMessage
        
    return username
        
        
async def current_user(username : str = Depends(verify_token)):
    user = search_user(username) 
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

    # comparar contraseñas con verify
    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta")
    
    # datetime.now(timezone.utc) Obtiene la fecha y hora actuales en el huso horario UTC (Tiempo Universal Coordinado).
    # timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) intervalo de tiempo de 1 minuto por el ACCESS_TOKEN_EXPIRE_MINUTES
    time_expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = {"sub": user_db.username, "exp": time_expire}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type" : "bearer" }

@router.get("/user/me")
async def me(user : User = Depends(current_user)):
    return user