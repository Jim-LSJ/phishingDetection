import csv, os
from selenium import webdriver
from selenium import common
import pandas as pd
import time, sys
import data_preprocess

def screen_shot():
    # geckodriver
    driver = webdriver.Firefox(executable_path = os.path.join(".", "geckodriver", "geckodriver"))
    driver.set_page_load_timeout(30)

    urlFiles = pd.read_csv(sys.argv[1])

    urlFiles = urlFiles[["URL", "UUID", "folder"]]
    for idx in range(len(urlFiles)):
        url = urlFiles.loc[idx, "URL"]
        uuid = urlFiles.loc[idx, "UUID"]
        folder = str(urlFiles.loc[idx, "folder"])

        print("\r{}/{}, {}".format(idx, len(urlFiles), url), end="")

        #####################
        # control
        #####################
        # if idx <= 76682:
        #     continue
        # if idx > 7837:
        #     break
        # if folder != "Alexa":
        #     continue
        #####################

        try:
            driver.get(url)
            try:
                os.makedirs(os.path.join("screenshot", folder))
            except:
                pass
            time.sleep(3)
            driver.save_screenshot(os.path.join("screenshot", folder, uuid + ".png"))

            try:
                os.makedirs(os.path.join("html", folder))
            except:
                pass

            html = driver.page_source
            file = open(os.path.join("html", folder, uuid + ".html"), "w")
            file.write(html)
            file.close()

        except KeyboardInterrupt:
            break
        except common.exceptions.TimeoutException:
            print('\n{} Timeout'.format(url))
            continue
        except common.exceptions.NoSuchElementException:
            print('\n{} cannot find code'.format(url))
            continue
        except:
            print("\n{} unknown error".format(url))
            continue



    driver.close()
    return

def main():
    if "screenshot" not in os.listdir("."):
        os.mkdir("screenshot")
    screen_shot()
    print("\nFinish Screen Shot")

if __name__ == '__main__':
    main()

# Usage: python3 code/screenshot.py URL/feature_preprocess.csv