from fastapi import FastAPI

app = FastAPI(title="Smart Rental Tracker API")

@app.get("/")
def root():
    return {"msg": "Smart Rental Tracker API up and running"}