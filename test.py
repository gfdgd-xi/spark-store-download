import requests
import time
while True:
    try:
        print(requests.post("http://127.0.0.1:8000", {"spk": "spk://store/store/com.gitee.uengine.runner.spark"}).text)
        time.sleep(0.1)
    except:
        pass