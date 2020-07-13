from bs4 import BeautifulSoup
import sys, os
import pandas as pd

def parse_cookies(uuid = "0a1d3d77-6842-4c3d-b0b0-229f60ac5056"):
    path = os.path.join("urlscan", uuid, "result_page.html")
    file = open(path)
    soup = BeautifulSoup(file.read(), "html.parser")
    file.close()
    
    secure = session = httponly = 0
    no_httponly_session = httponly_session = 0
    if not soup.find(id="behaviour"):
        return False

    total_cookies = 0
    for h3 in soup.find(id="behaviour").find_all("h3"):
        if h3.text.split(' ')[1] == "Cookies":
            total_cookies = h3.text.split(' ')[0]

    if total_cookies == '0':
        return {"Cookies": total_cookies}

    tbody = soup.find(id="behaviour").find("tbody")
    if not tbody:
        return False

    for tr in tbody.find_all("tr"):
        tds = tr.find_all(class_="right hidden-xs")
        secure += tds[0].span.attrs['class'][-1] == "green"
        session += tds[1].span.attrs['class'][-1] == "green"
        httponly += tds[2].span.attrs['class'][-1] == "green"
        # print("secure: {}, session: {}, http-only: {}, no http-only sess: {}, http-only sess: {}".
        #        format(secure, session, httponly, no_httponly_session, httponly_session))
    
    return {"Cookies": total_cookies, "secure":secure, "session": session, "httponly": httponly}

def parse_all_cookies():
    uuids = pd.read_csv(os.path.join(sys.argv[1], "uuid_graph.csv"))
    for idx, uuid in enumerate(uuids["UUID"].tolist()):
        print("\r{}/{}, {}".format(idx+1, len(uuids), uuid), end="")
        try:
            cookies = parse_cookies(uuid)
        except KeyboardInterrupt:
            return
        except:
            print("\n", uuid, "failed")
            continue
        
        if not cookies:
            continue

        uuids.loc[idx, "Cookies"] = cookies["Cookies"]
        if cookies["Cookies"] == '0':
            continue

        uuids.loc[idx, "secure"] = cookies["secure"]
        uuids.loc[idx, "session"] = cookies["session"]
        uuids.loc[idx, "httponly"] = cookies["httponly"]
        
    uuids.to_csv(os.path.join(sys.argv[1], "uuid_graph.csv"), index=False)
    print("\nFinish Cookies Parse")

    return

def parse_js_var(uuid = "0a0be43a-7091-43ea-aa4a-e78e10a65709"):
    path = os.path.join("urlscan", uuid, "result_page.html")
    file = open(path)
    soup = BeautifulSoup(file.read(), "html.parser")
    file.close()

    if not soup.find(id="behaviour"):
        return False

    total_js_var = 0
    for h3 in soup.find(id="behaviour").find_all("h3"):
        if h3.text.split(' ')[1] == "JavaScript":
            total_js_var = h3.text.split(' ')[0]
    
    return {"JSGlobalVar": total_js_var}

def parse_all_js():
    uuids = pd.read_csv(os.path.join(sys.argv[1], "uuid_graph.csv"))
    for idx, uuid in enumerate(uuids["UUID"].tolist()):
        print("\r{}/{}, {}".format(idx+1, len(uuids), uuid), end="")
        try:
            js_var = parse_js_var(uuid)
        except KeyboardInterrupt:
            return
        except:
            print("\n", uuid, "failed")
            continue

        if not js_var:
            continue

        uuids.loc[idx, "JSGlobalVar"] = js_var["JSGlobalVar"]

    uuids.to_csv(os.path.join(sys.argv[1], "uuid_graph.csv"), index=False)
    print("\nFinish JS Parse")

    return 

