from app.models.schemas import Product
import math

class ScoringModel:
    @staticmethod
    def calculate_score(product: Product) -> float:
        """
        Calculate a 0-100 score for a product based on multiple factors.
        """
        # 1. Base Rating Score (0-50)
        try:
            rating = float(product.product_star_rating or 0)
        except ValueError:
            rating = 0.0
        
        rating_score = (rating / 5.0) * 50
        
        # 2. Sentiment Score (0-30)
        # Average sentiment of fetched reviews (-1 to 1) -> mapped to 0-30
        reviews = product.reviews
        if reviews:
            avg_sentiment = sum(r.sentiment_score for r in reviews) / len(reviews)
        else:
            avg_sentiment = 0.0
            
        # Map -1..1 to 0..1 -> (s + 1) / 2
        # Then multiply by 30
        sentiment_component = ((avg_sentiment + 1) / 2) * 30
        
        # 3. Review Volume Confidence (0-20)
        # Logarithmic scale for number of ratings
        try:
            num_ratings = product.product_num_ratings or 0
        except:
            num_ratings = 0
            
        # Cap at 10,000 ratings for max score
        if num_ratings > 0:
            volume_score = min(20, 4 * math.log10(num_ratings))
        else:
            volume_score = 0
            
        # Total Score
        final_score = rating_score + sentiment_component + volume_score
        
        return round(min(100, final_score), 2)
