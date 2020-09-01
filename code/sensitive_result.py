import pandas as pd
import sys

# df = pd.read_csv("feature.csv")
df = pd.read_csv(sys.argv[1])

attr = [
            'div', 'img', 'iframe', 'a', 'script', 'external_script', 'internal_script',
            'form', 'input', 'textarea', 'Tags', 'No-class Tags', 'class Tags', 'Title',
            'Cookies', 'session', 'httponly', 'session & httponly',
            'OutGoingLinks', 'sensitive_label'
        ]

# drop duplicate
df = df.dropna()
a = df.drop_duplicates("hash_value")
# a = a.drop_duplicates(attr)

# phishing
a = a[a["label"] == 1]

sens = a[a["sensitive_label"] == 1]
no_sens = a[a["sensitive_label"] == 0]

print("origin:\n\tsens: {}\n\tno_sens: {}".format(sens.shape, no_sens.shape))

# case1
case1_s = sens[sens["sensitive_case1"] == 1]
case1_n = no_sens[no_sens["sensitive_case1"] == 1]
print("case1:\n\tsens: {}\n\tno_sens: {}".format(case1_s.shape, case1_n.shape))

# case2
case2_s = sens[(sens["sensitive_case1"] == 1) | (sens["sensitive_case2"] == 1)]
case2_n = no_sens[(no_sens["sensitive_case1"] == 1) | (no_sens["sensitive_case2"] == 1)]
print("case2:\n\tsens: {}\n\tno_sens: {}".format(case2_s.shape, case2_n.shape))

# case3
case3_s = sens[(sens["sensitive_case1"] == 1) | (sens["sensitive_case2"] == 1) | (sens["sensitive_case3"] == 1)]
case3_n = no_sens[(no_sens["sensitive_case1"] == 1) | (no_sens["sensitive_case2"] == 1) | (no_sens["sensitive_case3"] == 1)]
print("case3:\n\tsens: {}\n\tno_sens: {}".format(case3_s.shape, case3_n.shape))

# case4
case4_s = sens[(sens["sensitive_case1"] == 1) | (sens["sensitive_case2"] == 1) | (sens["sensitive_case3"] == 1) | (sens["sensitive_case4"] == 1)]
case4_n = no_sens[(no_sens["sensitive_case1"] == 1) | (no_sens["sensitive_case2"] == 1) | (no_sens["sensitive_case3"] == 1) | (no_sens["sensitive_case4"] == 1)]
print("case4:\n\tsens: {}\n\tno_sens: {}".format(case4_s.shape, case4_n.shape))

# case5
case5_s = sens[(sens["sensitive_case1"] == 1) | (sens["sensitive_case2"] == 1) | (sens["sensitive_case3"] == 1) | (sens["sensitive_case4"] == 1) | (sens["sensitive_case5"] == 1)]
case5_n = no_sens[(no_sens["sensitive_case1"] == 1) | (no_sens["sensitive_case2"] == 1) | (no_sens["sensitive_case3"] == 1) | (no_sens["sensitive_case4"] == 1) | (no_sens["sensitive_case5"] == 1)]
print("case5:\n\tsens: {}\n\tno_sens: {}".format(case5_s.shape, case5_n.shape))

# case6
case6_s = sens[(sens["sensitive_case1"] == 1) | (sens["sensitive_case2"] == 1) | (sens["sensitive_case3"] == 1) | (sens["sensitive_case4"] == 1) | (sens["sensitive_case5"] == 1) | (sens["sensitive_case6"] == 1)]
case6_n = no_sens[(no_sens["sensitive_case1"] == 1) | (no_sens["sensitive_case2"] == 1) | (no_sens["sensitive_case3"] == 1) | (no_sens["sensitive_case4"] == 1) | (no_sens["sensitive_case5"] == 1 ) | (no_sens["sensitive_case6"] == 1)]
print("case6:\n\tsens: {}\n\tno_sens: {}".format(case6_s.shape, case6_n.shape))

# case4 & object
case4_s = sens[(sens["object_detection"] == 1) | (sens["sensitive_case1"] == 1) | (sens["sensitive_case2"] == 1) | (sens["sensitive_case3"] == 1) | (sens["sensitive_case4"] == 1) | (sens["sensitive_case5"] == 1) | (sens["sensitive_case6"] == 1)]
case4_n = no_sens[(no_sens["object_detection"] == 1) | (no_sens["sensitive_case1"] == 1) | (no_sens["sensitive_case2"] == 1) | (no_sens["sensitive_case3"] == 1) | (no_sens["sensitive_case4"] == 1) | (no_sens["sensitive_case5"] == 1) | (no_sens["sensitive_case5"] == 1)]
print("case & object:\n\tsens: {}\n\tno_sens: {}".format(case4_s.shape, case4_n.shape))

examine = a[(a["sensitive_case1"] == 0) & (a["sensitive_case2"] == 0) & (a["sensitive_case3"] == 0) & (a["sensitive_case4"] == 0) & (a["sensitive_case5"] == 0)]# & (a["sensitive_case6"] == 0)]
examine.to_csv("examine_not_detected.csv", index=False)

examine = a[(a["object_detection"] == 0) & (a["sensitive_case1"] == 0) & (a["sensitive_case2"] == 0) & (a["sensitive_case3"] == 0) & (a["sensitive_case4"] == 0) & (a["sensitive_case5"] == 0) & (a["sensitive_case6"] == 0)]
examine.to_csv("examine_not_detect_od.csv", index=False)

examine = a[a["sensitive_case1"] == 1]
examine.to_csv("examine_case1.csv", index=False)

examine = a[a["sensitive_case2"] == 1]
examine.to_csv("examine_case2.csv", index=False)

examine = a[a["sensitive_case3"] == 1]
examine.to_csv("examine_case3.csv", index=False)

examine = a[a["sensitive_case4"] == 1]
examine.to_csv("examine_case4.csv", index=False)

examine = a[a["sensitive_case5"] == 1]
examine.to_csv("examine_case5.csv", index=False)

## Usage: python3 code/sensitive_result.py URL/20200826/feature.csv
## Usage: python3 code/sensitive_result.py feature.csv