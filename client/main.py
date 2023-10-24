import json
import os
import time
from urllib import request


RAM_USAGE_RERC_LIMIT = int(os.getenv("RAM_USAGE_RERC_LIMIT", "90"))
DELAY_SEC = int(os.getenv("DELAY_SEC", "1"),)
ALARM_URL = os.getenv("ALARM_URL", "http://0.0.0.0:8080")
SERVER_ID = os.getenv("SERVER_ID", "123")
headers={'Content-Type':'application/json'}

def ram_usage_percentage():
    # only RAM without swapfile and buff/cache
    total_memory, used_memory, free_memory, shared, buffcache, available = map(
        int, os.popen("free -t -m").readlines()[1].split()[1:]
    )

    return used_memory / total_memory * 100


print("RAM checker started")
while True:
    try:
        used = ram_usage_percentage()
        if used >= RAM_USAGE_RERC_LIMIT:
            data = json.dumps({"value": round(used, 2)})        
            bindata = data if type(data) == bytes else data.encode('utf-8')
            req = request.Request(f"{ALARM_URL}/{SERVER_ID}", bindata, headers)
            resp = request.urlopen(req)

            
        time.sleep(DELAY_SEC)

    except KeyboardInterrupt:
        print("RAM checker stopped")
        break
    
