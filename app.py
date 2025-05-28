from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Common message to return
    message = "Network is available and API is accessible"
    
    # Check if the request is from Twilio or a direct network check
    is_twilio_request = request.headers.get('User-Agent', '').startswith('TwilioProxy')
    is_network_check = request.headers.get('X-Network-Check') == 'true'
    
    if is_twilio_request or 'text/xml' in request.headers.get('Accept', ''):
        # Return TwiML for Twilio
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{message}</Say>
</Response>"""
        return Response(twiml_response, mimetype='text/xml')
    else:
        # Return XML format for app network checks too for consistency
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{message}</Say>
</Response>"""
        return Response(twiml_response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
