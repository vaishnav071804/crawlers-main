import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from collections import deque

SEARCH_ENGINE_URL = "https://search.brave.com/search?q={query}&source=web"

async def get_search_result_urls(query: str, max_results=10):
    urls = []
    url = SEARCH_ENGINE_URL.format(query=query.replace(' ', '+'))
    config = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=config, verbose=True) as crawler:
        run_config = CrawlerRunConfig(delay_before_return_html=2)
        result = await crawler.arun(url, config=run_config)

        if not result.success:
            print("Failed to fetch search results:", result.error)
            return urls

        import re
        hrefs = re.findall(r'href="([^"]+)"', result.html)
        for link in hrefs:
            if link.startswith("http"):
                urls.append(link)
            if len(urls) >= max_results:
                break

    return urls

async def main():
    query = "tell about virat kohli"
    print(f"Searching for: {query}")
    seed_urls = await get_search_result_urls(query)

    if not seed_urls:
        print("No search results found, exiting.")
        return

    print(f"Found {len(seed_urls)} URLs from search.")

    visited = set()
    queue = deque(seed_urls)
    index = {}
    max_pages = 20

    async with AsyncWebCrawler(verbose=True) as crawler:
        while queue and len(visited) < max_pages:
            url = queue.popleft()
            if url in visited:
                continue

            result = await crawler.arun(url=url, config=CrawlerRunConfig(respect_robots_txt=True, timeout=20))
            if not result.success:
                print(f"Failed to crawl: {url}")
                continue

            visited.add(url)
            index[url] = result.markdown

            for link in result.links.get("internal", []):
                href = link["href"]
                if href not in visited and href not in queue:
                    queue.append(href)

    for u, md in index.items():
        print(f"---\nURL: {u}\nPreview:\n{md[:200]}...\n")

if __name__ == "__main__":
    asyncio.run(main())
