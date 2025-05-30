from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # You can get the phone number from the request if you want
    data = request.get_json(silent=True)
    phone = None
    if data and 'phone' in data:
        phone = data['phone']

    # Do your logic here (log, process, etc.)
    # For demo, just reply with a message
    message = "Hello from backend! API reached successfully."
    if phone:
        message += f" Phone number received: {phone}"

    return jsonify({
        "success": True,
        "message": message
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
