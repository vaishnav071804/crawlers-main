import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from collections import deque
SEED_URLS = ["https://www.ms-dhoni.com"]
MAX_PAGES = 20  
async def main():
    visited = set()
    queue = deque(SEED_URLS)
    index = {}  

    async with AsyncWebCrawler(verbose=False) as crawler:
        while queue and len(visited) < MAX_PAGES:
            url = queue.popleft()
            if url in visited:
                continue

            result = await crawler.arun(url=url, config=CrawlerRunConfig())

            if not result.success:
                continue

            visited.add(url)
            index[url] = result.markdown

            for link in result.links.get("internal", []):
                href = link["href"]
                if href not in visited and href not in queue:
                    queue.append(href)

    for u, md in index.items():
        print(f"---\nURL: {u}\nContent Preview:\n{md[:200]}...\n")

if __name__ == "__main__":
    asyncio.run(main())
