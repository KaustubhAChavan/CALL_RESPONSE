from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Create a TwiML response
    twiml_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Call is successful and network is present</Say>
</Response>"""
    return Response(twiml_response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
