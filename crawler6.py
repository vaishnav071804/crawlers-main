import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from collections import deque

SEED_URLS = {
    "main transport": [
        "https://www.redbus.in/city/goa",
        "https://www.skyscanner.co.in/",
        "https://www.confirmtkt.com/"
    ],
    "stay": [
        "https://www.booking.com/city/in/goa.html"
    ],
    "eat": [
        "https://www.swiggy.com/city/goa",
        "https://www.zomato.com/goa/restaurants"
    ],
    "local transport": [
        "https://www.olacabs.com/",
        "https://www.uber.com/in/en/",
        "https://www.rapido.bike/"
    ]
}

MAX_PAGES_PER_CATEGORY = 3

async def crawl_category(category, seed_urls):
    print(f"Starting crawl for category: {category}")
    visited = set()
    queue = deque(seed_urls)
    collected = []

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
            collected.append({
                "url": url,
                "content": result.markdown[:500]
            })

            for link in result.links.get("internal", []):
                href = link["href"]
                if href not in visited and href not in queue:
                    queue.append(href)

    print(f"Finished crawl for {category}. Pages crawled: {len(visited)}")
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
