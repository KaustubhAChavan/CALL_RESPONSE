from flask import Flask, Response, request, jsonify
from twilio.rest import Client
import uuid
import time

app = Flask(__name__)

# YOUR TWILIO CREDENTIALS GO HERE
TWILIO_ACCOUNT_SID = 'AC9e0cefa0961ffecb451016cfc5a8cbd2'  # Replace with your actual SID
TWILIO_AUTH_TOKEN = '4eac8bbfcffb97c66d5e1d10a360bb22'     # Replace with your actual token
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Your Twilio phone number
TWILIO_PHONE_NUMBER = '+13158401423'  # Replace with your Twilio number

# Store for call results
call_results = {}



@app.route('/', methods=['GET', 'POST'])
def home():
    # Common message to return
    message = "Network is available and API is accessible"
    
    # Check if the request is from Twilio
    is_twilio_request = request.headers.get('User-Agent', '').startswith('TwilioProxy')
    
    if is_twilio_request or 'text/xml' in request.headers.get('Accept', ''):
        # Return TwiML for Twilio
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{message}</Say>
</Response>"""
        
        # If this is a Twilio call initiated by our app, store the result
        call_sid = request.values.get('CallSid')
        if call_sid:
            call_results[call_sid] = {
                'completed': True,
                'message': message,
                'timestamp': time.time()
            }
            
        return Response(twiml_response, mimetype='text/xml')
    else:
        # Return plain text for app
        return message

@app.route('/check-via-twilio', methods=['POST'])
def check_via_twilio():
    try:
        data = request.json
        twilio_number = data.get('twilioNumber')
        
        # Generate a unique call ID for tracking
        call_id = str(uuid.uuid4())
        
        # Use Twilio to make a call to your verification endpoint
        # This could be your own number that doesn't answer, or a special endpoint
        call = client.calls.create(
            url=f"https://your-server.com/twilio-verify?callId={call_id}",
            to='+15551234567',  # A verification number that doesn't need to answer
            from_=twilio_number,
            timeout=5  # Short timeout since we don't need the call to complete
        )
        
        # Store initial call data
        call_results[call_id] = {
            'completed': False,
            'twilio_sid': call.sid,
            'timestamp': time.time()
        }
        
        return jsonify({
            'success': True,
            'callId': call_id,
            'message': 'Twilio call initiated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/twilio-verify', methods=['GET', 'POST'])
def twilio_verify():
    # This endpoint is called by Twilio when verifying the network
    call_id = request.args.get('callId')
    
    if call_id and call_id in call_results:
        call_results[call_id]['completed'] = True
        call_results[call_id]['message'] = "Network verified successfully via Twilio"
    
    # Return minimal TwiML to end the call
    twiml_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Hangup/>
</Response>"""
    return Response(twiml_response, mimetype='text/xml')

@app.route('/check-result', methods=['GET'])
def check_result():
    call_id = request.args.get('callId')
    
    if not call_id or call_id not in call_results:
        return jsonify({
            'success': False,
            'message': 'Invalid or expired call ID'
        }), 404
    
    result = call_results[call_id]
    
    # Clean up old results (optional)
    current_time = time.time()
    for key in list(call_results.keys()):
        if current_time - call_results[key].get('timestamp', 0) > 3600:  # 1 hour
            del call_results[key]
    
    return jsonify({
        'success': True,
        'completed': result.get('completed', False),
        'message': result.get('message', 'Network check in progress')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
