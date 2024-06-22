import json
import os

def save_html(html_content):
    with open('../data/logging/', 'w', encoding='utf-8') as file:
        file.write(html_content)
        file.close()


def save_json(apps, page_number, by_page=True):
    directory = 'data/raw'
    if by_page:
        filename = f'{directory}/by_pages/page_{page_number}_apps.json'
    else:
        filename = f'{directory}/apps.json'
    # Write the apps to a JSON file
    with open(filename, 'w') as f:
        json.dump(apps, f, indent=4)

    print(f"Data successfully written to {filename}")