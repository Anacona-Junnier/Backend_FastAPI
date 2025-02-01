from pymongo import MongoClient


# Conexión base de datos local
# dbClient = MongoClient().local


# Conexión base de datos remota
# La base de datos se llama "tienda" que está dentro del "Cluster0"
dbClient = MongoClient("mongodb+srv://test:test@cluster0.5jhqi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").tienda


