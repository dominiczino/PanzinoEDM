import requests
import time


while True:
    time.sleep(2)
    r=requests.post("http://192.168.0.129:8080/api/v1/NYqjaBhuqyJgAUQTQAGx/telemetry", json={"Temp":65})
    print(r)
