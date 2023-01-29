from google.cloud import datastore
import functions_framework

@functions_framework.http

def fetch_wishlist_count(request):

    client = datastore.Client()
    query = client.query(kind="session_wishlist")
    
    query.add_filter("wishlist_status", "=", 1)

    wishlist_count = 0
    for entity in query.fetch():
        # product_id = entity['product_id']
        wishlist_count+=1

    return {"wishlist_count":wishlist_count} 