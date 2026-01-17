from textblob import TextBlob

class SentimentModel:
    @staticmethod
    def extract_features(text_list: list) -> dict:
        """
        Extract frequent noun phrases (topics) and their sentiment.
        Returns: {'pros': ['battery life', 'screen'], 'cons': ['shipping']}
        """
        if not text_list:
            return {"pros": [], "cons": []}
            
        full_text = " ".join(text_list)
        blob = TextBlob(full_text)
        
        # Simple extraction strategy:
        # 1. Get Noun Phrases
        # 2. Check sentiment of sentences containing them
        
        features = {}
        for sentence in blob.sentences:
            pol = sentence.sentiment.polarity
            for noun in sentence.noun_phrases:
                noun = noun.lower()
                if len(noun) < 3: continue
                if noun not in features:
                    features[noun] = []
                features[noun].append(pol)
                
        # Aggregate
        pros = []
        cons = []
        
        for noun, scores in features.items():
            if len(scores) < 1: continue # Filter rare mentions
            avg_score = sum(scores) / len(scores)
            
            if avg_score > 0.15:
                pros.append(noun)
            elif avg_score < -0.15:
                cons.append(noun)
                
        # Return top 5 unique
        return {
            "pros": list(set(pros))[:5],
            "cons": list(set(cons))[:5]
        }
    
    @staticmethod
    def analyze(text: str):
        """
        Analyze the sentiment of a text string.
        Returns:
            polarity (float): -1.0 to 1.0 (Negative to Positive)
            label (str): "Positive", "Neutral", "Negative"
        """
        if not text:
            return 0.0, "Neutral"
            
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"
            
        return polarity, label
