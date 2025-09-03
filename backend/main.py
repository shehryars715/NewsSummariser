import logging
import schedule
import time
from scraper import NewsScraper
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_scraper():
    """Run the news scraper"""
    logger.info("Starting news scraper...")
    
    try:
        scraper = NewsScraper()
        articles = scraper.scrape_all_sources()
        logger.info(f"Scraping completed. Processed {len(articles)} articles.")
        
    except Exception as e:
        logger.error(f"Error in scraper: {e}")

def main():
    """Main function to run the scraper on schedule"""
    # Run immediately on start
    run_scraper()
    
    # Schedule periodic runs
    schedule.every(Config.SCRAPE_INTERVAL_MINUTES).minutes.do(run_scraper)
    
    logger.info(f"Scraper scheduled to run every {Config.SCRAPE_INTERVAL_MINUTES} minutes")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()