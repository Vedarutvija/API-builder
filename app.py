from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

# Define a model for the water bill
class WaterBill(BaseModel):
    id: int
    date: date
    amount: float
    customer_name: str
    address: str

# In-memory database to store the bills
water_bills = []

# POST endpoint to create a water bill
@app.post("/waterbills/", response_model=WaterBill)
def create_water_bill(bill: WaterBill):
    # Check for duplicate IDs
    for existing_bill in water_bills:
        if existing_bill.id == bill.id:
            raise HTTPException(status_code=400, detail="Bill with this ID already exists.")
    water_bills.append(bill)
    return bill

# GET endpoint to retrieve all water bills
@app.get("/waterbills/", response_model=List[WaterBill])
def get_all_bills():
    return water_bills

# GET endpoint to retrieve a specific water bill by ID
@app.get("/waterbills/{bill_id}", response_model=WaterBill)
def get_bill(bill_id: int):
    for bill in water_bills:
        if bill.id == bill_id:
            return bill
    raise HTTPException(status_code=404, detail="Bill not found.")

# PUT endpoint to update a water bill by ID
@app.put("/waterbills/{bill_id}", response_model=WaterBill)
def update_bill(bill_id: int, updated_bill: WaterBill):
    for index, bill in enumerate(water_bills):
        if bill.id == bill_id:
            water_bills[index] = updated_bill
            return updated_bill
    raise HTTPException(status_code=404, detail="Bill not found.")

# DELETE endpoint to delete a water bill by ID
@app.delete("/waterbills/{bill_id}", response_model=WaterBill)
def delete_bill(bill_id: int):
    for index, bill in enumerate(water_bills):
        if bill.id == bill_id:
            return water_bills.pop(index)
    raise HTTPException(status_code=404, detail="Bill not found.")

@app.get("/")
def welcome():
    return {"message": "Hello, World!"}