def parse_result(uuid = "0a0be43a-7091-43ea-aa4a-e78e10a65709"):
    path = os.path.join("urlscan", uuid, "result_page.html")
    file = open(path)
    soup = BeautifulSoup(file.read(), "html.parser")
    file.close()

    main = soup.find(class_="main")
    if not main.h1.find("span"):
        return False

    if main.find("h2", class_="text-danger"):
        if  main.find("h2", class_="text-danger").text == "We could not scan this website!":
            return False

    URL = ""
    span = main.find_all(class_="row")[1].find("span")
    try:
        URL = span.text.split('\n')[1].strip()
    except:
        URL = span.text
    
    stats_dict = dict()
    summary = soup.find(id="summary")
    stats = summary.find(class_="row").find(class_="row")
    for stat in stats.find_all("div"):
        stats_dict[stat.find_all("small")[-1].text] = stat.span.attrs.get("data-count")

    OutGoingLinks = soup.find(id="links").h3.text.split(' ')[0]
    
    stats_dict["URL"] = URL
    stats_dict["OutGoingLinks"] = OutGoingLinks

    return stats_dict

def parse_results():
    uuids = pd.read_csv(os.path.join(sys.argv[1], "uuid_graph.csv"))
    for idx, uuid in enumerate(uuids["UUID"].tolist()):
        print("\r{}/{}, {}".format(idx+1, len(uuids), uuid), end="")
        try:
            stats = parse_result(uuid)
        except KeyboardInterrupt:
            return
        except:
            print("\n", uuid, "failed")
            continue

        if not stats:
            continue

        for key, value in stats.items():
            uuids.loc[idx, key] = value

    uuids.to_csv(os.path.join(sys.argv[1], "uuid_graph.csv"), index=False)
    print("\nFinish Result Parse")

    return

def parse_dom(uuid = "0a0be43a-7091-43ea-aa4a-e78e10a65709"):
    path = os.path.join("urlscan", uuid, "dom_page.html")
    file = open(path)
    outer_soup = BeautifulSoup(file.read(), "html.parser")
    file.close()
    
    if not outer_soup.pre:
        return False

    page_dom = outer_soup.pre.text
    soup = BeautifulSoup(page_dom, "html.parser")

    div = soup.find_all('div')
    img = soup.find_all('img')
    iframe = soup.find_all('iframe')
    a = soup.find_all('a')
    script = soup.find_all('script')
    internal_script = soup.find_all('script', src='')
    form = soup.find_all('form')
    inputs = soup.find_all('input')
    textarea = soup.find_all('textarea')
    tag = soup.find_all()
    no_class_tag = soup.find_all(class_='')
    title = ''
    try:
        title = soup.find_all('title')[0].text
    except:
        pass
    
    tags = dict()
    tags["div"] = len(div)
    tags["img"] = len(img)
    tags["iframe"] = len(iframe)
    tags["a"] = len(a)
    tags["script"] = len(script)
    tags["external_script"] = len(script) - len(internal_script)
    tags["internal_script"] = len(internal_script)
    tags["form"] = len(form)
    tags["input"] = len(inputs)
    tags["textarea"] = len(textarea)
    tags["Tags"] = len(tag)
    tags["No-class Tags"] = len(no_class_tag)
    tags["class Tags"] = len(tag) - len(no_class_tag)
    tags["Title"] = title

    return tags

def parse_all_dom():
    uuids = pd.read_csv(os.path.join(sys.argv[1], "uuid_graph.csv"))
    for idx, uuid in enumerate(uuids["UUID"].tolist()):
        print("\r{}/{}, {}".format(idx+1, len(uuids), uuid), end="")
        try:
            tags = parse_dom(uuid)
        except KeyboardInterrupt:
            return
        except:
            print("\n", uuid, "failed")
            continue

        if not tags:
            continue

        for key, value in tags.items():
            uuids.loc[idx, key] = value

    uuids.to_csv(os.path.join(sys.argv[1], "uuid_graph.csv"), index=False)
    print("\nFinish DOM Parse")

    return

def parse():
    parse_all_dom()
    parse_all_cookies()
    parse_all_js()
    parse_results()
    
if __name__ == "__main__":
    parse()

## Usage python3 code/parse_features.py <URL/20200710>