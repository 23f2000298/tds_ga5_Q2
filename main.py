from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI()


class ProrateRequest(BaseModel):
    old_price: float
    new_price: float
    days_remaining: float
    days_in_actual_month: float
    spec: Literal["v1", "v2"]


@app.post("/prorate")
async def prorate(req: ProrateRequest):
    price_delta = req.new_price - req.old_price

    if req.spec == "v1":
        charge = price_delta * (req.days_remaining / 30)
    else:  # "v2"
        charge = price_delta * (req.days_remaining / req.days_in_actual_month)

    return {"charge": round(charge, 2)}


@app.get("/")
async def health():
    return {"status": "ok"}
