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
    
    #language_class = CustomLanguage
    
    # add this part later:
    # form_spec = FormSpec()

    def cmd_makecldf(self, args):

        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        concepts = {}
        for i, concept in enumerate(self.etc_dir.read_csv("concepts.tsv", delimiter="\t", dicts=True)):
            idx = str(i+1)+"_"+slug(concept["gloss"])
            print(concept)
            args.writer.add_concept(ID=idx, Name=concept["gloss"])
            concepts[concept["gloss"]] = idx
    
        # add language
        print(self.languages)
        languages = args.writer.add_languages()
        print("hi")
        #args.log.info("added languages")
        
        # add senses (link to concepticon later)
#        currentid = 0
 #       for concept in self.concepts:
  #          idx = f"{currentid}_{slug(concept['sense'])}"
   #         concepts[concept["sense"]] = idx
    #        args.writer.add_concept(
     #           ID=idx,
      #          Name=concept["sense"])
       #     currentid += 1
        #args.log.info("added senses")
        

        
        # read in data
#        data = self.raw_dir.read_csv(
 #           'Streitberg-1910-3659.tsv', delimiter="\t",
  #          header=True
   #     )
#
 #       for i in range(1, len(data)):
  #          args.writer.add_forms_from_value(
   #                                     Language_ID=0,
    #                                    Parameter_ID=concepts[concept],
     #                                   Value=data[i][0].strip(),
      #                                  )