from fastapi import FastAPI
import json

from datebase import Drug, db

app = FastAPI()


@app.get("/")
async def root():
    return Drug.get_all_json()


@app.get("/{filter}")
async def drugs_filter(filter: str):
    return Drug.filter(filter)


@app.get("/get/{id}")
async def drug_get(id: int):
    return Drug.get_by_id(id)


@app.get("/name/{name}")
async def drug_get(name: str):
    return Drug.get_by_name(name)


@app.get("/original_pack/{original_pack}")
async def drug_get(original_pack: str):
    return Drug.get_by_original_pack(original_pack)


@app.get("/base_price/{base_price}")
async def drug_get(base_price: str):
    return Drug.get_by_base_price(base_price)


@app.get("/expiration_date/{expiration_date}")
async def drug_get(expiration_date: str):
    return Drug.get_by_expiration_date(expiration_date)


@app.get("/manufacturer/{manufacturer}")
async def drug_get(manufacturer: str):
    return Drug.get_by_manufacturer(manufacturer)
