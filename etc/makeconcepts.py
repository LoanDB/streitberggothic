"""cd to folder `etc` and run `python makeconcepts.py` from terminal"""

from pathlib import Path
import re

import pandas as pd
from pysem.glosses import to_concepticon

PATH = Path.cwd().parent / "raw" / "Streitberg-1910-3645.tsv"


def gg(d):
    """dict vals to tuples (ID, Gloss) or ("", "")"""
    return {k: (d[k][0][0], d[k][0][1]) if d[k] else ("", "") for k in d}


def main():
    """"
    read Streitberg-1910-3645.tsv,
    link data to concepticon,
    write concepts.tsv
    """
    # read file and clean column "sense"
    dfgot = pd.read_csv(PATH, sep="\t", usecols=["sense", "pos"])
    dfgot["sense"] = [re.sub("[†\d\.\*\?\~]", "", g) for g in dfgot.sense]

    # define list of dictionaries and plug into to_concepticon()
    glo = [{"gloss": g, "pos": p} for g, p in zip(dfgot.sense, dfgot.pos)]
    G = gg(to_concepticon(glo, language="de", pos_ref="pos", max_matches=1))

    # map dictionary to new columns
    newcols = ["Concepticon_ID", "Concepticon_Gloss"]
    dfgot[newcols] = dfgot['sense'].map(G).tolist()
    dfgot.to_csv("concepts.tsv", index=False, encoding="utf-8", sep="\t")

if __name__ == "__main__":
    main()
