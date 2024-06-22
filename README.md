# DesktopApps_dataset_scraper

This app scrapes all of over 10000 desktop apps published (available from getintopc.com) and saves them in json format page by page and altogether.

This has been made using Python and its libraries like Beautifulsoup, Playwright, json, logging, re.

Project Structure:

- **data/**: Contains raw, processed data, and logs.
- **notebooks/**: Jupyter notebooks for data analysis and experimentation.
- **src/**: Source code of the project.
  - `main.py`: The main script to run the project.
  - `fetch_html.py`: Module to fetch HTML using Playwright.
  - `process_data.py`: Module to process data.
  - `utils.py`: Utility functions.
  - `config.py`: Configuration settings.
- **.gitignore**: Specifies files and directories to ignore in git.
- **requirements.txt**: Lists project dependencies.
- **README.md**: Project overview and setup instructions.
- **.env**: Environment variables file (not to be committed to version control).