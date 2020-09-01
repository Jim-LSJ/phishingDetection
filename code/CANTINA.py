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

    file = open(os.path.join("urlscan", date, uuid, "dom_page.html"))
    outer_soup = BeautifulSoup(file.read(), "html.parser")
    file.close()

    if not outer_soup.pre:
        return False

    page_dom = outer_soup.pre.text
    soup = BeautifulSoup(page_dom, "html.parser")

    # file = open(os.path.join("html", date, uuid + ".html"))
    # outer_soup = BeautifulSoup(file.read(), "html.parser")
    # file.close()
    # soup = outer_soup

    span = soup.find_all('span')
    button = soup.find_all('button')
    forms = soup.find_all('form')

    tags["span"] = len(span)
    tags["button"] = len(button)

    # CANTINA+ Case1.
    for form in forms:

        all_tags = form.find_all(True)
        input_tags = soup.find_all("input")

        if len(input_tags) >= 1:
            # Login keywords are searched in the text nodes
            if sensitive_attr(form.text, login_keyword):
                tags["sensitive_case1"] = 1
                break
            # alt and title attributes of element nodes of the subtree rooted at the form node
            for _tag in all_tags:
                if sensitive_attr(_tag.attrs.get("alt"), login_keyword):
                    tags["sensitive_case1"] = 1
                    break
                if sensitive_attr(_tag.attrs.get("title"), login_keyword):
                    tags["sensitive_case1"] = 1
                    break

            if tags.get("sensitive_case1"):
                break

    if tags.get("sensitive_case1") != 1:
        tags["sensitive_case1"] = 0

    # CANTINA+ Case2.
    if tags["sensitive_case1"] == 0:
        for form in forms:
            all_tags = form.find_all(True)
            input_tags = soup.find_all("input")
            # Login keywords exist outside the subtree rooted at the form node
            if len(input_tags) >=1 and sensitive_attr(soup.text, login_keyword):
                # Examine whether the form f is a search form
                if sensitive_attr(form.text, ["search"]):
                    tags["sensitive_case2"] = 0
                    break
                # alt and title attributes of element nodes of the subtree rooted at the form node
                for _tag in all_tags:
                    if sensitive_attr(_tag.attrs.get("alt"), ["search"]):
                        tags["sensitive_case2"] = 0
                        break
                    if sensitive_attr(_tag.attrs.get("title"), ["search"]):
                        tags["sensitive_case2"] = 0
                        break

                if tags.get("sensitive_case2") == 0:
                    break

                # Traverse the DOM tree up for K=2 levels to ancestor node n
                current_tag = form
                counter = 0
                while current_tag.name != "body" and counter < 2:
                    current_tag = current_tag.parent
                    counter += 1

                all_Tags = current_tag.find_all(True)
                # Search login keywords under the subtree rooted at n
                if sensitive_attr(current_tag.text, login_keyword):
                    tags["sensitive_case2"] = 1
                    break

                # alt and title attributes of element nodes of the subtree rooted at the form node
                for _Tag in all_Tags:
                    if sensitive_attr(_Tag.attrs.get("alt"), login_keyword):
                        tags["sensitive_case2"] = 1
                        break
                    if sensitive_attr(_Tag.attrs.get("title"), login_keyword):
                        tags["sensitive_case2"] = 1
                        break

            if tags.get("sensitive_case2"):
                break

    if tags.get("sensitive_case2") != 1:
        tags["sensitive_case2"] = 0

    # CANTINA+ Case3.
    if not tags["sensitive_case1"] and not tags["sensitive_case2"]:
        for form in forms:
            all_tags = form.find_all(True)
            input_tags = soup.find_all("input")
            # Login keywords exist outside the subtree rooted at the form node
            if len(input_tags) >=1 and sensitive_attr(soup.text, login_keyword):
                # Examine whether the form f is a search form
                if sensitive_attr(form.text, ["search"]):
                    tags["sensitive_case3"] = 0
                    break
                # alt and title attributes of element nodes of the subtree rooted at the form node
                for _tag in all_tags:
                    if sensitive_attr(_tag.attrs.get("alt"), ["search"]):
                        tags["sensitive_case3"] = 0
                        break
                    if sensitive_attr(_tag.attrs.get("title"), ["search"]):
                        tags["sensitive_case3"] = 0
                        break

            if tags.get("sensitive_case3") == 0:
                break

            text = form.text
            text = text.replace(" ", "")    # delete space
            text = text.replace("\n", "")    # delete end line
            text = text.replace("\t", "")    # delete tab
            if len(text) == 0 and len(form.find_all("img")) != 0:
                tags["sensitive_case3"] = 1
                break

    if tags.get("sensitive_case3") != 1:
        tags["sensitive_case3"] = 0

    # Cantina+ Case4.
    if not tags["sensitive_case1"] and not tags["sensitive_case2"] and not tags["sensitive_case3"]:
        if sensitive_attr(soup.text, login_keyword):
            tags["sensitive_case4"] = 1
        else:
            tags["sensitive_case4"] = 0

    return tags

def parse_all_dom():
    df = pd.read_csv(os.path.join(sys.argv[1]))

    login_keyword = pd.read_csv("login_keyword.txt")["word"].tolist()
    sensitive_word = pd.read_csv("sensitive_word.txt")["word"].tolist()
    for idx, uuid in enumerate(df["UUID"].tolist()):
        print("\r{}/{}, {}".format(idx+1, len(df), uuid), end="")
        try:
            # if str(df.loc[idx, "folder"])[0] != "C":
            #     folder = str(int(df.loc[idx, "folder"]))
            # else:
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

    df.to_csv(os.path.join(sys.argv[1]).split(".")[0] + "_CANTINA.csv", index=False)
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