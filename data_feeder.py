import requests
import random
import time

IOT_AGENT_URL = "http://20.63.91.180:7896/iot/d?k=health-api-key&i=dev-esp32-001"

while True:
    body_temp = round(random.uniform(36.0, 38.5), 1)
    heart_rate = random.randint(60, 140)
    distance_km = round(random.uniform(0.0, 0.5), 4)

    payload = f"t|{body_temp}|h|{heart_rate}|d|{distance_km}"
    headers = {"Content-Type": "text/plain"}

    try:
        r = requests.post(IOT_AGENT_URL, data=payload, headers=headers, timeout=3)
        print("Enviado:", payload, "| HTTP", r.status_code)
    except Exception as e:
        print("Erro ao enviar:", e)

    time.sleep(5)
