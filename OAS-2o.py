from fastapi import FastAPI
from fastapi_swagger2 import FastAPISwagger2
from pydantic import BaseModel
import uvicorn

app = FastAPI()
FastAPISwagger2(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Numbers(BaseModel):
    a: float
    b: float

@app.post("/add")
def add(numbers: Numbers):
    result = numbers.a + numbers.b
    return {"result": result}

@app.post("/multiply")
def multiply(numbers: Numbers):
    result = numbers.a * numbers.b
    return {"result": result}

class ForecastRequest(BaseModel):
    latitude: float
    longitude: float
@app.post("/get_forecast")
async def forecast(req: ForecastRequest):
    from weather import get_forecast
    return await get_forecast(req.latitude ,req.longitude)

# /swagger2/docs for 2.0 oas
# /docs for 3.0 oas

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8999)