from bs4 import BeautifulSoup
import sys, os
import pandas as pd

def sensitive_attr(text, sensitive_word):
    if not text:
        return False

    for word in sensitive_word:
        if text.lower().find(word) != -1:
            return True

    return False

def parse_dom(sensitive_word, login_keyword, date, uuid = "0a0be43a-7091-43ea-aa4a-e78e10a65709"):
    tags = dict()

    # file = open(os.path.join("urlscan", date, uuid, "dom_page.html"))
    # outer_soup = BeautifulSoup(file.read(), "html.parser")
    # file.close()

    # if not outer_soup.pre:
    #     return False

    # page_dom = outer_soup.pre.text
    # soup = BeautifulSoup(page_dom, "html.parser")

    file = open(os.path.join("html", date, uuid + ".html"))
    outer_soup = BeautifulSoup(file.read(), "html.parser")
    file.close()
    soup = outer_soup

    span = soup.find_all('span')
    button = soup.find_all('button')
    forms = soup.find_all('form')

    tags["span"] = len(span)
    tags["button"] = len(button)

    # CANTINA+ Case1: input exists in form and keyword match the text or attributes
    # My Case1: input in form
    for form in forms:
        # Check whether it is a search form
        flag = False
        for _input in form.find_all("input"):
            if sensitive_attr(_input.attrs.get("id"), ["search, query"]):
                flag = True
                break
            if sensitive_attr(_input.attrs.get("name"), ["search, query"]):
                flag = True
                break
            if sensitive_attr(_input.attrs.get("alt"), ["search, query"]):
                flag = True
                break
            if sensitive_attr(_input.attrs.get("title"), ["search, query"]):
                flag = True
                break
            if sensitive_attr(_input.attrs.get("aria-label"), ["search, query"]):
                flag = True
                break
            if sensitive_attr(_input.attrs.get("placeholder"), ["search, query"]):
                flag = True
                break
        if flag:
            continue

        inputs = form.find_all("input")
        if len(inputs) >= 1:
            if sensitive_attr(form.text, login_keyword):
                tags["sensitive_case1"] = 1
                break

            if sensitive_attr(form.attrs.get("id"), login_keyword):
                tags["sensitive_case1"] = 1
                break

            if sensitive_attr(form.attrs.get("name"), login_keyword):
                tags["sensitive_case1"] = 1
                break

            for _input in inputs:
                if _input.attrs.get("type") == "email":
                    tags["sensitive_case1"] = 1
                    break
                if _input.attrs.get("type") == "password":
                    tags["sensitive_case1"] = 1
                    break
                if sensitive_attr(_input.attrs.get("id"), login_keyword):
                    tags["sensitive_case1"] = 1
                    break
                if sensitive_attr(_input.attrs.get("name"), login_keyword):
                    tags["sensitive_case1"] = 1
                    break
                if sensitive_attr(_input.attrs.get("alt"), login_keyword):
                    tags["sensitive_case1"] = 1
                    break
                if sensitive_attr(_input.attrs.get("title"), login_keyword):
                    tags["sensitive_case1"] = 1
                    break
                if sensitive_attr(_input.attrs.get("aria-label"), login_keyword):
                    tags["sensitive_case1"] = 1
                    break
                if sensitive_attr(_input.attrs.get("placeholder"), login_keyword):
                    tags["sensitive_case1"] = 1
                    break
                if _input.attrs.get("type") == "submit":
                    if sensitive_attr(_input.attrs.get("value"), login_keyword):
                        tags["sensitive_case1"] = 1
                        break

            if tags.get("sensitive_case1"):
                break

    if tags.get("sensitive_case1") != 1:
        tags["sensitive_case1"] = 0

    # CANTINA+ Case2: examine keyword outside the form tag with K = 2
    # I think this method is not good enough because of K..., maybe detect input tag without form outsides
    # if tags["sensitive_case1"] == 0:
    #     for form in forms:
    #         # Check whether it is a search form
    #         flag = False
    #         for _input in form.find_all("input"):
    #             if sensitive_attr(_input.prettify(), ["search, query"]):
    #                 flag = True
    #                 break

    #         if flag:
    #             continue

    #         # Not a search form, seek keywords from parent's node
    #         p = form.parent.parent
    #         if sensitive_attr(p.text, sensitive_word):
    #             tags["sensitive_case2"] = 1
    #             break

    # My Case2: input outside the form
    if tags["sensitive_case1"] == 0:
        for _input in soup.find_all("input"):
            current_tag = _input
            while current_tag.name != "body" and current_tag.name != "form":
                current_tag = current_tag.parent

            # form in Case1
            if current_tag.name != "body":
                continue

            # no form outside the input tag
            if _input.attrs.get("type") == "email":
                tags["sensitive_case2"] = 1
                break
            if _input.attrs.get("type") == "password":
                tags["sensitive_case2"] = 1
                break
            if sensitive_attr(_input.attrs.get("id"), login_keyword):
                tags["sensitive_case2"] = 1
                break
            if sensitive_attr(_input.attrs.get("name"), login_keyword):
                tags["sensitive_case2"] = 1
                break
            if sensitive_attr(_input.attrs.get("alt"), login_keyword):
                tags["sensitive_case2"] = 1
                break
            if sensitive_attr(_input.attrs.get("title"), login_keyword):
                tags["sensitive_case2"] = 1
                break
            if sensitive_attr(_input.attrs.get("aria-label"), login_keyword):
                tags["sensitive_case2"] = 1
                break
            if sensitive_attr(_input.attrs.get("placeholder"), login_keyword):
                tags["sensitive_case2"] = 1
                break
            if _input.attrs.get("type") == "submit":
                if sensitive_attr(_input.attrs.get("value"), login_keyword):
                    tags["sensitive_case2"] = 1
                    break
                if _input.attrs.get("onclick"):
                    tags["sensitive_case2"] = 1
                    break
                if _input.attrs.get("onClick"):
                    tags["sensitive_case2"] = 1
                    break

    if tags.get("sensitive_case2") != 1:
        tags["sensitive_case2"] = 0

    # CANTINA+ Case3: no login keyword, check only image with no text in form tag
    if not tags["sensitive_case1"] and not tags["sensitive_case2"]:
        for form in forms:
            # Check whether it is a search form
            flag = False
            for _input in form.find_all("input"):
                if sensitive_attr(_input.attrs.get("id"), ["search, query"]):
                    flag = True
                    break
                if sensitive_attr(_input.attrs.get("name"), ["search, query"]):
                    flag = True
                    break
                if sensitive_attr(_input.attrs.get("alt"), ["search, query"]):
                    flag = True
                    break
                if sensitive_attr(_input.attrs.get("title"), ["search, query"]):
                    flag = True
                    break
                if sensitive_attr(_input.attrs.get("aria-label"), ["search, query"]):
                    flag = True
                    break
                if sensitive_attr(_input.attrs.get("placeholder"), ["search, query"]):
                    flag = True
                    break
            if flag:
                continue

            text = form.text
            text = text.replace(" ", "")    # delete space
            text = text.replace("\n", "")    # delete end line
            text = text.replace("\t", "")    # delete tab
            if len(text) == 0 and len(form.find_all("img")) != 0:
                tags["sensitive_case3"] = 1
                break

    if tags.get("sensitive_case3") != 1:
        tags["sensitive_case3"] = 0

    # My Case4: examine title
    if not tags["sensitive_case1"] and not tags["sensitive_case2"] and not tags["sensitive_case3"]:
        title = ''
        try:
            title = soup.find_all('title')[0].text
        except:
            pass
        if sensitive_attr(title, login_keyword):
            body = soup.body.text
            if sensitive_attr(body, login_keyword):
                tags["sensitive_case4"] = 1
            else:
                tags["sensitive_case4"] = 0
        else:
            tags["sensitive_case4"] = 0

    # # CANTINA+ Case4: only input tag without form, check keywords in all html.text
    # # Detect in my Case2
    # if not tags["sensitive_case1"] and not tags["sensitive_case2"] and not tags["sensitive_case3"]:
    #     if len(forms) == 0 and len(soup.find_all("input")) > 0:
    #         text = soup.body.text
    #         text = text.replace(" ", "")    # delete space
    #         text = text.replace("\n", "")    # delete end line
    #         text = text.replace("\t", "")    # delete tab
    #         if sensitive_attr(text, sensitive_word):
    #             tags["sensitive_case4"] = 1

    # My Case5: iframe
    if not tags["sensitive_case1"] and not tags["sensitive_case2"] and not tags["sensitive_case3"] and not tags["sensitive_case4"]:
        iframes = soup.find_all("iframe")
        for iframe in iframes:
            if sensitive_attr(iframe.attrs.get("id"), login_keyword + ["form"]):
                tags["sensitive_case5"] = 1
                break
            if sensitive_attr(iframe.attrs.get("name"), login_keyword + ["form"]):
                tags["sensitive_case5"] = 1
                break
            if sensitive_attr(iframe.attrs.get("title"), login_keyword + ["form"]):
                tags["sensitive_case5"] = 1
                break
            if sensitive_attr(iframe.attrs.get("aria-label"), login_keyword + ["form"]):
                tags["sensitive_case5"] = 1
                break
            if sensitive_attr(iframe.attrs.get("src"), login_keyword + ["form"]):
                tags["sensitive_case5"] = 1
                break

    if tags.get("sensitive_case5") != 1:
        tags["sensitive_case5"] = 0

    # My Case6: detect button links to phishing pages
    if not tags["sensitive_case1"] and not tags["sensitive_case2"] and not tags["sensitive_case3"] and not tags["sensitive_case4"] and not tags["sensitive_case5"]:
        a = soup.find_all("a")
        for _a in a:
            if sensitive_attr(_a.text, login_keyword):
                tags["sensitive_case6"] = 1
                break
            if sensitive_attr(_a.attrs.get("href"), login_keyword + ["popupwnd", "window.open"]):
                tags["sensitive_case6"] = 1
                break
            if sensitive_attr(_a.attrs.get("onclick"), ["popupwnd", "window.open"]):
                tags["sensitive_case6"] = 1
                break
            if sensitive_attr(_a.attrs.get("onClick"), ["popupwnd", "window.open"]):
                tags["sensitive_case6"] = 1
                break

    if tags.get("sensitive_case6") != 1:
        buttons = soup.find_all("button")
        for button in buttons:
            if sensitive_attr(button.text, login_keyword):
                tags["sensitive_case6"] = 1
                break
            if sensitive_attr(button.attrs.get("onclick"), ["popupwnd", "window.open", "window.location", "location.href"]):
                tags["sensitive_case6"] = 1
                break
            if sensitive_attr(button.attrs.get("onClick"), ["popupwnd", "window.open", "window.location", "location.href"]):
                tags["sensitive_case6"] = 1
                break

    if tags.get("sensitive_case6") != 1:
        tags["sensitive_case6"] = 0

    return tags

