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
        print("{}/{}, {}".format(idx, len(uuidFile), uuid))
        #####################
        # control
        #####################
        # if idx <= 7834:
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
                print('{} Timeout'.format(url))
                continue
            except common.exceptions.NoSuchElementException:
                print('{} cannot find code'.format(url))
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

            if uuid not in os.listdir("urlscan"):
                os.makedirs(os.path.join("urlscan", uuid))
            file = open(os.path.join("urlscan", uuid, key + ".html"), "w+")
            file.write(driver.page_source)
            file.close()

    driver.close()
    return

def main():
    if 'urlscan' not in os.listdir('.'):
        os.mkdir('urlscan')
    crawl_urlscan()

if __name__ == '__main__':
    main()


#### clone a website
# from pywebcopy import save_webpage
# url = 'http://some-site.com/some-page.html'
# download_folder = '/path/to/downloads/'    
# kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name'}
# save_webpage(url, download_folder, **kwargs)


## usage python3 urlscan_crawler.py uuid.csv

## uuid.csv must have a column named UUID

## Results
## urlscan/
## urlscan/uuid
## urlscan/uuid/result_page.html
## urlscan/uuid/related_page.html
## urlscan/uuid/dom_page.html
## urlscan/uuid/content_page.html
## urlscan/uuid/api_page.html