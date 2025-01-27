import scrapy
from scrapy.http import HtmlResponse
from scrapy_project.items import JobItem
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("job_details_spider.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)
logger = logging.getLogger(__name__)

class JobDetailsSpider(scrapy.Spider):
    name = "job_details"
    custom_settings = {
        "FEEDS": {
            "output/output.json": {
                "format": "json",  # Save output in JSON format
                "encoding": "utf8",  # Use UTF-8 encoding
                "indent": 4,  # Pretty-print the JSON with indentation
                "overwrite": True,  # Overwrite the file if it already exists
            },
        }
    }

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def start_requests(self):
        # Read job links from the temporary file
        try:
            with open("../../../temp_job_links.json", "r") as f:
                job_links = json.load(f)
            logger.info(f"Loaded {len(job_links)} job links from temp_job_links.json")
        except FileNotFoundError:
            logger.error("File 'temp_job_links.json' not found. Please run the Selenium scraper first.")
            return
        except Exception as e:
            logger.error(f"Error loading job links: {e}")
            return

        for link in job_links:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        try:
            # Use Selenium to load the job detail page
            self.driver.get(response.url)
            time.sleep(5)  # Wait for the page to load

            # Pass the rendered page source to Scrapy
            rendered_page = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=rendered_page, encoding='utf-8')

            # Extract job details with error handling
            item = JobItem()
            item["job_title"] = response.css('section.pb-4.flex.gap-1.mb-2 h1.leading-none.mr-3.text-2xl.md\\:text-3xl::text').get(default="N/A").strip()
            logger.info(f"Job Title: {item['job_title']}")

            item["company_name"] = response.css('section.mb-4 div.md\\:flex.md\\:items-center div.ui-job-card-info.flex-1.grid.md\\:grid-flow-col.md\\:grid-cols-2.md\\:grid-rows-3.gap-3 div.ui-company span.text-wis-black::text').get(default="N/A").strip()
            logger.info(f"Company Name: {item['company_name']}")

            item["location"] = response.css('section.mb-4 div.md\\:flex.md\\:items-center div.ui-job-card-info.flex-1.grid.md\\:grid-flow-col.md\\:grid-cols-2.md\\:grid-rows-3.gap-3 div.ui-location span::text').get(default="N/A").strip()
            logger.info(f"Location: {item['location']}")

            item["job_type"] = response.css('section.mb-4 div.md\\:flex.md\\:items-center div.ui-job-card-info.flex-1.grid.md\\:grid-flow-col.md\\:grid-cols-2.md\\:grid-rows-3.gap-3 div.ui-contract-time::text').get(default="N/A").strip()
            logger.info(f"Job Type: {item['job_type']}")

            # Extract Job Description
            description_paragraphs = response.css('section.mb-4 section.adp-body.mb-4.text-sm.md\\:text-base.md\\:mb-0 p::text').getall()
            item["job_description"] = " ".join(description_paragraphs).strip() if description_paragraphs else "N/A"
            logger.info(f"Job Description: {item['job_description']}")

            # Extract Email from Job Description
            item["email"] = self.extract_email(description_paragraphs)
            logger.info(f"Email: {item['email']}")

            # Extract Application Link
            item["application_link"] = response.css('section.mb-4 a.border.border-solid.leading-10.font-semibold.px-4.rounded-md.text-center.text-white.border-adzuna-green-500.bg-adzuna-green-500.hover\\:bg-adzuna-green-600.hover\\:border-adzuna-green-600.active\\:border-adzuna-green-700.active\\:bg-adzuna-green-700.bg-wis-black.hover\\:bg-wis-orange-dark.hover\\:text-wis-black.border-0.text-center.block.my-4.md\\:inline-block::attr(href)').get(default="N/A")
            logger.info(f"Application Link: {item['application_link']}")

            yield item
        except Exception as e:
            logger.error(f"Error parsing job details: {e}")

    def extract_email(self, paragraphs):
        try:
            # Define the regex pattern for emails
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

            # Search for emails in each paragraph
            for paragraph in paragraphs:
                match = re.search(email_pattern, paragraph)
                if match:
                    return match.group(0)  # Return the first email found

            return "N/A"  # Return "N/A" if no email is found
        except Exception as e:
            logger.error(f"Error extracting email: {e}")
            return "N/A"

    def closed(self, reason):
        try:
            # Close the Selenium WebDriver when the spider is done
            self.driver.quit()
            logger.info("Selenium WebDriver closed.")
        except Exception as e:
            logger.error(f"Error closing Selenium WebDriver: {e}")