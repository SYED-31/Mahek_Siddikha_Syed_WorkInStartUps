# Job Scraping and Data Export Project

A comprehensive solution for scraping job listings, extracting details, and exporting to Excel.

## Features

- **Selenium Scraper**: Extracts job links with pagination support
- **Scrapy Spider**: Extracts detailed job information
- **JSON-to-Excel Converter**: Formats data into Excel
- **Automated Workflow**: Single command execution via `main.py`

## Prerequisites

- Python 3.8+
- Google Chrome
- ChromeDriver (auto-managed)

## Installation

```bash
git clone https://github.com/your-username/job-scraping-project.git
cd job-scraping-project
pip install -r requirements.txt
```

## Usage

### Automated Execution
```bash
python main.py
```

### Manual Execution

1. **Selenium Scraper**:
```bash
python selenium_scraper/job_link_scraper.py
```

2. **Scrapy Spider**:
```bash
cd scrapy_project
scrapy crawl job_details
```

3. **JSON to Excel**:
```bash
python json_to_excel.py
```

## Project Structure

```
job-scraping-project/
├── selenium_scraper/
│   ├── job_link_scraper.py
│   └── requirements.txt
├── scrapy_project/
│   ├── scrapy_project/
│   │   ├── spiders/
│   │   │   └── job_details_spider.py
│   │   ├── items.py
│   │   ├── settings.py
│   │   └── __init__.py
│   └── scrapy.cfg
├── output/
│   ├── output.json
│   └── jobs.xlsx
├── temp_job_links.json
├── json_to_excel.py
├── main.py
├── requirements.txt
└── README.md
```

## Error Handling

- Selenium: Handles cookie consent, navigation issues
- Scrapy: Manages extraction failures, missing files
- JSON-to-Excel: Validates input file integrity
- Logging: All components log to separate files

## Troubleshooting

### ChromeDriver Issues
- Verify Chrome installation
- Update Chrome if needed
- Manual ChromeDriver installation: [ChromeDriver](https://sites.google.com/chromium.org/driver/)

### Missing Files
- Verify `temp_job_links.json` before running spider
- Check `output.json` before Excel conversion

### Logs
Check these files for error details:
- `job_link_scraper.log`
- `job_details_spider.log`
- `main.log`

## Tools Used

- Selenium
- Scrapy
- Pandas
- Openpyxl
- Webdriver-manager
- Logging
- Subprocess