def parse_all_dom():
    df = pd.read_csv(os.path.join(sys.argv[1]))

    login_keyword = pd.read_csv("login_keyword.txt")["word"].tolist()
    sensitive_word = pd.read_csv("sensitive_word.txt")["word"].tolist()
    for idx, uuid in enumerate(df["UUID"].tolist()):
        print("\r{}/{}, {}".format(idx+1, len(df), uuid), end="")
        try:
            if str(df.loc[idx, "folder"])[0] != "C":
                folder = str(int(df.loc[idx, "folder"]))
            else:
                folder = df.loc[idx, "folder"]
            tags = parse_dom(sensitive_word, login_keyword, folder, uuid)
        except KeyboardInterrupt:
            return
        except:
            print("\n", uuid, "failed")
            continue

        if not tags:
            continue

        for key, value in tags.items():
            df.loc[idx, key] = value

    df.to_csv(os.path.join(sys.argv[1]), index=False)
    print("\nFinish DOM Parse")

    return

def parse_one_dom():
    df = pd.read_csv(os.path.join(sys.argv[1]))

    login_keyword = pd.read_csv("login_keyword.txt")["word"].tolist()
    sensitive_word = pd.read_csv("sensitive_word.txt")["word"].tolist()
    for idx, uuid in enumerate(df["UUID"].tolist()):
        print("\r{}/{}, {}".format(idx+1, len(df), uuid), end="")

        if uuid != sys.argv[2]:
            continue

        try:
            if str(df.loc[idx, "folder"])[0] != "C":
                folder = str(int(df.loc[idx, "folder"]))
            else:
                folder = df.loc[idx, "folder"]
            tags = parse_dom(sensitive_word, login_keyword, folder, uuid)
        except KeyboardInterrupt:
            return
        except:
            print("\n", uuid, "failed")
            continue

        if not tags:
            continue

        for key, value in tags.items():
            print(key, value)

    print("\nFinish DOM Parse")

    return


def parse():
    if len(sys.argv) < 3:
        parse_all_dom()
    else:
        parse_one_dom()

if __name__ == "__main__":
    parse()

## Usage python3 code/detect_sensitive.py unique.csv

## Usage python3 code/detect_sensitive.py feature.csv uuid