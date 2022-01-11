import epitran
import pandas as pd
from pathlib import Path

epi = epitran.Epitran("got-Latn")

# add IPA
path = Path.cwd().parent / "cldf" / "forms.csv"
pd.read_csv(path).assign(IPA=lambda x: list(map(epi.transliterate, x.Form)))\
.to_csv(path, index=False, encoding="utf-8")
