## RAM CHECKER


sends a POST request if RAM is full more than the limit

```bash
RAM_USAGE_RERC_LIMIT=20
DELAY_SEC=2
ALARM_URL="http://0.0.0.0:8080"
SERVER_ID=123
```
full alarm url example: `http://0.0.0.0:8080/123`

sends POST request json in percent: `{"value": "43.23"}`

### client

python:
```bash
cd client
python main.py
```
bash:
```bash
cd client
. ram_checker.sh
```

### server

```bash
cd server
docker-compose up
```