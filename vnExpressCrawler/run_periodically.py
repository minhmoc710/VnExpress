import os
import time
try:
    while True:
        os.system("cd vnExpressCrawler")
        os.system("scrapy crawl update_periodically")
        time.sleep(10)
except KeyboardInterrupt:
    print("Crawler stopped becaused of Keyboard Interuption")
