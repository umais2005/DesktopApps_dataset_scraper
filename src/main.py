import concurrent.futures
import pandas as pd
from process_data import get_app_info, get_page_links, process_page
from utils import save_json


def main(page_range):
    all_apps = []
    for page_number in page_range:
        page_apps = process_page(page_number)
        all_apps.extend(page_apps)
    save_json(all_apps)


if __name__ == '__main__':
    PAGE_RANGE = range(0,2)
    main(PAGE_RANGE)