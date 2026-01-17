from pydantic import BaseModel
from typing import List, Optional

class Review(BaseModel):
    review_id: str
    review_title: Optional[str] = None
    review_comment: Optional[str] = None
    review_star_rating: str  # API returns as string usually
    review_date: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None  # Positive, Neutral, Negative

class Seller(BaseModel):
    seller_id: Optional[str] = None
    seller_name: Optional[str] = None
    seller_rating: Optional[float] = None
    seller_review_count: Optional[int] = None
    trust_score: Optional[float] = None # Calculated by our ML model

class Product(BaseModel):
    asin: str
    product_title: str
    product_price: Optional[str] = None
    product_original_price: Optional[str] = None
    currency: Optional[str] = None
    product_star_rating: Optional[str] = None
    product_num_ratings: Optional[int] = None
    product_url: Optional[str] = None
    product_photo: Optional[str] = None
    is_prime: Optional[bool] = False
    delivery: Optional[str] = None
    
    # Enriched Data
    reviews: List[Review] = []
    seller: Optional[Seller] = None
    
    # ML Scores
    quality_score: Optional[float] = 0.0
    rank: Optional[int] = None
