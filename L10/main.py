from typing import Dict, List, Optional
from fastapi import FastAPI
from joblib import load
from tinydb import TinyDB, Query
from datetime import datetime
from tinydb.operations import set

app = FastAPI(title="Lab 6")

# aquí carguen el modelo guardado (con load de joblib) y
model = load("modelo.joblib")
# el cliente de base de datos (con tinydb). Usen './db.json' como bbdd.
db = TinyDB("./db.json")

# Nota: En el caso que al guardar en la bbdd les salga una excepción del estilo JSONSerializable
# conviertan el tipo de dato a uno más sencillo.
# Por ejemplo, si al guardar la predicción les levanta este error, usen int(prediccion[0])
# para convertirla a un entero nativo de python.

# Nota 2: Las funciones ya están implementadas con todos sus parámetros. No deberían
# agregar más que esos.


@app.post("/potabilidad/")
async def predict_and_save(observation: Dict[str, float]):
    input_post_list = list(observation.values())
    Prediction = int(model.predict([input_post_list])[0])
    hoy = datetime.now()
    observation["Day"] = hoy.day
    observation["Month"] = hoy.month
    observation["Year"] = hoy.year
    observation['Prediction'] = Prediction
    id_row = db.insert(observation)
    return {"potabilidad": Prediction, "id": id_row}


@app.get("/potabilidad/")
async def read_all():
    # implementar 2 aquí.
    return db.all()



@app.get("/potabilidad_diaria/")
async def read_by_day(day: int, month: int, year: int):
    # implementar 3 aquí
    Mediciones = Query()
    return db.search((Mediciones.Day == day) & (Mediciones.Month == month) & (Mediciones.Year == year))


@app.put("/potabilidad/")
async def update_by_day(day: int, month: int, year: int, new_prediction: int):
    # implementar 4 aquí
    Mediciones = Query()
    try:
        ids = db.update(set("ph", new_prediction),(Mediciones.Day == day) & (Mediciones.Month == month) & (Mediciones.Year == year))
        return { "success": True, "updated_elements":ids}
    except:
        return { "success": False, "updated_elements": []}


@app.delete("/potabilidad/")
async def delete_by_day(day: int, month: int, year: int):
    # implementar 5 aquí
    Mediciones = Query()
    try:
        ids = db.remove((Mediciones.Day == day) & (Mediciones.Month == month) & (Mediciones.Year == year))
        return { "success": True, "deleted_elements":ids}
    except:
        return { "success": False, "deleted_elements": []}
