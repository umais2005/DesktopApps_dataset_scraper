from process_data import process_page
from utils import save_json
import config
import concurrent.futures
import time

def main(page_range):
    all_apps = []
    for page_number in page_range:
        page_apps = process_page(page_number)
        all_apps.extend(page_apps)
        save_json(all_apps)

def concurrent_main(first_page, last_page):
    all_apps = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        # Submit each page processing task and collect futures
        futures = [executor.submit(process_page, page_num) for page_num in range(first_page, last_page+1)]
        
        # Gather results from futures as they complete
        for future in concurrent.futures.as_completed(futures):
            page_apps = future.result()
            all_apps.extend(page_apps)
    
    save_json(all_apps)

if __name__ == '__main__':
    PAGE_RANGE = config.PAGE_RANGE
    start_time = time.time()
    concurrent_main(first_page=1636, last_page=1638)
    
    print(f"Total time taken: {time.time() - start_time:.2f} seconds")