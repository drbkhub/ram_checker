import os

from flask import Flask, Response, request, jsonify, make_response
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
redis = redis.Redis(connection_pool=pool)


@app.route('/<key>', methods = ['GET', 'POST', 'PUT'])
def ram(key):
   if request.method == 'GET':
      value_db = redis.get(key)
      if value_db:
         return jsonify({"key": key, "value": value_db.decode("utf8")})
      
      return make_response(jsonify({"key": key, "value": None}), 404)
   
   if request.content_type != "application/json":
      return Response(
         response="Incorrect content format, require JSON", status=400
      )
   
   data = request.json
   value = data.get('value')
   if not value:
      return Response(
         response="Require JSON key (value)", status=400
      )

   elif request.method == 'POST':
      redis.set(key, value)
      return make_response(jsonify({"key": key, "value": value}), 201)

   
   elif request.method == 'PUT':
      redis.set(key, value)
      return make_response(jsonify({"key": key, "value": value}), 204 if redis.get(key) else 201)




if __name__ == '__main__':
   from waitress import serve
   serve(app, host="0.0.0.0", port=8080)
   # app.run(port=8080, host='0.0.0.0')