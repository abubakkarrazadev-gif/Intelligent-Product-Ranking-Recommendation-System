from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.services.ranking_service import RankingService
from app.services.data_service import DataService
from app.models.schemas import Product

router = APIRouter()
ranking_service = RankingService()
data_service = DataService()

@router.get("/recommend/{query}", response_model=List[Product])
async def recommend_products(query: str, limit: int = 5):
    """
    Search and rank products based on the query.
    """
    try:
        results = ranking_service.get_top_products(query, limit)
        return results
    except Exception as e:
        print(f"Error in recommend: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/product/{asin}/analysis", response_model=Product)
async def analyze_product(asin: str):
    """
    Get detailed analysis for a specific product.
    """
    try:
        product = data_service.analyze_product(asin)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        # Ensure it has a score
        from app.ml.scoring import ScoringModel
        score = ScoringModel.calculate_score(product)
        product.quality_score = score
        
        return product
    except Exception as e:
        print(f"Error in analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
