import pathlib
import re

import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec, Lexeme
import pylexibank
from cldfbench import CLDFSpec
from clldutils.misc import slug
import attr
from collections import defaultdict

REP = [(x, "") for x in "†*[]~?;+-"] + \
      [(x, "a") for x in "áàā"] + [(x, "ɪ") for x in "ïíìī"] + \
      [("ē", "e"), ("ō", "o"), ("ū", "u"), (" ", "_"), (",_", ", ")]


@attr.s
class CustomLexeme(Lexeme):
    Meaning = attr.ib(default=None)
    Sense_ID = attr.ib(default=None)
    Entry_ID = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "streitberggothic"

    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements=REP)
    lexeme_class = CustomLexeme

    def cldf_specs(self):
        return {
            None: pylexibank.Dataset.cldf_specs(self),
            "dictionary": CLDFSpec(
                module="Dictionary",
                dir=self.cldf_dir,
            ),
        }

    def cmd_makecldf(self, args):
        senses = defaultdict(list)
        idxs = {}
        form2idx = {}
        # assemble senses
        for idx, row in enumerate(self.raw_dir.read_csv(
            "Streitberg-1910-3645.tsv", delimiter="\t", dicts=True)):
            if row["sense"].strip():
                fidx = str(idx+1)+"-"+slug(row["form"])
                idxs[fidx] = row
                for sense in re.split("[,;]", row["sense"]):
                    if row["form"].strip() and sense.strip():
                        senses[slug(sense, lowercase=False)] += [(fidx, sense)]
                        form2idx[row["form"], sense.strip()] = fidx

        with self.cldf_writer(args) as writer:
            writer.add_sources()
            ## add concept
            concepts = {}
            for concept in self.conceptlists[0].concepts.values():
                idx = "{0}-{1}".format(concept.number, slug(concept.gloss))
                writer.add_concept(
                        ID=idx,
                        Name=concept.gloss,
                        Concepticon_ID=concept.concepticon_id,
                        Concepticon_Gloss=concept.concepticon_gloss,
                        )
                concepts[concept.concepticon_id] = idx
            args.log.info("added concepts")

            ## add languages
            for language in self.languages:
                writer.add_language(
                        ID="Gothic",
                        Name="Gothic",
                        Glottocode="goth1244"
                        )
            args.log.info("added languages")

            language_table = writer.cldf["LanguageTable"]

            ## add forms
            for row in self.raw_dir.read_csv(
                "wordlist.tsv", delimiter="\t", dicts=True):
                writer.add_forms_from_value(
                    Local_ID=row["ID"],
                    Language_ID="Gothic",
                    Parameter_ID=concepts[row["CONCEPTICON_ID"]],
                    Value=row["FORM"],
                    Meaning=row["MEANING"],
                    Entry_ID=form2idx[row["FORM"], row["SENSE"]],
                    Sense_ID=row["SENSE_ID"],
                    Source="557564"
                    )

        with self.cldf_writer(args, cldf_spec="dictionary", clean=False) as writer:

            # we use the same language table for the data
            writer.cldf.add_component(language_table)

            for sense, values in senses.items():
                for i, (fidx, sense_desc) in enumerate(values):
                    writer.objects["SenseTable"].append({
                        "ID": sense+"-"+str(i+1),
                        "Description": sense_desc,
                        "Entry_ID": fidx
                        })
            for fidx, row in idxs.items():
                writer.objects["EntryTable"].append({
                    "ID": fidx,
                    "Language_ID": "Gothic",
                    "Headword": row["form"],
                    "Part_of_Speech": row["pos"]
                    })

            #for idx, row in enumerate(self.raw_dir.read_csv(
            #    "Streitberg-1910-3645.tsv", delimiter="\t", dicts=True)):
            #    entry_id = "{0}-{1}".format(idx+1, slug(row["form"]))
            #    sense_id = "{0}-{1}".format(idx+1, slug(row["SENSE"]))
            #    writer.objects["EntryTable"].append({
            #        "ID": entry_id,
            #        "Language_ID": "Gothic",
            #        "Headword": row["form"],
            #        "Part_Of_Speech": row["pos"]
            #        })
            #    writer.objects["SenseTable"].append({
            #        "ID": sense_id,
            #        "Description": row["SENSE"],
            #        "Entry_ID": entry_id
            #        })
