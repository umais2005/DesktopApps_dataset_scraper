import json
import os
import asyncio

def save_json(apps, page_number=None, by_page=False):
    if by_page:
        directory = '../data/raw/by_pages/'
        filename = f'{directory}page_{page_number}_apps.json'
    else:
        directory = '../data/raw'
        filename = f'{directory}/apps.json'
    os.makedirs(directory, exist_ok=True)
    # Write the apps to a JSON file
    with open(filename, 'w') as f:
        json.dump(apps, f, indent=4)
    if filename:
        return filename
    return None

async def save_json_async(apps, page_number, by_page=False):
    if by_page:
        directory = '../data/raw/by_pages/'
        filename = f'{directory}page_{page_number}_apps.json'
    else:
        directory = '../data/raw'
        filename = f'{directory}/apps.json'
    os.makedirs(directory, exist_ok=True)
    # Write the apps to a JSON file
    with open(filename, 'w') as f:
        json.dump(apps, f, indent=4)
    if filename:
        return filename
    return None