import os, sys
from selenium import webdriver, common

def crawl_website(uuid):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("permissions.default.image",2)
    fp.set_preference("permissions.default.stylesheet",2)

    # geckodriver
    driver = webdriver.Firefox(firefox_profile=fp, executable_path = os.path.join(".", "geckodriver", "geckodriver"))
    driver.set_page_load_timeout(30)

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

uuids = os.listdir('urlscan')
for uuid in uuids:
    if len(os.listdir(os.path.join('urlscan', uuid))) != 5:
        print(uuid)
        crawl_website(uuid)

print("check re-crawl")
for uuid in uuids:
    if len(os.listdir(os.path.join('urlscan', uuid))) != 5:
        print(uuid)

## Usage: python3 validate_urlscan_files.py