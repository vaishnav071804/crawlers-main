import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from collections import deque

SEED_URLS = {
    "main transport": [
        "https://www.redbus.in/",
        "https://www.skyscanner.co.in/",
        "https://www.confirmtkt.com/"
    ],
    "stay": [
        "https://www.booking.com/city/in/new-delhi.html"
    ],
    "eat": [
        "https://www.swiggy.com/city/delhi",
        "https://www.zomato.com/delhi/restaurants"
    ],
    "local transport": [
        "https://www.olacabs.com/",
        "https://www.uber.com/in/en/",
        "https://www.rapido.bike/"
    ]
}

# Define keyword filters for each category
CATEGORY_FILTERS = {
    "stay": ["budget", "cheap", "hotel", "guest house"],
    "eat": ["restaurant", "food", "delivery", "cuisine"],
    "local transport": ["ride", "bike", "cab", "auto"],
    "main transport": ["bus", "train", "flight", "ticket", "booking"]
}

MAX_PAGES_PER_CATEGORY = 3

def content_matches_filter(content, filters):
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in filters)

async def crawl_category(category, seed_urls):
    print(f"Starting crawl for category: {category}")
    visited = set()
    queue = deque(seed_urls)
    collected = []

    filters = CATEGORY_FILTERS.get(category, [])

    async with AsyncWebCrawler(verbose=False) as crawler:
        while queue and len(visited) < MAX_PAGES_PER_CATEGORY:
            url = queue.popleft()
            if url in visited:
                continue

            result = await crawler.arun(url=url, config=CrawlerRunConfig())

            if not result.success:
                print(f"Failed to crawl {url}")
                continue

            visited.add(url)

            # Apply content filter
            if content_matches_filter(result.markdown, filters):
                collected.append({
                    "url": url,
                    "content": result.markdown[:500]
                })

            # Enqueue internal links for crawling
            for link in result.links.get("internal", []):
                href = link["href"]
                if href not in visited and href not in queue:
                    queue.append(href)

    print(f"Finished crawl for {category}. Pages crawled: {len(visited)} | Collected: {len(collected)}")
    return collected

async def main():
    results = {}
    for category, urls in SEED_URLS.items():
        results[category] = await crawl_category(category, urls)

    for category, items in results.items():
        print(f"\n--- Category: {category} ---")
        for item in items:
            print(f"URL: {item['url']}")
            print(f"Preview:\n{item['content'][:200]}...\n")

if __name__ == "__main__":
    asyncio.run(main())
 