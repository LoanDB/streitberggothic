import pathlib

from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "streitberggothic"

    def cldf_specs(self):
        from cldfbench import CLDFSpec
        return CLDFSpec(dir=self.cldf_dir, module='Wordlist') 

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        >>> args.writer.objects['LanguageTable'].append(...)
        """
        # add bib
        #args.writer.add_sources()
        #args.log.info("added sources")

        # add language
        #args.writer.add_languages()
        #args.log.info("added languages")
        
        from csvw.dsv_dialects import Dialect
        currentid = 0
        for row in self.raw_dir.read_csv(
            'Streitberg-1910-3659.tsv',
            dicts=True, 
            dialect=Dialect(delimiter='\t', header=True)
        ):

            args.writer.objects['FormTable'].append({
                'ID': currentid,
                'Language_ID': 0,
                'Parameter_ID': currentid,
                'Value': row["form"],})

            args.writer.objects['ParameterTable'].append({
                'ID': currentid,
                'Name': row["sense"],})
            currentid+=1