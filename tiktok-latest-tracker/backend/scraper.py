from playwright.async_api import async_playwright
import asyncio

# In-memory cache to store results for a short period to avoid repeated scrapes for the same query
# This is very basic. For a real app, consider Redis or a more robust caching solution.
RECENT_SEARCHES_CACHE = {}
CACHE_EXPIRY_SECONDS = 300 # 5 minutes

async def scrape_tiktok(query: str):
    print(f"Attempting to scrape TikTok for query: {query}")

    # Check cache first
    if query in RECENT_SEARCHES_CACHE:
        timestamp, cached_results = RECENT_SEARCHES_CACHE[query]
        if (asyncio.get_event_loop().time() - timestamp) < CACHE_EXPIRY_SECONDS:
            print(f"Returning cached results for query: {query}")
            return {"query": query, "results": cached_results, "message": "Data from cache"}
        else:
            print(f"Cache expired for query: {query}")
            del RECENT_SEARCHES_CACHE[query] # Remove expired entry

    results = []
    try:
        async with async_playwright() as p:
            # Launch browser - headless=True is default, good for servers
            # For local dev, you might set headless=False to see the browser
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            page = await browser.new_page()

            search_url = f"https://www.tiktok.com/search/video?q={query}"
            print(f"Navigating to URL: {search_url}")

            await page.goto(search_url, wait_until="networkidle", timeout=60000) # Increased timeout

            # Wait for video items to be present.
            # The selector might change based on TikTok's actual HTML structure.
            # This is a common selector pattern, but it's fragile.
            video_item_selector = "div[data-e2e='search_video-item-list'] > div" # Example selector

            try:
                await page.wait_for_selector(video_item_selector, timeout=30000) # Wait for items to appear
                print("Video items selector found.")
            except Exception as e:
                print(f"Could not find video item selector: {video_item_selector}. Error: {e}")
                # Try to get page content for debugging if selector fails
                page_content = await page.content()
                print(f"Page content length: {len(page_content)}")
                # It's possible no results were found or page structure changed.
                await browser.close()
                return {"query": query, "results": [], "message": f"No video items found with selector or timeout. Page content length: {len(page_content)}"}

            # Extract data - this is highly dependent on TikTok's HTML structure and will likely break.
            # This is a placeholder to demonstrate concept.
            # For a real scraper, you'd need to inspect TikTok's HTML carefully.
            video_elements = await page.query_selector_all(video_item_selector)
            print(f"Found {len(video_elements)} potential video elements.")

            for i, el in enumerate(video_elements[:5]): # Limit to first 5 results for now
                try:
                    # Attempt to extract some text content. This is very generic.
                    # Specific attributes (like href for links, src for images, text from specific sub-elements)
                    # would be targeted in a more robust scraper.

                    # Example: try to get a link if an 'a' tag is within the item
                    link_element = await el.query_selector("a")
                    video_url = await link_element.get_attribute("href") if link_element else "No URL found"

                    # Example: try to get some text, like a caption
                    # This selector needs to be identified from actual TikTok HTML
                    caption_element = await el.query_selector("p[data-e2e='search-video-desc']") # Made-up selector
                    caption = await caption_element.text_content() if caption_element else "No caption found"

                    results.append({
                        "id": f"video_{i+1}",
                        "url": video_url,
                        "caption": caption.strip() if caption else caption,
                        "source": "TikTok Web Scrape (Basic)"
                    })
                except Exception as e:
                    print(f"Error processing video element {i}: {e}")
                    results.append({
                        "id": f"video_{i+1}",
                        "error": f"Could not parse element: {e}",
                        "source": "TikTok Web Scrape (Basic)"
                    })

            await browser.close()

            if results:
                 # Add to cache
                RECENT_SEARCHES_CACHE[query] = (asyncio.get_event_loop().time(), results)
                print(f"Successfully scraped {len(results)} items for query: {query}")
            else:
                print(f"No results extracted for query: {query}, though elements might have been found.")


    except Exception as e:
        print(f"An error occurred during Playwright scraping for query '{query}': {e}")
        # In case of a broader error (e.g., Playwright setup, navigation failed before item search)
        return {"query": query, "error": str(e), "results": [], "message": "Scraping failed with an exception."}

    return {"query": query, "results": results, "message": f"Scraped {len(results)} items from TikTok." if results else "No items scraped or an error occurred."}
