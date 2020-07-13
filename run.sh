#!/bin/bash
python3 URL/check_url.py URL/20200713
python3 URL/submit.py URL/20200713/OpenPhish/new_feed.txt
python3 URL/submit.py URL/20200713/PhishTank/new_url.txt
python3 code/urlscan_crawler.py URL/20200713/OpenPhish/uuid.txt
python3 code/urlscan_crawler.py URL/20200713/PhishTank/uuid.txt
python3 code/validate_urlscan_files.py
python3 code/merge.py URL/20200713 first
python3 code/parse_features.py URL/20200713
python3 code/merge.py URL/20200713 all