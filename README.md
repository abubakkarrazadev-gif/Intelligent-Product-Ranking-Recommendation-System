# Intelligent Product Ranking & Recommendation System

## Overview
An end-to-end Machine Learning system that leverages real-time e-commerce data to score, rank, and recommend products.

## Architecture
- **Data Source**: Real-Time Amazon Data API (RapidAPI)
- **Backend**: FastAPI
- **ML Engine**: Scikit-Learn, XGBoost, TextBlob (Sentiment)

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables:
   - Create `.env` file
   - Add `RAPIDAPI_KEY=your_key_here`

## Running the API
```bash
uvicorn app.main:app --reload
```
