"""
Twitter Trends Scraper
----------------------
This script automates the process of logging into Twitter/X, fetching top trending topics,
and storing them in MongoDB. It uses Selenium for web automation and includes proxy support
and headless browser operation.

Requirements:
- Selenium WebDriver
- MongoDB
- Python-dotenv
- Chrome WebDriver
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import time 
import uuid
import requests
import logging
import os 

# Load environment variables from .env file
load_dotenv()

# Initialize WebDriver with Chrome service
WEBDRIVER = os.environ.get('CHROME_WEBDRIVER')  
service = Service(WEBDRIVER)
driver = webdriver.Chrome(service=service)

# Configure logging to track script execution
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s - %(message)s")

# Load configuration from environment variables
MONGO_URI = os.environ.get('MONGODB_URL')
USERNAME = os.environ.get('X_USERNAME')
PASSWORD = os.environ.get('X_PASSWORD')
EMAIL = os.environ.get('X_EMAIL')  
PROXY = os.environ.get('PROXY')

# Initialize MongoDB connection
client = MongoClient(MONGO_URI)
db = client.get_database("mydatabase")
collection = db.get_collection("trending_topics")

# Configure Chrome options for headless operation and proxy support
options = Options()
options.add_argument(f"--proxy-server={PROXY}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

def fetch_trends():
    """
    Fetches the top 5 trending topics from Twitter/X.
    
    This function performs the following steps:
    1. Logs into Twitter using provided credentials
    2. Navigates to the Explore section
    3. Extracts trending topics from the trends container
    4. Filters out unwanted text and formats the trends
    
    Returns:
        list: A list of trending topics, where each trend is represented as a list of related text
    
    Raises:
        Exception: Any unexpected errors during the scraping process
    """
    try:
        # Navigate to login page and wait for username field
        logging.info("Navigating to Twitter login page...")
        driver.get("https://x.com/i/flow/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'text')))

        # Enter username and proceed
        logging.info("Locating username field...")
        username = driver.find_element(By.NAME, 'text')
        username.send_keys(USERNAME)

        logging.info("Clicking Next button after entering username...")
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()

        # Wait for and enter password
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        logging.info("Entering password...")
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(PASSWORD)

        logging.info("Clicking Login button after entering password...")
        login_button = driver.find_element(By.XPATH, "//span[text()='Log in']")
        login_button.click()

        # Navigate to explore section
        logging.info("Waiting for explore section...")
        explore_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]'))
        )
        explore_button.click()

        # Extract trending topics
        logging.info("Fetching trending section...")
        trends_container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//section[contains(@aria-labelledby, 'accessible-list')]"))
        )
        trend_items = trends_container.find_elements(By.XPATH, ".//div[contains(@data-testid, 'trend')]")

        # Process and filter trends
        top_trends = []
        unwanted_texts = {'.', 'Trending in India'}  # Texts to filter out from trends
        for item in trend_items[:5]:
            try:
                span_tags = item.find_elements(By.XPATH, ".//span")
                trend_texts = [span.text.strip() for span in span_tags if span.text.strip() not in unwanted_texts]
                if trend_texts:
                    top_trends.append(trend_texts)
            except Exception as trend_extraction_error:
                logging.warning(f"Could not extract trend text for an item: {trend_extraction_error}")

        logging.info(f"Top 5 trends fetched: {top_trends}")
        return top_trends

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise  # Re-raise the exception after logging
    finally:
        driver.quit()

if __name__ == "__main__":
    # Execute trend fetching and store results in MongoDB
    top_trends = fetch_trends()
    
    # Prepare document for MongoDB storage
    document = {
        "datetime": datetime.now().isoformat(),
        "trends": [
            trend[1] if len(trend) > 1 else "N/A"
            for trend in top_trends
        ],
        "ip_address": requests.get("https://api.ipify.org").text  # Get current IP address
    }
    
    # Insert document into MongoDB
    collection.insert_one(document)
    logging.info("Data inserted into MongoDB successfully.")
