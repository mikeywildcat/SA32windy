"""
Poll the local GPS HTTP endpoint repeatedly and print timestamped results.
Run for ~30s to capture plugin-like polling behavior.
"""
import time
import requests

URL = 'http://localhost:5000/gps-data'
DURATION = 30.0
INTERVAL = 0.5

end = time.time() + DURATION
count = 0
while time.time() < end:
    t = time.time()
    try:
        r = requests.get(URL, timeout=1.0)
        text = r.text.strip()
        print(f"{time.strftime('%H:%M:%S')} | {len(text):4d} bytes | {text}")
    except Exception as e:
        print(f"{time.strftime('%H:%M:%S')} | ERROR: {e}")
    count += 1
    sleep_time = INTERVAL - (time.time() - t)
    if sleep_time > 0:
        time.sleep(sleep_time)

print('Done')
