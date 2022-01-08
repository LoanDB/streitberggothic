import pathlib

from cldfbench import Dataset as BaseDataset


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
        from csvw.dsv_dialects import Dialect
        currentid = 0
        for row in self.raw_dir.read_csv(
            'Streitberg-1910-3659.tsv',
            dicts=True, 
            dialect=Dialect(delimiter='\t', header=True)
        ):

            args.writer.objects['FormTable'].append({
                'ID': currentid,
                'Form': row["form"],
                'Gloss': row["sense"],
                'Language_ID': 0})
            currentid+=1
