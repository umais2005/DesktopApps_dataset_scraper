from process_data import process_page
from utils import save_json
import config

def main(page_range):
    all_apps = []
    for page_number in page_range:
        page_apps = process_page(page_number)
        all_apps.extend(page_apps)
        save_json(all_apps)


if __name__ == '__main__':
    page_range = config.PAGE_RANGE
    main(page_range)