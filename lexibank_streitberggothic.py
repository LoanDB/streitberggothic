import pathlib

from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import Language
from pylexibank import FormSpec
import attr

class CustomLanguage(Language):
    pass

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
        concepts = {}
        for i, concept in enumerate(self.concepts):
            idx = f"{i}_{slug(concept['sense'])}"
            concepts[concept["sense"]] = idx
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["sense"]
                    )
        args.log.info("added concepts")
        
        # add language
        args.writer.add_languages()
            