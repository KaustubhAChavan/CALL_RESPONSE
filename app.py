from flask import Flask

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    return "call is successful, network is present"

@app.route('/', methods=['GET'])
def home():
    return "Welcome to my Flask API! Try /api/health endpoint."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)