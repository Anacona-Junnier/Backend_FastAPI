from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="imagenEstatica") # llamar recursos estaticos en un directorio
app.include_router(users_db.router)



@app.get("/")
async def read_root():
    return "Hello World"

@app.get("/url")
async def obtener_URL():
    return { "url_curso":"http://junnier.com" }