# Source directory

This directory contains the "raw" source data of the dataset from which the
CLDF dataset in [`cldf/`](../cldf) is derived.

- `Streitberg-1910-3659.xml`: original file, http://www.wulfila.be/lib/streitberg/1910/
- `xml2tsv.py` is the Python script with which the xml is converted to tsv by running it from the terminal
- `Streitberg-1910-3659.tsv` is the raw file that cldfbench will use as input
- `postags.csv`: http://www.wulfila.be/archive/2006/DB/dictionary/#POSTags
- `sources.bib`: BibTex File containing all sources through which the data was assembled