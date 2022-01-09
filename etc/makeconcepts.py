import pandas as pd

pd.read_csv("Streitberg-1910-3659.tsv", usecols=["sense"], sep="\t")\
.to_csv("concepts.tsv", index=False, encoding="utf-8", sep="\t")
