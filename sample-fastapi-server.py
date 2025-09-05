from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

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

# @app.post("/get_alerts")
# async def alerts(state: str):
#     from weather import get_alerts
#     return await get_alerts(state)
class WeatherRequest(BaseModel):
    state: str
@app.post("/get_alerts")
async def alerts(req: WeatherRequest):
    from weather import get_alerts
    return await get_alerts(req.state)   
 
from fastapi_mcp import FastApiMCP
mcp = FastApiMCP(app)
mcp.mount_http()
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    