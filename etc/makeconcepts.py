"""cd to folder `etc` and run `python makeconcepts.py` from terminal"""

from pathlib import Path
import re

import pandas as pd
from pysem.glosses import to_concepticon

PATH = Path.cwd().parent / "raw" / "Streitberg-1910-3659.tsv"


def main():
    dfgot = pd.read_csv(PATH, sep="\t")

    conid, conglo = [], []
    for g, p in zip(dfgot.sense, dfgot.pos):
        gloss = [{"gloss": re.sub("[†\d\.\*\?\~]", "", g), "pos": p}]
        out = list(to_concepticon(gloss, language="de",
                                  pos_ref="pos", max_matches=1).values())[0]
        if out:
            conid.append(out[0][0])
            conglo.append(out[0][1])
        else:
            conid.append(None)
            conglo.append(None)

    dfgot["CONCEPTICON_ID"], dfgot["CONCEPTICON_GLOSS"] = conid, conglo
    del dfgot["form"]
    dfgot.to_csv("concepts.tsv", index=False, encoding="utf-8", sep="\t")

if __name__ == "__main__":
    main()
