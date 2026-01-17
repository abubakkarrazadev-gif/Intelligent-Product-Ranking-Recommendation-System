import requests
from typing import Dict, List, Optional
from app.core.config import settings

class AmazonClient:
    def __init__(self):
        self.headers = {
            "x-rapidapi-key": settings.RAPIDAPI_KEY,
            "x-rapidapi-host": settings.RAPIDAPI_HOST
        }
        self.base_url = settings.BASE_URL

    def search_products(self, query: str, country: str = "US") -> Dict:
        """
        Search for products by query.
        """
        url = f"{self.base_url}/search"
        querystring = {"query": query, "country": country}
        
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching products: {e}")
            return {"data": {"products": []}}

    def get_product_details(self, asin: str, country: str = "US") -> Dict:
        """
        Get detailed product information.
        """
        url = f"{self.base_url}/product-details"
        querystring = {"asin": asin, "country": country}
        
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching product details: {e}")
            return {}

    def get_product_reviews(self, asin: str, country: str = "US", sort_by: str = "TOP_REVIEWS") -> Dict:
        """
        Get reviews for a product.
        """
        url = f"{self.base_url}/product-reviews"
        querystring = {"asin": asin, "country": country, "sort_by": sort_by}
        
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching reviews: {e}")
            return {"data": {"reviews": []}}
