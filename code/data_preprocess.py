import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])

print("Initial:", df.shape)

df = df.dropna()

print("Dropna:", df.shape)

df = df.drop_duplicates("URL")

print("Drop duplicate URL:", df.shape)

df = df[df["Tags"] > 50]

print("Tags > 50:", df.shape)

# df.to_csv(sys.argv[1].split(".")[0] + "_preprocessed.csv")

## Usage: python3 code/preprocess.py URL/feature.csv
## Usage: python3 code/preprocess.py URL/CommonCrawl_5/feature.csv