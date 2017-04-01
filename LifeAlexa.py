import phone_number
import boto3

def lambda_handler(event, context):
    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'])
    else:
        return on_intent(event['request'])

def on_launch(request):
    output = 'Preparing to send message. Are you sure you\'d like me to send?'
    return build_response(output, False)

def on_intent(request):
    continueIntents = ['PositiveResponseIntent', 'NegativeResponseIntent', 'SendMessageIntent']
    if request['intent']['name'] not in continueIntents:
        return build_response("", True)
    if request['intent']['name'] == 'SendMessageIntent':
        return on_launch(request)
    if request['intent']['name'] == 'PositiveResponseIntent':
        output = "Okay, contacting your emergency contact."
        text_contact()
        should_end_session = True
    elif request['intent']['name'] == 'NegativeResponseIntent':
        output = "Canceled"
        should_end_session = True
    return build_response(output, should_end_session)

def build_response(output, should_end_session):
    speechlet_response = {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": "LifeAlexa",
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output
            }
        },
        "shouldEndSession": should_end_session
    }
    return {
        "version": "1.0",
        "session_attributes": {},
        "response": speechlet_response
    }

def text_contact():
    client = boto3.client('sns')
    message = "This is a LifeAlexa alert. Your friend or loved one has requested assistance from their home."
    client.publish(Message=message, PhoneNumber=phone_number.PHONE_NUMBER)