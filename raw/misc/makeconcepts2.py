"""
cd to folder `etc` and run `python makeconcepts.py` from terminal,
src of masterconceptlist.csv: http://northeuralex.org/parameters
"""

from pathlib import Path
import re

from numpy import nan
import pandas as pd
from pysem.glosses import to_concepticon

in_path = Path.cwd().parent / "Streitberg-1910-3645.tsv"
in_path2 = Path.cwd().parent.parent / "etc" / "masterconceptlist.txt"
out_path = Path.cwd().parent.parent / "etc" / "concepts2.tsv"
out_path2 = Path.cwd().parent.parent / "etc" / "missing.txt"

mcl = open(in_path2).read().split("\n")

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
    dfgot = pd.read_csv(in_path, sep="\t", usecols=["sense", "pos"])
    dfgot["sense"] = [re.sub("[†\\d\\.\\*\\?\\~]", "", g) for g in dfgot.sense]

    # define list of dictionaries and plug into to_concepticon()
    glo = [{"gloss": g, "pos": p} for g, p in zip(dfgot.sense, dfgot.pos)]
    G = gg(to_concepticon(glo, language="de", pos_ref="pos", max_matches=10))

    # map dictionary to new columns
    newcols = ["Concepticon_ID", "Concepticon_Gloss"]
    dfgot[newcols] = dfgot.sense.map(G).tolist()
    
    #drop concepts not in masterconceptlist
    dfgot = dfgot[dfgot.Concepticon_Gloss.isin(mcl)]
    dfgot.Concepticon_Gloss.replace("", nan, inplace=True)    
    dfgot.dropna(subset=["Concepticon_Gloss"], inplace=True)
    dfgot.to_csv(out_path, index=False, encoding="utf-8", sep="\t")

    #write missing concepts
    with open(out_path2, "w") as f:
        f.write("\n".join(i for i in (set(mcl) - set(dfgot.Concepticon_Gloss))))

if __name__ == "__main__":
    main()
