#!/bin/bash
# Program:
#   This program control the whole project
# History:
# 2020/07/07 First version
usage() {
    echo -e "bash main.sh -r submit_url -url <URL/CommonCrawl/url.txt>"
    echo -e "bash main.sh -r urlscan_result -uuid <URL/CommonCrawl/uuid.txt"
}

while getopts r:url:uuid:? argv
do
    case $argv in
        r) RUN=$OPTARG;;
        url) URL_FILE=$OPTARG;;
        uuid) UUID_FILE=$OPTARG;;
        ?) usage; exit;
    esac
done

if [ "${RUN}" == "submit_url" ]; then
    python3 URL/submit.py ${URL_FILE}
elif [ "${RUN}" == "urlscan_result" ]; then
    python3 code/urlscan_crawler.py ${UUID_FILE}
else
   usage
fi