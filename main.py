import subprocess
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("main.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)
logger = logging.getLogger(__name__)

def run_selenium_scraper():
    """Run the Selenium scraper to extract job links."""
    try:
        logger.info("Running Selenium scraper...")
        subprocess.run(["python", "selenium_scraper/job_link_scraper.py"], check=True)
        logger.info("Selenium scraper completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Selenium scraper failed: {e}")
        raise

def run_scrapy_spider():
    """Run the Scrapy spider to extract job details."""
    try:
        logger.info("Running Scrapy spider...")
        os.chdir("scrapy_project")  # Change to the Scrapy project directory
        subprocess.run(["scrapy", "crawl", "job_details"], check=True)
        os.chdir("..")  # Return to the root directory
        logger.info("Scrapy spider completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Scrapy spider failed: {e}")
        raise

def run_json_to_excel():
    """Convert the JSON output to an Excel file."""
    try:
        logger.info("Converting JSON to Excel...")
        subprocess.run(["python", "convert.py"], check=True)
        logger.info("JSON-to-Excel conversion completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"JSON-to-Excel conversion failed: {e}")
        raise

def main():
    """Main function to execute all steps in order."""
    try:
        # Step 1: Run the Selenium scraper
        run_selenium_scraper()

        # Step 2: Run the Scrapy spider
        run_scrapy_spider()

        # Step 3: Convert JSON to Excel
        run_json_to_excel()

        logger.info("All steps completed successfully. Final Excel file saved as output/jobs.xlsx.")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()