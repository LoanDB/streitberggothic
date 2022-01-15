# Supplementary files

- `Streitberg-1910-3645.xml`: original file, downloaded from http://www.wulfila.be/lib/streitberg/1910/text/dictionary.xml
- `postags.csv`: Decodes part of speech tags from numberical IDs. Downloaded from http://www.wulfila.be/archive/2006/DB/dictionary/#POSTags
- `xml2tsv.py`: Python script with which the xml is converted to tsv. Cd into this directory and run `python xml2tsv.py` from the terminal. Dependencies: beautifulsoup4-4.10.0, pandas-1.3.5, lxml-4.7.1
- `orthography0.tsv`: an alternative way of IPA-transcribing and segmenting the Gothic orthography. Was not used in the end.
- `makeortho.py`: The file `orthography.tsv` in the folder `etc` is created with this script. Dependencies: ipatok 0.4.0, epitran 1.15 (needs marisa-trie 0.7.7, panphon 0.19.1, Microsoft C++ Build Tools)