import os, sys
import pandas as pd
from bs4 import BeautifulSoup

df = pd.read_csv(sys.argv[1])

try:
    os.makedirs(os.path.join("examine_screenshot", "sensitive_form"))
    os.makedirs(os.path.join("examine_screenshot", "no_sensitive_form"))
except:
    pass

os.system("rm -r examine_screenshot/sensitive_form/*")
os.system("rm -r examine_screenshot/no_sensitive_form/*")

for i in range(len(df)):
    print("\r{}/{}".format(i, len(df)), end="")
    folder = str(df.loc[i, "folder"])
    uuid = df.loc[i, "UUID"]
    if i >= 400:
        break
    try:
        if df.loc[i, "sensitive_label"] == 1:
            os.system("cp " + os.path.join("screenshot_phishing", "sensitive_form", folder, uuid + ".png") +
                    " " + os.path.join("examine_screenshot", "sensitive_form"))

            os.makedirs(os.path.join("examine_screenshot", "sensitive_form", uuid))
            soup = BeautifulSoup(open(os.path.join("urlscan", folder, uuid, "dom_page.html")).read(), "html.parser")
            html = soup.pre.text
            soup = BeautifulSoup(html, "html.parser")
            html = soup.prettify()
            file = open(os.path.join("examine_screenshot", "sensitive_form", uuid, "dom_page.html"), "w")
            file.write(html)
            file.close()
        else:
            os.system("cp " + os.path.join("screenshot_phishing", "no_sensitive_form", folder, uuid + ".png") +
                    " " + os.path.join("examine_screenshot", "no_sensitive_form"))

            os.makedirs(os.path.join("examine_screenshot", "no_sensitive_form", uuid))
            soup = BeautifulSoup(open(os.path.join("urlscan", folder, uuid, "dom_page.html")).read(), "html.parser")
            html = soup.pre.text
            soup = BeautifulSoup(html, "html.parser")
            html = soup.prettify()
            file = open(os.path.join("examine_screenshot", "no_sensitive_form", uuid, "dom_page.html"), "w")
            file.write(html)
            file.close()
    except KeyboardInterrupt:
        break
    except:
        continue

print("\nEnd examine")

## Usage: python3 code/examine_screenshot.py test.csv