import random, time
from fastapi import FastAPI, HTTPException
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

def cpu_temp():
    try:
        return int(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000
    except Exception:
        return 0

Gauge("pi_cpu_temp_celsius", "Temperatura da CPU").set_function(cpu_temp)

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/work")
def work():
    time.sleep(random.uniform(0.05, 0.6))
    if random.random() < 0.1:
        raise HTTPException(500, "erro aleatório")
    return {"done": True}

Instrumentator().instrument(app).expose(app)