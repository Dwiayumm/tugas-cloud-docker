import time
import redis
from flask import Flask

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

@app.route('/')
def hello():
    count = get_hit_count()
    # Tampilan Dashboard UI sederhana dengan HTML & CSS bawaan
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flash Sale Dashboard</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .dashboard-card {{ background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); text-align: center; width: 450px; border-top: 5px solid #ff4757; }}
            .logo {{ font-size: 26px; font-weight: bold; color: #ff4757; margin-bottom: 10px; letter-spacing: 1px; }}
            .status {{ color: #2ed573; font-weight: bold; margin-bottom: 25px; font-size: 14px; background: #e8f8f5; padding: 5px 15px; border-radius: 20px; display: inline-block; }}
            .counter-box {{ background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
            .counter {{ font-size: 56px; font-weight: bold; color: #2f3542; margin: 10px 0; }}
            .label {{ color: #747d8c; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
            .footer {{ color: #a4b0be; font-size: 12px; margin-top: 20px; border-top: 1px solid #f1f2f6; padding-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="dashboard-card">
            <div class="logo">⚡ RETAIL MEGA FLASH SALE ⚡</div>
            <div class="status">🟢 Server Azure Active & Scaled</div>
            
            <div class="counter-box">
                <div class="label">Live Traffic / Antrean Pembeli:</div>
                <div class="counter">{count}</div>
                <div class="label">Pengunjung Sedang Memantau Promo</div>
            </div>
            
            <div class="footer">Sistem Pelacak Real-Time Berbasis Redis & Docker container</div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)