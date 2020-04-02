import time
import schedule

from src.crawler import crawling


if __name__ == "__main__":
    schedule.every().day.at("12:00").do(crawling)

    while True:
        print("Check crawling schedule...")
        schedule.run_pending()
        time.sleep(10)
