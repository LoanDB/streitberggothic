import pandas as pd

dfc = pd.read_csv("Streitberg-1910-3659.tsv", usecols=["sense])
dfc["NUMBER"] = dfc.index + 1
dfc.to_csv("Streitberg-1910-3659.tsv", index=False, encoding="utf-8")
