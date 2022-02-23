import pathlib

from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec, Concept
import pylexibank
from cldfbench import CLDFSpec
from clldutils.misc import slug
import attr

REP = [(x, "") for x in "†*[]~?;+-"] + [(" ", "_"), (",_", ", ")]

@attr.s
class CustomConcept(Concept):
    POS = attr.ib(default=None)



class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "streitberggothic"

    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements=REP)

    concept_class = CustomConcept

    def cldf_specs(self):
        return {
            None: pylexibank.Dataset.cldf_specs(self),
            "dictionary": CLDFSpec(
                module="Dictionary",
                dir=self.cldf_dir,
            ),
        }

    def cmd_makecldf(self, args):

        with self.cldf_writer(args) as writer:
            writer.add_sources()
            args.log.info("added sources")

            # add concept
            concepts = {}
            for i, concept in enumerate(self.concepts):
                idx = str(i+1)+"_"+slug(concept["sense"])
                writer.add_concept(
                        ID=idx,
                        Name=concept["sense"],
                        POS=concept["pos"],
                        Concepticon_ID=concept["CONCEPTICON_ID"],
                        Concepticon_Gloss=concept["CONCEPTICON_GLOSS"]
                        )
                concepts[concept["sense"], concept["pos"]] = idx
            args.log.info("added concepts")

            # add languages
            writer.add_languages()
            args.log.info("added languages")

            language_table = writer.cldf["LanguageTable"]

            # add forms
            for idx, row in enumerate(self.raw_dir.read_csv(
                    "Streitberg-1910-3659.tsv", delimiter="\t", dicts=True)[1:]):
                writer.add_forms_from_value(
                    Local_ID=idx,
                    Language_ID="Gothic",
                    Parameter_ID=concepts[row["sense"], row["pos"]],
                    Value=row["form"],
                    Source="557564")
            args.log.info("added forms")
        with self.cldf_writer(args, cldf_spec="dictionary", clean=False) as writer:
            writer.cldf.add_component(language_table)
            for idx, row in enumerate(self.raw_dir.read_csv(
                "Streitberg-1910-3659.tsv", delimiter="\t", dicts=True)):
                entry_id = "{0}-{1}".format(idx+1, slug(row["form"]))
                sense_id = "{0}-{1}".format(idx+1, slug(row["sense"]))
                writer.objects["EntryTable"].append({
                    "ID": entry_id,
                    "Language_ID": "Gothic",
                    "Headword": row["form"],
                    "Part_Of_Speech": row["pos"]
                    })
                writer.objects["SenseTable"].append({
                    "ID": sense_id,
                    "Description": row["sense"],
                    "Entry_ID": entry_id
                    })
