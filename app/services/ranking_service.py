from typing import List
from app.services.data_service import DataService
from app.ml.scoring import ScoringModel
from app.models.schemas import Product

class RankingService:
    def __init__(self):
        self.data_service = DataService()
        self.scorer = ScoringModel()

    def get_top_products(self, query: str, limit: int = 5) -> List[Product]:
        """
        Search, Analyze, Score, and Rank products.
        """
        # 1. Search (Fetch basic data)
        print(f"RankingService: Searching for '{query}'...")
        products = self.data_service.search_products(query, limit=limit)
        
        scored_products = []
        for p in products:
            # 2. Analyze (Fetch detailed data + Sentiment)
            print(f"RankingService: Analyzing {p.asin}...")
            enriched_p = self.data_service.analyze_product(p.asin)
            
            if enriched_p:
                # 3. Score
                score = self.scorer.calculate_score(enriched_p)
                enriched_p.quality_score = score
                scored_products.append(enriched_p)
        
        # 4. Rank (Sort by score descending)
        ranked_products = sorted(scored_products, key=lambda x: x.quality_score, reverse=True)
        
        # Assign rank numbers
        for i, p in enumerate(ranked_products):
            p.rank = i + 1
            
        return ranked_products
