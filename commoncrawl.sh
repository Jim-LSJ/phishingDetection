#!/bin/bash

## CommonCrawl
# python3 code/submit.py URL/CommonCrawl_12/url.txt
# python3 code/urlscan_crawler.py URL/CommonCrawl_12/uuid.txt
# python3 code/validate_urlscan_files.py urlscan/CommonCrawl_12
# python3 code/merge.py URL/CommonCrawl_12 benign
# python3 code/parse_features.py URL/CommonCrawl_12
# python3 code/merge.py URL/CommonCrawl_5 all

python3 code/validate_urlscan_files.py urlscan/CommonCrawl_18
python3 code/merge.py URL/CommonCrawl_18 benign
python3 code/parse_features.py URL/CommonCrawl_18
echo 18Finish

python3 code/validate_urlscan_files.py urlscan/CommonCrawl_19
python3 code/merge.py URL/CommonCrawl_19 benign
python3 code/parse_features.py URL/CommonCrawl_19
echo 19Finish