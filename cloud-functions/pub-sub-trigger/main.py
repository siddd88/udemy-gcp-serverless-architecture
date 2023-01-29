import base64

def process_pubsub_events(event, context):

    message = base64.b64decode(event['data']).decode('utf-8')

    event_id = context.event_id
    event_type = context.event_type

    print(f"A new event is received: id={event_id}, type={event_type}")
    print(f"data = {message}")

    