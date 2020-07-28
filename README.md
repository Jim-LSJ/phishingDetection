# Phishing Detection

# Data now
1. Phishing: 
      20200702_1
      20200702_2
      20200702_3
      20200710
      20200711
      20200712
      20200713
      20200714
      20200717
      20200719
      20200720
      20200722
      20200723
      20200724
      20200727
      20200728 (doing all now)

2. CommonCrawl:
      CommonCrawl_0
      CommonCrawl_1
      CommonCrawl_2
      CommonCrawl_3
      CommonCrawl_4
      CommonCrawl_5
      CommonCrawl_6
      CommonCrawl_7
      CommonCrawl_8
      CommonCrawl_9
      CommonCrawl_10
      CommonCrawl_11
      CommonCrawl_12 (already parsed but not merged all)
      CommonCrawl_13 (already parsed but not merged all)
      CommonCrawl_14 (already parsed but not merged all)
      CommonCrawl_15 (already parsed but not merged all)
      CommonCrawl_16 (already parsed but not merged all)
      CommonCrawl_17 (already parsed but not merged all)
      CommonCrawl_18 (already crawled and parsing now)
      CommonCrawl_19 (already crawled and parsing now)

# Folders
1. code folder includes all code
2. geckodriver folder include the geckodriver for firefox (used while collecting data from browser)
3. phishingDetection-env folder include the virtual environment created by python3 -m virtualenv
  You can use `source phisihngDetection-env/bin/activate` to get into this virtual environment and get out by `deactivaet`
4. URL folder include the <b>url, uuid, feature.csv</b> for each folder

# Crawl data
## Common Crawl
- `bash commoncrawl.sh` is the data collecting flow in this project.
1. `python3 code/submit.py <URL/CommonCrawl_5/url.txt>`: submit the urls to urlscan and record the success uuid in uuid.txt under the same folder
2. `python3 code/urlscan_crawler.py URL/CommonCrawl_5/uuid.txt`: collect all urlscan html files of each uuid in uuid.txt
3. `python3 code/validate_urlscan_files.py urlscan/CommonCrawl_5`: recollect the missing html files in step 2
4. `python3 code/merge.py URL/CommonCrawl_5 benign`: create the <b>feature.csv</b> and write the uuid and label in it
5. `python3 code/parse_features.py URL/CommonCrawl_5`: parse features from urlscan html files and store in feature.csv
6. `python3 code/merge.py URL/CommonCrawl_5 all`: merge URL/CommonCrawl_5/feature.csv to URL/feature.csv

## Phishing
- `bash run.sh` is the collecting flow in this project
1. `python3 code/check_url.py URL/20200719`: check the unique urls in PhishTank/verified.csv and OpenPhish/url.txt by comparing to URL/feature.csv
2-1. `python3 code/submit.py URL/20200719/OpenPhish/new_feed.txt`: submit the urls to urlscan
2-2. `python3 code/submit.py URL/20200719/PhishTank/new_url.txt`: submit the urls to urlscan
3-1. `python3 code/urlscan_crawler.py URL/20200719/OpenPhish/uuid.txt`: collect urlscan html files
3-2. `python3 code/urlscan_crawler.py URL/20200719/PhishTank/uuid.txt`: collect urlscan html files
4. `python3 code/validate_urlscan_files.py urlscan/20200719`: recollect the missing html files in step 2
5. `python3 code/merge.py URL/20200719 phishing`: merge OpenPhish/uuid.txt and PhishTank/uuid.txt and store in feature.csv
6. `python3 code/parse_features.py URL/20200719`: parse features from urlscan html files and store in feature.csv
7. `python3 code/merge.py URL/20200719 all`: merge URL/20200719/feature.csv to URL/feature.csv

# Important Files
1. URL/feature.csv: store all data and feature now existed, you can use the uuid to find the html files in urlscan/<date>/<uuid>
2. URL/<date>/feature.csv: store the data of that date
3. urlscan/<date>/<uuid>/: store five result html files of that uuid
3-1. urlscan/<date>/<uuid>/result_page.html: store the result
3-2. urlscan/<date>/<uuid>/dom_page.html: store the DOM page of urlscan, you can take code/DOM_graph.py as reference to understand how to parse and generate a graph

# You may need to do
1. Download the html files from https://drive.google.com/drive/u/1/folders/1wpvg2rYCsn0UF6OEFZiutZoIUU1e8AR_ , and unzip them (about 30GB maybe)
2. Put the flies to the path phishingDetection/urlscan/<date folder>
    ![](https://i.imgur.com/TT8VCco.png)
    
    ![](https://i.imgur.com/0fvJXG0.png)
3. Parse the urlscan/<date>/<uuid>/dom_page.html, where date and uuid are in URL/feature.csv or URL/<date>/feature.csv

4. continue step 3, construct the graph. You can reference code/DOM_graph.py (需要修改，因為那時候資料還沒有分日期存)
