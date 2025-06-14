from fastapi import FastAPI
# Ensure the import path is correct for the scraper module.
# If scraper.py is in the same directory (backend), it should be:
from scraper import scrape_tiktok

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "TikTok Latest Tracker Backend"}

@app.get("/search")
async def search_videos(q: str = None): # Added default None for q
    '''
    Searches for TikTok videos based on a query.
    Calls the scraper function and returns its results.
    '''
    if not q:
        # Return a 400 Bad Request if q is missing
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Search query 'q' is required.")

    results = await scrape_tiktok(q)
    return results

# To run this app (from the backend directory):
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
