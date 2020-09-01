import pandas as pd
import os, sys

# df = pd.read_csv(sys.argv[1])
# d = pd.DataFrame()
# for i in range(len(df)):
#     print("\r{}/{}".format(i, len(df)), end="")
#     if df.loc[i, "UUID"] + ".png" in os.listdir("screenshot/" + df.loc[i, "folder"]):
#         d = d.append(df.loc[i])

# d.to_csv(sys.argv[1], index=False)

df = pd.read_csv(sys.argv[1])
print(len(df))
expired_uuid = sys.argv[2]
df = df[df["UUID"] != expired_uuid]
df.to_csv(sys.argv[1], index=False)
print(len(df))
## Usage: python3 code/drop_expired.py URL/20200829/feature.csv
## Usage: python3 code/drop_expired.py feature.csv uuid