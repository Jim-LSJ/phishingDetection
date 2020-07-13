#!/bin/bash
# Program:
#   This program control the whole project
# History:
# 2020/07/07 First version
usage() {
    echo -e "bash main.sh -r check_url -date <URL/20200710>"
    echo -e "bash main.sh -r submit_url -url <URL/CommonCrawl/url.txt>"
    echo -e "bash main.sh -r urlscan_result -uuid <URL/CommonCrawl/uuid.txt>"
    echo -e "bash main.sh -r validate_urlscan"
    echo -e "bash main.sh -r merge_csv -date <URL/20200710>"
    echo -e "bash main.sh -r parse_feature -date <URL/20200710>"
    echo -e "bash main.sh -r generate_DOM_graph -uuid <URL/OpenPhish/uuid.txt>"
}

while getopts r:url:uuid:date:? argv
do
    case $argv in
        r) RUN=$OPTARG;;
        url) URL_FILE=$OPTARG;;
        uuid) UUID_FILE=$OPTARG;;
        date) DATE=$OPTARG;;
        ?) usage; exit;
    esac
done

if [ "${RUN}" == "check_url" ]; then
    python3 URL/check_url.py "$DATE"
elif [ "${RUN}" == "submit_url" ]; then
    python3 URL/submit.py "$URL_FILE"
elif [ "${RUN}" == "urlscan_result" ]; then
    python3 code/urlscan_crawler.py "$UUID_FILE"
elif [ "${RUN}" == "validate_urlscan" ]; then
    python3 code/validate_urlscan_files.py
elif [ "${RUN}" == "merge_csv" ]; then
    python3 code/merge.py "$DATE"
elif [ "${RUN}" == "parse_feature" ]; then
    python3 code/parse_features.py "$DATE"
elif [ "${RUN}" == "generate_DOM_graph" ]; then
    python3 code/DOM_graph.py "$UUID_FILE"
else
   usage
fi