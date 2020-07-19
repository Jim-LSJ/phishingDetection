#!/bin/bash

## Phishing
python3 code/check_url.py URL/20200719
python3 code/submit.py URL/20200719/OpenPhish/new_feed.txt
python3 code/submit.py URL/20200719/PhishTank/new_url.txt
python3 code/urlscan_crawler.py URL/20200719/OpenPhish/uuid.txt
python3 code/urlscan_crawler.py URL/20200719/PhishTank/uuid.txt
python3 code/validate_urlscan_files.py urlscan/20200719
python3 code/merge.py URL/20200719 first
python3 code/parse_features.py URL/20200719
python3 code/merge.py URL/20200719 all
