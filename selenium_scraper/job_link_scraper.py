import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("job_link_scraper.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)
logger = logging.getLogger(__name__)

class JobLinkScraper:
    def __init__(self):
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def get_job_links(self, url, max_pages):
        self.driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Handle the cookie consent banner if it exists
        self.handle_cookie_banner()

        job_links = []
        page_number = 1

        while True:
            logger.info(f"Scraping page {page_number}...")

            # Extract job links from the current page
            try:
                jobs = self.driver.find_elements(By.CSS_SELECTOR, 'h2.font-bold a')
                for job in jobs:
                    job_links.append(job.get_attribute('href'))
            except Exception as e:
                logger.error(f"Error extracting job links: {e}")
                break

            # Stop if the user-specified page limit is reached
            if max_pages != "max" and page_number >= int(max_pages):
                logger.info(f"Reached the page limit ({max_pages}). Stopping.")
                break

            # Check for the "Next" button and click it
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'a.flex-auto.lg\\:inline-block.px-3.leading-10.border.border-wis-grey-light.border-wis-orange.bg-white.text-wis-black.rounded-lg.hover\\:bg-wis-orange.hover\\:border-wis-orange.md\\:ml-1')
                
                # Scroll the "Next" button into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                time.sleep(1)  # Wait for scrolling to complete

                # Click the "Next" button using ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element(next_button).click().perform()
                time.sleep(5)  # Wait for the next page to load
                page_number += 1
            except NoSuchElementException:
                logger.info("No more pages.")
                break
            except ElementClickInterceptedException as e:
                logger.error(f"Failed to click the 'Next' button: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                break

        self.driver.quit()

        # Save job links to a temporary file
        try:
            with open("temp_job_links.json", "w") as f:
                json.dump(job_links, f)
            logger.info(f"Saved {len(job_links)} job links to temp_job_links.json")
        except Exception as e:
            logger.error(f"Error saving job links to file: {e}")

        return job_links

    def handle_cookie_banner(self):
        try:
            # Locate and close the cookie consent banner
            cookie_banner = self.driver.find_element(By.ID, 'cookiescript_rightpart')
            if cookie_banner:
                close_button = self.driver.find_element(By.CSS_SELECTOR, '#cookiescript_close')
                close_button.click()
                time.sleep(1)  # Wait for the banner to close
                logger.info("Closed the cookie consent banner.")
        except NoSuchElementException:
            logger.info("No cookie consent banner found.")
        except Exception as e:
            logger.error(f"Error handling cookie banner: {e}")

# Get user input for the number of pages to scrape
def get_user_input():
    while True:
        user_input = input("Enter the number of pages to scrape (from 1 to 20): ").strip().lower()
        if user_input == "max" or user_input.isdigit():
            return user_input
        print("Invalid input. Please enter a number or 'max'.")

# Example usage
if __name__ == "__main__":
    try:
        scraper = JobLinkScraper()
        max_pages = get_user_input()  # Get user input
        job_links = scraper.get_job_links("https://workinstartups.com/search?f=7&loc=86383", max_pages)
        logger.info(f"Extracted {len(job_links)} job links.")
    except Exception as e:
        logger.error(f"Script failed with error: {e}")