import pandas as pd
import os, sys

df = pd.read_csv("feature.csv")
for i in range(len(df)):
    label = df.loc[i, "sensitive_label"]
    folder = str(df.loc[i, "folder"])
    if folder[0] != "C":
        continue

    uuid = df.loc[i, "UUID"]

    print("\r{}/{}, {}/{}".format(i, len(df), folder, uuid), end="")

    if label == 1:
        try:
            os.makedirs(os.path.join("screenshot_phishing", "sensitive_form", folder))
        except:
            pass

        os.system("cp " + os.path.join("screenshot", folder, uuid + ".png") + " " +
                os.path.join("screenshot_phishing", "sensitive_form", folder, uuid + ".png"))

    else:
        try:
            os.makedirs(os.path.join("screenshot_phishing", "no_sensitive_form", folder))
        except:
            pass

        os.system("cp " + os.path.join("screenshot", folder, uuid + ".png") + " " +
                os.path.join("screenshot_phishing", "no_sensitive_form", folder, uuid + ".png"))