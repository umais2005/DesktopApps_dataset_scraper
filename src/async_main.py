import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from process_data import get_page_links, get_app_info
from utils import save_json  # Replace with actual module

# Convert get_page_links and get_app_info to async if they are not already
async def get_page_links_async(page_number):
    return get_page_links(page_number)

async def get_app_info_async(link, cat, img_link):
    return get_app_info(link, cat, img_link)

async def process_page(page_number):
    page_apps = []
    links, categories, img_links = await get_page_links_async(page_number)
    
    if bool(links):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            tasks = [
                loop.run_in_executor(executor, get_app_info, link, cat, img_link)
                for link, cat, img_link in zip(links, categories, img_links)
            ]
            results = await asyncio.gather(*tasks)
            page_apps.extend(results)
    
    filename = save_json([page_app for page_app in page_apps if page_app], page_number, by_page=True)
    if filename: logging.info(f"Data successfully written to {filename}\n")
    
    return page_apps

async def process_pages_concurrently(page_range):
    all_apps = []
    tasks = [process_page(page_num) for page_num in page_range]
    results = await asyncio.gather(*tasks)
    for result in results:
        all_apps.extend(result)
    save_json(all_apps)

async def main():
    page_range = range(5)  # Example page range
    await process_pages_concurrently(page_range)

if __name__ == "__main__":
    asyncio.run(main())