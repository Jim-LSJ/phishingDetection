#!/bin/bash

## Phishing
# python3 code/check_url.py URL/20200731
# python3 code/submit.py URL/20200731/OpenPhish/new_feed.txt
# python3 code/submit.py URL/20200731/PhishTank/new_url.txt
# python3 code/urlscan_crawler.py URL/20200731/OpenPhish/uuid.txt
# python3 code/urlscan_crawler.py URL/20200731/PhishTank/uuid.txt
# python3 code/validate_urlscan_files.py urlscan/20200731
# python3 code/merge.py URL/20200731 first
# python3 code/parse_features.py URL/20200731
# python3 code/merge.py URL/20200731 all



python3 code/parse_features.py URL/20200731
echo finish31

python3 code/parse_features.py URL/Alexa
echo finish Alexa