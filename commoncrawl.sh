#!/bin/bash

## CommonCrawl
python3 code/submit.py URL/CommonCrawl_5/url.txt
python3 code/urlscan_crawler.py URL/CommonCrawl_5/uuid.txt
python3 code/validate_urlscan_files.py urlscan/CommonCrawl_5
python3 code/merge.py URL/CommonCrawl_5 benign
python3 code/parse_features.py URL/CommonCrawl_5
# python3 code/merge.py URL/CommonCrawl_5 all