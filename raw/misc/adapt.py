"""cd to folder `misc` and run `python3.9 -m adapt` from terminal"""

from pathlib import Path
import re

import pandas as pd

from loanpy import adrc

def main():
    """adds col with predicted loanword adaptation(s) to forms.csv"""

    # define in and output paths and name of the output column
    in_path1 = Path.cwd().parent.parent / "cldf" / "forms.csv"
    in_path2 = Path.cwd().parent.parent.parent / "ronatasbertawot" / "etc" / "soundsubstiEAH_WOT.txt"
    in_path3 = Path.cwd().parent.parent.parent / "ronatasbertawot" / "etc" / "phonotctsubstiEAH_WOT.txt"
    out_path = in_path1
    outcolname = "ad"

    #read in forms.csv with pandas
    dfforms = pd.read_csv(in_path1)
    #add new column of backward-reconstructions with loanpy
    Sc = adrc.Adrc(scdict=in_path2, scdict_struc=in_path3)
    output = [(Sc.adapt(i.replace(" ", ""), howmany=70,
                            hm_struc=3, hm_paths=2,
                            show_workflow=True), Sc.workflow)
                            for i in dfforms["Segments"]]
    dfforms[outcolname] = [i[0] for i in output]
    dfforms[outcolname+"_workflow"] = [i[1] for i in output]
    #write new file
    dfforms.to_csv(out_path, encoding="utf-8", index=False)

if __name__ == "__main__":
    main()
