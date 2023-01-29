import base64,json
from google.cloud import datastore

def trigger_wishlist_event(event,context):

    input_payload = base64.b64decode(event['data']).decode('utf-8')
    input_payload_dict = json.loads(input_payload)
    
    session_id = input_payload_dict['notification'][0]['session_id']
    product_id = input_payload_dict['notification'][1]['product_id']
    wishlist_status = input_payload_dict['notification'][2]['wishlist_status']

    upsert_user_wishlist(session_id,product_id,wishlist_status)

def upsert_user_wishlist(session_id,product_id,wishlist_status):

    client = datastore.Client()
    unique_id = session_id + "_" + str(product_id)

    key = client.key("session_wishlist",unique_id)

    entity = datastore.Entity(key=key)
    entity.update(
        {
            "product_id": product_id,
            "wishlist_status":wishlist_status
        }
    )

    client.put(entity)

    print("Wishlist Updated")

