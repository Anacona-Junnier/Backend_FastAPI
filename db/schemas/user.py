# Aquí van las operaciones que nos permiten convertir el modulo de nuestro usuario al esquema que recibe la BD
def user_schema(userDB):
    return {"id": str(userDB["_id"]), 
            "username": userDB["username"],
            "email": userDB["email"]}
    
    
def users_schema(usersDB) -> list:
    return [user_schema(user) for user in usersDB] # recorre y almacena con el esquema en una lista