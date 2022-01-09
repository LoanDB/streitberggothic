import pathlib

from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import Language
from pylexibank import FormSpec
import attr

@attr.s
class CustomLanguage(Language):
    attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "streitberggothic"
    
    language_class = CustomLanguage
    
    form_spec = FormSpec(separators=",", first_form_only=True)

    def cmd_makecldf(self, args):
    
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        for i, concept in enumerate(self.concepts):
            args.writer.add_concept(
                    ID=i,
                    Name=concept["sense"]
                    )
        args.log.info("added concepts")
            
        args.writer.add_languages()
        args.log.info("added languages")
        
        df = self.raw_dir.read_csv(
            "Streitberg-1910-3659.tsv", delimiter="\t", 
        )

        for idx, row in enumerate(df[1:]):
            args.writer.add_forms_from_value(
                ID=idx,
                Language_ID = "goth1244",
                Parameter_ID = f"{idx}",
                Value = row[0]
                )