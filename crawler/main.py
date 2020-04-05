import time
import schedule
import logging

from src.crawler import crawling


if __name__ == "__main__":

    # Set logger
    logger = logging.getLogger("blueblue")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Set schedule
    schedule.every().day.at("12:00").do(crawling)

    while True:
        logger.info("Check crawling schedule...")
        schedule.run_pending()
        time.sleep(600)
