"""cd to folder `etc` and run `python makeortho.py` from terminal"""

from pathlib import Path

import epitran
import pandas as pd
from ipatok import tokenise

epi = epitran.Epitran("got-Latn").transliterate

def segment(word):
    return ' '.join(tokenise(epi(word)))
    
def main():
    """adds col IPA with epitran"""

    # create orthography.tsv
    in_path = Path.cwd().parent / "cldf" / "forms.csv"
    out_path = Path.cwd().parent / "etc" / "orthography.tsv"
    pd.read_csv(in_path, usecols=["Form"])\
    .assign(IPA=lambda x: list(map(segment, x.Form)))\
    .rename(columns={"Form": "Grapheme"})\
    .drop_duplicates()\
    .to_csv(out_path, index=False, encoding="utf-8", sep="\t")

if __name__ == "__main__":
    main()
    