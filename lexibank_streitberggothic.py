import pathlib
import re

import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec, Concept

REP = [(x, "") for x in "†*[]~?;+-"] + \
      [(x, "a") for x in "áàā"] + [(x, "ɪ") for x in "ïíìī"] + \
      [("ē", "e"), ("ō", "o"), ("ū", "u"), (" ", "_"), (",_", ", ")]

@attr.s
class CustomConcept(Concept):
    POS = attr.ib(default=None)
    
def cln(word): return re.sub("[†\d\.\*\?\~]", "", word)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "streitberggothic"

    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements=REP)
                         
    concept_class = CustomConcept

    def cmd_makecldf(self, args):

        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for i, concept in enumerate(self.concepts):
            idx = str(i+1) + "_" + slug(concept["sense"])
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["sense"],
                    POS=concept["pos"],
                    Concepticon_ID=concept["Concepticon_ID"],
                    Concepticon_Gloss=concept["Concepticon_Gloss"]
                    )
            concepts[concept["sense"], concept["pos"]] = idx
        args.log.info("added concepts")

        # add languages
        args.writer.add_languages()
        args.log.info("added languages")

        # add forms
        for idx, row in enumerate(self.raw_dir.read_csv(
                "Streitberg-1910-3645.tsv", delimiter="\t", dicts=True)[1:]):
            args.writer.add_forms_from_value(
                Local_ID=idx,
                Language_ID="Gothic",
                Parameter_ID=concepts[cln(row["sense"]), cln(row["pos"])],
                Value=row["form"],
                Source="557564")

        args.log.info("added forms")
