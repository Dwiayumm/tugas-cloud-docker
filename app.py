import time
import redis
from flask import Flask, render_template, jsonify

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_current_count():
    retries = 5
    while True:
        try:
            val = cache.get('hits')
            return int(val) if val else 0
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('index.html', count=count)

# Endpoint khusus untuk AJAX polling — hanya mengembalikan JSON angka terkini
@app.route('/count')
def count():
    current = get_current_count()
    return jsonify({'count': current})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)