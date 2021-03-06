import csv, os
from selenium import webdriver
from selenium import common
import pandas as pd
import time, sys

def crawl_urlscan():
    # browser settings
    # dismiss loading image and css to boost crawling
    fp = webdriver.FirefoxProfile()
    fp.set_preference("permissions.default.image",2)
    fp.set_preference("permissions.default.stylesheet",2)

    # geckodriver
    driver = webdriver.Firefox(firefox_profile=fp, executable_path = os.path.join(".", "geckodriver", "geckodriver"))
    driver.set_page_load_timeout(10)

    uuidFile = pd.read_csv(sys.argv[1])
    uuids = uuidFile["UUID"]
    for idx, uuid in enumerate(uuids.values):
        print("\r{}/{}, {}".format(idx, len(uuidFile), uuid), end="")
        #####################
        # control
        #####################
        # if idx <= 4844:
        #     continue
        # if idx > 7837:
        #     break
        #####################
        urls = {
                "result_page": "https://urlscan.io/result/" + uuid, 
                "related_page": "https://urlscan.io/result/" + uuid + "/related/",  
                "dom_page": "https://urlscan.io/dom/" + uuid,
                "content_page": "https://urlscan.io/result/" + uuid + "/content/",
                "api_page": "https://urlscan.io/api/v1/result/" + uuid
                }

        for key, url in urls.items():
            try:
                driver.get(url)
            except common.exceptions.TimeoutException:
                print('\n{} Timeout'.format(url))
                continue
            except common.exceptions.NoSuchElementException:
                print('\n{} cannot find code'.format(url))
                continue
            
            ####################################
            # wait for dynamically loading html
            ####################################
            # tic = time.clock()
            # flag = 0
            # while not code.text:
            #     toc = time.clock()
            #     if toc - tic > 10:
            #         flag = 1
            #         break
            # if flag:
            #     print('{} js loading fail'.format(url))
            #     continue
            ####################################

            try:
                os.makedirs(os.path.join("urlscan", sys.argv[1].split("/")[1], uuid))
            except:
                pass

            file = open(os.path.join("urlscan", sys.argv[1].split("/")[1], uuid, key + ".html"), "w+")
            file.write(driver.page_source)
            file.close()

    driver.close()
    return

def main():
    if 'urlscan' not in os.listdir('.'):
        os.mkdir('urlscan')
    crawl_urlscan()
    print("\nFinish Crawl")

if __name__ == '__main__':
    main()



## usage python3 code/urlscan_crawler.py URL/CommonCrawl_3/uuid.txt

## uuid.csv must have a column named UUID

## Results
## urlscan/
## urlscan/uuid
## urlscan/uuid/result_page.html
## urlscan/uuid/related_page.html
## urlscan/uuid/dom_page.html
## urlscan/uuid/content_page.html
## urlscan/uuid/api_page.html