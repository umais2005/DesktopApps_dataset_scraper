import json
import os

def save_json(apps, page_number=None, by_page=False):
    directory = 'data/raw'
    if by_page:
        filename = f'{directory}/by_pages/page_{page_number}_apps.json'
    else:
        filename = f'{directory}/apps.json'
    # Write the apps to a JSON file
    with open(filename, 'w') as f:
        json.dump(apps, f, indent=4)
    if filename:
        return filename
    return None