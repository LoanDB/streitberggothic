"""open terminal, cd into folder `raw`, run `python xml2tsv.py` """

import re

from bs4 import BeautifulSoup
import unicodedata as ud
import pandas as pd

# "http://www.wulfila.be/archive/2006/DB/dictionary/#POSTags
DFPOS = pd.read_csv(r"postags.csv")
POSDICT = {i: j for i, j in zip(DFPOS.ID, DFPOS.Name)}

latin_letters = {}


def is_latin(uchr):
    """
    src: https://stackoverflow.com/questions/3094498/how-can-i-check-if-a-
    python-unicode-string-contains-non-western-letters
    """
    try:
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))


def only_roman_chars(unistr):
    """
    src: https://stackoverflow.com/questions/3094498/how-can-i-check-if-a-
    python-unicode-string-contains-non-western-letters
    """
    return all(is_latin(uchr)
               for uchr in unistr
               if uchr.isalpha())  # isalpha suggested by John Machin


def main():
    """create & read soup w beautifulsoup & put into pandas df"""

    # create soup
    with open("Streitberg-1910-3659.xml", 'r', encoding="utf-8") as f:
        file = f.read()
    soup = BeautifulSoup(file, 'lxml')

    # read soup
    dfgot = pd.DataFrame()

    # append forms
    dfgot["form"] = [i.text for i in soup.find_all("form")]
    sense = []  # meanings
    key = []  # "row ID" within xml
    # "#P003.18": http://www.wulfila.be/lib/streitberg/1910/text/html/#P003.18
    pos = []  # part of speech

    # loop through soup
    for i in soup.find_all("form"):
        gr2lat = None  # greek to latin characters
        if i:

            # append sense
            if i.parent.find("sense"):
                if i.parent.find("sense").find_all("tr", {"xml:lang": "grc"}):
                    for j in i.parent.find("sense").find_all("tr"):
                        if only_roman_chars(j.text):
                            gr2lat = j.text
            if gr2lat:
                sense.append(gr2lat)
            else:
                try:
                    sense.append(str(i.parent.find("sense"))
                                 .split("target=\"")[1][:7])
                except IndexError:
                    try:
                        sense.append(i.parent.find("sense").tr.text)
                    except AttributeError:
                        sense.append(None)

            # append keys
            try:
                key.append(str(i.parent).split("key=\"")[1][:7])
            except IndexError:
                key.append(None)

            # append pos
            if i.parent.find("grammar"):
                pos.append(POSDICT[int(i.parent.find("grammar")
                                        .attrs.get("db:pos", 47))])
            else:
                pos.append(POSDICT[47])  # "<none>"

    # where row only points to key, insert content of that link
    keyd = {key: sense for key, sense in zip(key, sense)}
    dfgot["sense"] = [keyd.get(key, key) if key else None for key in sense]
    dfgot["sense"].fillna(value=dfgot["form"], inplace=True)
    dfgot["sense"] = [i if only_roman_chars(i) else None for i in dfgot.sense]
    dfgot["sense"].fillna(value=dfgot["form"], inplace=True)

    # remove brackets and their content
    dfgot["sense"] = [re.sub("\(.*\)", "", i) for i in dfgot["sense"]]

    # add col pos
    dfgot["pos"] = pos

    # write tsv
    dfgot.to_csv("Streitberg-1910-3659.tsv", index=False,
                 encoding="utf-8", sep="\t")

if __name__ == "__main__":
    main()
