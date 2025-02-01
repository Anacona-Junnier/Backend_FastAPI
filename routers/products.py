from fastapi import APIRouter

# prefix= definir el domino general sin especificarlo en cada funcion que se cree, responses= definir un error por defecto,
# tags= para que en la documentación se divida esta seccion de api products 
router = APIRouter(prefix="/products", responses={404: {"error": "No encontrado"}}, tags=["products_info"]) 

products_list = ["Producto 1", "Producto 2", "Producto 3","Producto 5"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def product(id: int):
    return products_list[id]