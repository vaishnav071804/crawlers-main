import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def run_brave_search(query: str):
    # 🔁 Use Brave Search's query URL
    url = f"https://search.brave.com/search?q={query}&source=web"

    # 🧑‍💻 Simulate Brave browser using a custom user-agent
    brave_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Brave/123"
    )

    config = BrowserConfig(headless=True, user_agent=brave_user_agent)

    async with AsyncWebCrawler(config=config) as crawler:
        run_config = CrawlerRunConfig(delay_before_return_html=2)
        result = await crawler.arun(url, config=run_config)

        if result.success:
            print("✅ Brave Search page loaded successfully.")
            print(result.html[:1000])  # Preview first 1000 characters of HTML
        else:
            print("❌ Failed to crawl:", result.error)

if __name__ == "__main__":
    query = input("Enter search query: ")
    asyncio.run(run_brave_search(query))
