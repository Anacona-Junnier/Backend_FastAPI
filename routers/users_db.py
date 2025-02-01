from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.models.user import User
from db.connection_mongodb import dbClient
from db.schemas.user import user_schema, users_schema
from bson import ObjectId


router = APIRouter(prefix="/usersdb",
                   tags=["usersdb_info"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})


oauth2 = OAuth2PasswordBearer(tokenUrl="/usersdb")


@router.get("/", response_model=list[User])
async def usersDB():
    return users_schema(dbClient.users.find())


@router.get("/{id}")
async def userDB(id: str):
    return findUser("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def createUserDB(user: User):
    if type(findUser("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe")
    
    userDictionary = dict(user)
    del userDictionary["id"]
    
    idUser = dbClient.users.insert_one(userDictionary).inserted_id
    newUser = findUser("_id", idUser)
    return newUser

    


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def deleteUserDB(id: str):
    found = dbClient.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error": "usuario no eliminado"}


@router.put("/", status_code= status.HTTP_200_OK)
async def updateUserDB(user: User):
    userDictionary = dict(user)
    del userDictionary["id"]
    try:
        dbClient.users.find_one_and_replace({"_id": ObjectId(user.id)}, userDictionary)       
    except:
        return {"error": "No sé actualizo el usuario"}
    
    return findUser("_id", ObjectId(user.id))


def findUser(field: str, key):
    try:  
        user = user_schema(dbClient.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error": "No se ha encontrado el usuario"}
    
    