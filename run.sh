#!/bin/bash

## Phishing
# python3 code/check_url.py URL/20200827
# python3 code/submit.py URL/20200730/OpenPhish/new_feed.txt
# python3 code/submit.py URL/20200827/PhishTank/new_url.txt
# python3 code/urlscan_crawler.py URL/20200827/OpenPhish/uuid.txt
# python3 code/urlscan_crawler.py URL/20200827/PhishTank/uuid.txt
# python3 code/validate_urlscan_files.py urlscan/20200827
# python3 code/merge.py URL/20200730 first
# python3 code/parse_features.py URL/20200730
# python3 code/merge.py URL/20200730 all

# python3 code/phishtank_newdata.py URL/20200830/PhishTank
# python3 code/submit.py URL/20200830/PhishTank/new_url.txt
# python3 code/urlscan_crawler.py URL/20200830/PhishTank/uuid.txt
# python3 code/validate_urlscan_files.py urlscan/20200830
# python3 code/merge.py URL/20200830 phishtank
# python3 code/parse_features.py URL/20200830
# python3 code/screenshot.py URL/20200830/feature.csv

python3 code/drop_expired.py URL/20200831/feature.csv
python3 code/hash_near_duplicate.py URL/20200831/feature.csv
python3 code/detect_sensitive.py URL/20200831/feature.csv
python3 code/newdata_result.py URL/20200831/feature.csv

# 4.sensitive_result需要把screenshot檔名改掉，要先弄object_detection

# 2.sensitive_result用在CommonCrawl之前，要先根據feature.csv中的object_detection，把screenshot中的圖片複製到label資料夾