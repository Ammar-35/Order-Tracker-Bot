from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

tracking_data = {}

agents = [
    {"name": "Rahul Sharma", "phone": "9876543210"},
    {"name": "Amit Verma", "phone": "9123456780"},
    {"name": "Sneha Patil", "phone": "9988776655"}
]

def validate_tracking_id(tid):
    return re.match(r'^[A-Za-z]{4}[0-9]{3}$', tid)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    tid = data.get("tracking_id")

    if not validate_tracking_id(tid):
        return jsonify({"status": "invalid"})

    if tid not in tracking_data:
        tracking_data[tid] = random.choice(["delivered", "transit", "lost"])

    status = tracking_data[tid]

    if status == "delivered":
        return jsonify({"status": "delivered"})

    elif status == "transit":
        agent = random.choice(agents)
        return jsonify({
            "status": "transit",
            "agent": agent
        })

    else:
        return jsonify({"status": "lost"})

@app.route('/complaint', methods=['POST'])
def complaint():
    data = request.json
    tid = data.get("tracking_id")
    confirm_tid = data.get("confirm_id")

    if tid != confirm_tid:
        return jsonify({"status": "mismatch"})

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)