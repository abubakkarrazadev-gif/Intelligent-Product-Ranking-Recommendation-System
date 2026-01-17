from typing import List, Optional
from app.services.amazon_client import AmazonClient
from app.models.schemas import Product, Review, Seller
from app.ml.sentiment import SentimentModel

class DataService:
    def __init__(self):
        self.client = AmazonClient()

    def search_products(self, query: str, limit: int = 5) -> List[Product]:
        """
        Search for products and return enriched Product objects.
        """
        raw_data = self.client.search_products(query)
        products_data = raw_data.get("data", {}).get("products", [])[:limit]
        
        results = []
        for p_data in products_data:
            product = Product(
                asin=p_data.get("asin"),
                product_title=p_data.get("product_title"),
                product_price=p_data.get("product_price"),
                product_original_price=p_data.get("product_original_price"),
                currency=p_data.get("currency"),
                product_star_rating=p_data.get("product_star_rating"),
                product_num_ratings=p_data.get("product_num_ratings"),
                product_url=p_data.get("product_url"),
                product_photo=p_data.get("product_photo"),
                is_prime=p_data.get("is_prime", False),
                delivery=p_data.get("delivery")
            )
            results.append(product)
            
        return results

    def analyze_product(self, asin: str) -> Optional[Product]:
        """
        Fetch full details, reviews, and perform sentiment analysis.
        """
        # 1. Fetch Details
        details_raw = self.client.get_product_details(asin)
        if not details_raw.get("data"):
            return None
            
        p_data = details_raw["data"]
        
        # 2. Fetch Reviews
        reviews_raw = self.client.get_product_reviews(asin)
        r_data_list = reviews_raw.get("data", {}).get("reviews", [])
        
        # 3. Process Reviews & Sentiment
        processed_reviews = []
        total_sentiment = 0.0
        
        for r in r_data_list:
            comment = r.get("review_comment", "")
            polarity, label = SentimentModel.analyze(comment)
            
            review_obj = Review(
                review_id=r.get("review_id", ""),
                review_title=r.get("review_title"),
                review_comment=comment,
                review_star_rating=r.get("review_star_rating", "0"),
                review_date=r.get("review_date"),
                sentiment_score=polarity,
                sentiment_label=label
            )
        for r in r_data_list:
            comment = r.get("review_comment", "")
            polarity, label = SentimentModel.analyze(comment)
            
            review_obj = Review(
                review_id=r.get("review_id", ""),
                review_title=r.get("review_title"),
                review_comment=comment,
                review_star_rating=r.get("review_star_rating", "0"),
                review_date=r.get("review_date"),
                sentiment_score=polarity,
                sentiment_label=label
            )
            processed_reviews.append(review_obj)
            total_sentiment += polarity
            
        # 3b. Extract Key Features (Pros/Cons)
        all_comments = [r.review_comment for r in processed_reviews if r.review_comment]
        features = SentimentModel.extract_features(all_comments)
        
        # 4. Construct Product Object
        product = Product(
            asin=p_data.get("asin"),
            product_title=p_data.get("product_title"),
            product_price=p_data.get("product_price"),
            product_original_price=p_data.get("product_original_price"),
            currency=p_data.get("currency"),
            product_star_rating=p_data.get("product_star_rating"),
            product_num_ratings=p_data.get("product_num_ratings"),
            product_url=p_data.get("product_url"),
            product_photo=p_data.get("product_photo"),
            is_prime=p_data.get("is_prime", False),
            delivery=p_data.get("delivery"),
            reviews=processed_reviews,
            pros=features['pros'],
            cons=features['cons']
        )
        
        # 5. Extract Seller Info (simplified for now as API support varies)
        # Note: RapidAPI mock/real response structure for seller might vary
        # For now, we will leave seller as None or basic extraction if present in details
        
        return product
