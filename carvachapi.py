from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()
data = []

db_name = "carvach"
db_user = "postgres"
db_pswd = "9212"
db_host = "localhost"
db_port = "5432"

# Establish a database connection
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_pswd,
    host=db_host,
    port=db_port
)

class Car(BaseModel):
    owner_name: str
    model: str
    brand: str

@app.post("/car")
def create_car(car: Car):
    cursor = conn.cursor()
    insert_query = "INSERT INTO car(owner_name, model, brand) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (car.owner_name, car.model, car.brand))
    conn.commit()
    cursor.close()
    
    return car

@app.get("/car/{id}")
def read_car(id: int):
    cursor = conn.cursor()
    select_query = "SELECT * FROM car WHERE id = %s"
    cursor.execute(select_query, (id,))
    car = cursor.fetchone()
    cursor.close()
    
    if car:
        return {"id": car[0], "owner_name": car[1], "model": car[2], "brand": car[3]}
    else:
        return {"error": "Car not found"}

@app.put("/car/{id}")
def update_car(id: int, car: Car):
    cursor = conn.cursor()
    update_query = "UPDATE car SET owner_name = %s, model = %s, brand = %s WHERE id = %s"
    cursor.execute(update_query, (car.owner_name, car.model, car.brand, id))
    conn.commit()
    cursor.close()
    
    return {"message": "Car updated successfully"}

@app.delete("/car/{id}")
def delete_car(id: int):
    cursor = conn.cursor()
    delete_query = "DELETE FROM car WHERE id = %s"
    cursor.execute(delete_query, (id,))
    conn.commit()
    cursor.close()
    
    return {"message": "Car deleted successfully"}
