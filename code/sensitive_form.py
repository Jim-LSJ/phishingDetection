import os, sys
import pandas as pd
from bs4 import BeautifulSoup


def data_preprocessing():
    df = pd.read_csv(os.path.join("URL", "phishing.csv"))

    df = df.drop_duplicates("URL")

    for idx, cookies in enumerate(df["Cookies"].tolist()):
        if cookies == 0:
            df.loc[idx, "secure"] = cookies
            df.loc[idx, "httponly"] = cookies
            df.loc[idx, "session"] = cookies

    df = df.dropna()

    df = df[df["Tags"] > 50]

    df.to_csv(os.path.join("URL", "feature.csv"), index=False)

    return df

def form_parser(uuid, df_form, df_input):
    tag_attrs = ["id", "name", "class", "value", "aria-label"]

    file = open(os.path.join("urlscan", uuid, "dom_page.html"))
    outer_soup = BeautifulSoup(file.read(), "html.parser")
    file.close()

    if not outer_soup.pre:
        return df_form, df_input

    page_dom = outer_soup.pre.text
    soup = BeautifulSoup(page_dom, "html.parser")
    
    forms = soup.find_all("form")
    for form in forms:
        inputs = form.find_all("input")
        if len(inputs) >= 2:
            df_form = df_form.append({"uuid": uuid, 
                                    "form_id": form.attrs.get("id"), 
                                    "form_name": form.attrs.get("name")
                                    }, ignore_index=True)
                            
            for _input in inputs:
                df_input = df_input.append({"uuid": uuid, 
                                    "id":_input.attrs.get("id"),
                                    "name":_input.attrs.get("name"),
                                    "class":_input.attrs.get("class"),
                                    "value":_input.attrs.get("value"),
                                    "aria-label":_input.attrs.get("aria-label")
                                    }, ignore_index=True)

    return df_form, df_input

def parse():
    df = data_preprocessing()
    df = df[df['label'] == 1]
    df = df[df['form'] > 0]

    df_form, df_input = pd.DataFrame(), pd.DataFrame()
    for idx, uuid in enumerate(df["UUID"]):
        print("\r{}/{}, {}".format(idx+1, len(df), uuid), end="")
        df_form, df_input = form_parser(uuid, df_form, df_input)

    df_form.to_csv("form.csv", index=False)
    df_input.to_csv("input.csv", index=False)

def sensitive_attr(text, sensitive_word):
    if not text:
        return False
    
    for word in sensitive_word:
        if text.lower().find(word) != -1:
            return True

    return False

def sensitive_detection(uuid, sensitive_word):
    tag_attrs = ["id", "name", "class", "value", "aria-label"]

    try:
        file = open(os.path.join("urlscan", uuid, "dom_page.html"))
    except:
        return False

    outer_soup = BeautifulSoup(file.read(), "html.parser")
    file.close()

    if not outer_soup.pre:
        return False

    page_dom = outer_soup.pre.text
    soup = BeautifulSoup(page_dom, "html.parser")
    
    forms = soup.find_all("form")
    for form in forms:
        inputs = form.find_all("input")
        if len(inputs) >= 2:
            if sensitive_attr(form.attrs.get("id"), sensitive_word):
                return True
            
            if sensitive_attr(form.attrs.get("name"), sensitive_word):
                return True
                            
            for _input in inputs:
                if sensitive_attr(_input.attrs.get("id"), sensitive_word):
                    return True
                if sensitive_attr(_input.attrs.get("name"), sensitive_word):
                    return True
                if sensitive_attr(_input.attrs.get("aria-label"), sensitive_word):
                    return True

    return False

def sensitive_form():
    path = os.path.join(sys.argv[1], "feature.csv")
    df = pd.read_csv(path)

    sensitive_word = pd.read_csv("sensitive_word.txt")["word"].tolist()

    for idx, uuid in enumerate(df["UUID"]):
        print("\r{}/{}, {}".format(idx+1, len(df), uuid), end="")
        if df.loc[idx, "form"] == 0:
            df.loc[idx, "sensitive"] = 0
            continue
        elif not df.loc[idx, "form"]:
            continue

        if sensitive_detection(uuid, sensitive_word):
            df.loc[idx, "sensitive"] = 1
        else:
            df.loc[idx, "sensitive"] = 0

    df.to_csv(os.path.join(sys.argv[1], "feature.csv"), index=False)

def main():
    # parse()
    sensitive_form()
    print("\nFinish Sensitive Form Detection")

if __name__ == "__main__":
    main()

## Usage: python3 code/sensitive_form.py <URL/20200702>