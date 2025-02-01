from fastapi import APIRouter, HTTPException #Para utilizar el contexto FastAPI y HTTPException para error de codigo estandar ej: 200, 404
from pydantic import BaseModel #Para tipar un modelo base



router = APIRouter()



# Forma sin tipado:
@router.get("/users_json")
async def users_json():
    return [{ "name":"Junnier", "surname":"anco", "url":"https://junnier.com", "age":30 }, 
            { "name":"Camilo", "surname":"Lux", "url":"https://Camilo.com", "age":25 }]




# Forma con tipado con BaseModel:
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id = 1, name = "Junnier", surname = "anco", url = "https://junnier.com", age = 30), 
              User(id = 2, name = "Camilo", surname = "Lux", url = "https://Camilo.com", age = 25),]




@router.get("/users")
async def users():
    return users_list




# Solicitud Get con Path        http://127.0.0.1:8000/userpath/2
@router.get("/userpath/{id}")
async def user(id: int):
    return search_user(id)




# Solicitud Get con Query de un solo parametro       http://127.0.0.1:8000/userquery/?id=1
@router.get("/userquery/")
async def user_one(id: int):
    return search_user(id)




def search_user(id: int): # Para buscar un usuario
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"Lo sentimos, no hemos encontrado al usuario"}
    
    
    

# Solicitud Get con Query de un dos parametro       http://127.0.0.1:8000/userquerytwo/?id=1&name=Junnier
@router.get("/userquerytwo/")
async def user_two(id: int, name: str):
    return search_user_two_params(id, name)

def search_user_two_params(id: int, name: str):
    users = filter(lambda user: user.id == id and user.name == name, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"Lo sentimos, no hemos encontrado al usuario"}





@router.post("/user", status_code=201, response_model=User) # Para crear un usuario verificando que no exista, status_code permite definir un estandar de codigo por defecto "201 created", response_model para responder con algo en este caso User que es un json con atributos
async def create_user(newUser: User):
    if type(search_user(newUser.id)) == User:
        raise HTTPException(status_code=409, detail="El usuario ya existe") # raise para ejecutar la excepción, HTTPException para invocarla el metodo, status_code para definir el estandar de error, detail para explicar el error
    else:
        users_list.append(newUser)
        return users_list[-1] #Para reenviar el último elemento agregado




@router.put("/user") # Para actualizar un usuario verificando que no exista
async def update_user(newUser: User):
    found = False
    for index, user in enumerate(users_list):
        if user.id == newUser.id:
            users_list[index] = newUser
            found = True
            return {"successful": "Usuario actualizado"}
    
    if not found:
        return {"error": "No se agrego el usuario"}




@router.delete("/user/{id}") # Endpoint para eliminar un usuario con un ID en especifico
async def delete_user(id: int):
    found = False
    for index, user in enumerate(users_list):
        if user.id == id:
            del users_list[index]
            found = True
    
    if found:
        return {"successful": "Usuario eliminado"}
    else:
        return {"error": "No se elimino el usuario"}