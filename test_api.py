from app.services.amazon_client import AmazonClient
import json

def test_client():
    client = AmazonClient()
    
    print("Searching for 'gaming mouse'...")
    search_results = client.search_products("gaming mouse")
    products = search_results.get("data", {}).get("products", [])
    
    if products:
        first_product = products[0]
        asin = first_product.get("asin")
        title = first_product.get("product_title")
        print(f"Found: {title} ({asin})")
        
        print(f"Fetching details for {asin}...")
        details = client.get_product_details(asin)
        print("Details fetched successfully.")
        
        print(f"Fetching reviews for {asin}...")
        reviews = client.get_product_reviews(asin)
        review_list = reviews.get("data", {}).get("reviews", [])
        print(f"Found {len(review_list)} reviews.")
    else:
        print("No products found.")

if __name__ == "__main__":
    test_client()
