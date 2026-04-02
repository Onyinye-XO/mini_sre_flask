from flask import Flask
import random
import time

app = Flask(__name__)

# --- Store metrics in memory ---
metrics = {
    "index":  {"requests": 0, "success": 0, "errors": 0, "total_time": 0.0},
    "slow":   {"requests": 0, "success": 0, "errors": 0, "total_time": 0.0},
    "fail":   {"requests": 0, "success": 0, "errors": 0, "total_time": 0.0},
}

def record(route_name, status_code, elapsed):
    """Update metrics for a given route after each request."""
    m = metrics[route_name]
    m["requests"]   += 1
    m["total_time"] += elapsed
    if status_code >= 400:
        m["errors"]  += 1
    else:
        m["success"] += 1


# --- Routes ---
@app.route('/')
def index():
    start = time.time()
    elapsed = time.time() - start
    record("index", 200, elapsed)
    return 'Service is running'

@app.route('/slow')
def slow():
    start = time.time()
    time.sleep(5)
    elapsed = time.time() - start
    record("slow", 200, elapsed)
    return {"status": "success", "message": "Response was slow", "latency": "5s"}, 200

@app.route('/fail')
def fail():
    start = time.time()
    if random.random() < 0.5:
        status = 500
        response = {"status": "error", "message": "Something went wrong"}, 500
    else:
        status = 200
        response = {"status": "success", "message": "Recovered successfully"}, 200
    elapsed = time.time() - start
    record("fail", status, elapsed)
    return response


# --- Dashboard ---
@app.route('/dashboard')
def dashboard():
    rows = ""
    for route, m in metrics.items():
        avg_time = (m["total_time"] / m["requests"] * 1000) if m["requests"] > 0 else 0
        rows += f"""
        <tr>
            <td>/{route}</td>
            <td>{m['requests']}</td>
            <td style="color: green">{m['success']}</td>
            <td style="color: red">{m['errors']}</td>
            <td>{avg_time:.2f} ms</td>
        </tr>"""

    return f"""
    <html>
    <head>
        <title>App Dashboard</title>
        <style>
            body    {{ font-family: Arial, sans-serif; padding: 30px; background: #f4f4f4; }}
            h1      {{ color: #333; }}
            table   {{ border-collapse: collapse; width: 60%; background: white; }}
            th, td  {{ padding: 12px 16px; border: 1px solid #ddd; text-align: left; }}
            th      {{ background: #333; color: white; }}
            tr:hover{{ background: #f0f0f0; }}
        </style>
        <meta http-equiv="refresh" content="5">  <!-- auto-refreshes every 5 seconds -->
    </head>
    <body>
        <h1>📊 Mini SRE Dashboard</h1>
        <table>
            <tr>
                <th>Route</th>
                <th>Total Requests</th>
                <th>Successes</th>
                <th>Errors</th>
                <th>Avg Response Time</th>
            </tr>
            {rows}
        </table>
        <p style="color: grey; font-size: 12px">Auto-refreshes every 5 seconds</p>
    </body>
    </html>
    """

# --- Random route runner ---
def run_random_route():
    routes = [index, slow, fail]
    chosen = random.choice(routes)
    print(f"Running route: {chosen.__name__}")
    result = chosen()
    print(f"Result: {result}")

if __name__ == "__main__":
    run_random_route()
    app.run(debug=True)