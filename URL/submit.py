import requests
import json
import sys, os, csv
import time

api_key = 'fb643854-aab2-4254-8cef-acd506ccdbc0'

def urlscan(url):
    headers = {'API-Key': api_key,'Content-Type':'application/json'}
    data = {"url": url, "visibility": "public"}
    response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
    
    try:
        r = response.json()
        print(url, response, r.get('uuid'))
        return r.get('uuid')

    except:
        print(url, "JsonDecodeError")
        time.sleep(30)
        return None

def main():
    f_out = open(os.path.join("/".join(sys.argv[1].split('/')[0:-1]),"uuid.txt"), "a+")
    f_out.write("UUID\n")

    file = open(sys.argv[1])
    rows = csv.reader(file)

    count = 0
    # init_time = time.time()
    for url in rows:
        uuid = urlscan(url)
        if uuid:
            f_out.write(uuid)
            f_out.write("\n")
            count += 1
        
        # # control api limitation
        # if count >= 5000:
        #     print("Day limitation")
        #     break

        # if count % 60 == 0:
        #     if time.time() - init_time < 60:
        #         time.sleep( int(60 - init_time + time.time()) )
            
        #     init_time = time.time()
        
    file.close()
    f_out.close()

    print("\nFinish Submit!")

if __name__ == "__main__":
    main()

## usage python3 submit.py url.txt
## one line for one url in url.txt