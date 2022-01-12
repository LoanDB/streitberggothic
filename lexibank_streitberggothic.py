import pathlib

from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec

REP = [(x, "") for x in "†*[]~?;+-"] + [(" ", "_"), (",_", ", ")]


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "streitberggothic"

    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements=REP)

    def cmd_makecldf(self, args):

        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        for i, concept in enumerate(self.concepts):
            args.writer.add_concept(
                    ID=i,
                    Name=concept["sense"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"]
                    )
        args.log.info("added concepts")

        # add languages
        args.writer.add_languages()
        args.log.info("added languages")

        # add forms
        for idx, row in enumerate(self.raw_dir.read_csv(
                "Streitberg-1910-3659.tsv", delimiter="\t")[1:]):
            args.writer.add_forms_from_value(
                ID=idx,
                Language_ID=str(0),
                Parameter_ID=str(idx),
                Value=row[0],
                Source="557564")

        args.log.info("added forms")
