from textblob import TextBlob

class SentimentModel:
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
