import itertools

import nlp2
import eng_to_ipa as ipa
from pathlib import Path
from . import dragonmapper
#from .tamil2ipa import txt2ipa
from .kannada2ipa import kannada2ipa
import epitran


class IPA2:
    def __init__(self, lang='yue'):
        super().__init__()
        self.data = {}
        self.lang = lang
        self.epi = None
        if isinstance(lang, str):
            if lang == 'kan':
                pass
            else:
                if lang == 'lao':
                    self.lao_epi = epitran.Epitran('lao-Laoo')
                elif lang == 'tam':
                    self.epi = epitran.Epitran('tam-Taml')
                elif lang == 'amh':
                    self.epi = epitran.Epitran('amh-Ethi')
                elif lang == 'aze':
                    self.epi = epitran.Epitran('aze-Latn')
                elif lang == 'cze':
                    self.epi = epitran.Epitran('ces-Latn')
                elif lang == 'ger':
                    self.epi = epitran.Epitran('deu-Latn')
                elif lang == 'spa':
                    self.epi = epitran.Epitran('spa-Latn-eu')
                elif lang == 'spa-latin':
                    self.epi = epitran.Epitran('spa-Latn')
                elif lang == 'fas':
                    self.epi = epitran.Epitran('fas-Arab')
                elif lang == 'fra':
                    self.epi = epitran.Epitran('fra-Latn')
                elif lang == 'hun':
                    self.epi = epitran.Epitran('hun-Latn')
                elif lang == 'ind':
                    self.epi = epitran.Epitran('ind-Latn')
                elif lang == 'ita':
                    self.epi = epitran.Epitran('ita-Latn')
                elif lang == 'khm':
                    self.epi = epitran.Epitran('khm-Khmr')
                elif lang == 'kaz':
                    self.epi = epitran.Epitran('kaz-Cyrl')
                elif lang == 'msa':
                    self.epi = epitran.Epitran('msa-Latn')
                elif lang == 'bur':
                    self.epi = epitran.Epitran('mya-Mymr')
                elif lang == 'pol':
                    self.epi = epitran.Epitran('pol-Latn')
                elif lang == 'por-po':
                    self.epi = epitran.Epitran('por-Latn')
                elif lang == 'swe':
                    self.epi = epitran.Epitran('swe-Latn')
                elif lang == 'ron':
                    self.epi = epitran.Epitran('ron-Latn')
                elif lang == 'rus':
                    self.epi = epitran.Epitran('rus-Cyrl')
                elif lang == 'tgl':
                    self.epi = epitran.Epitran('tgl-Latn')
                elif lang == 'tur':
                    self.epi = epitran.Epitran('tur-Latn')
                elif lang == 'tha':
                    self.epi = epitran.Epitran('tha-Thai')
                elif lang == 'vie-n':
                    self.epi = epitran.Epitran('vie-Latn')
                elif lang == 'dut':
                    self.epi = epitran.Epitran('nld-Latn')
                elif lang == 'ukr':
                    self.epi = epitran.Epitran('ukr-Cyrl')
                self.data = self.load_lang_to_list(lang)
        elif isinstance(lang, list):
            for i in lang:
                if i == 'kan':
                    pass
                else:
                    if i == 'lao':
                        self.lao_epi = epitran.Epitran('lao-Laoo')
                    elif i == 'tam':
                        self.epi = epitran.Epitran('tam-Taml')
                    elif i == 'amh':
                        self.epi = epitran.Epitran('amh-Ethi')
                    elif i == 'aze':
                        self.epi = epitran.Epitran('aze-Latn')
                    elif i == 'cze':
                        self.epi = epitran.Epitran('ces-Latn')
                    elif i == 'ger':
                        self.epi = epitran.Epitran('deu-Latn')
                    elif i == 'spa':
                        self.epi = epitran.Epitran('spa-Latn-eu')
                    elif i == 'spa-latin':
                        self.epi = epitran.Epitran('spa-Latn')
                    elif i == 'fas':
                        self.epi = epitran.Epitran('fas-Arab')
                    elif i == 'fra':
                        self.epi = epitran.Epitran('fra-Latn')
                    elif i == 'hun':
                        self.epi = epitran.Epitran('hun-Latn')
                    elif i == 'ind':
                        self.epi = epitran.Epitran('ind-Latn')
                    elif i == 'ita':
                        self.epi = epitran.Epitran('ita-Latn')
                    elif i == 'khm':
                        self.epi = epitran.Epitran('khm-Khmr')
                    elif i == 'kaz':
                        self.epi = epitran.Epitran('kaz-Cyrl')
                    elif i == 'msa':
                        self.epi = epitran.Epitran('msa-Latn')
                    elif i == 'bur':
                        self.epi = epitran.Epitran('mya-Mymr')
                    elif i == 'pol':
                        self.epi = epitran.Epitran('pol-Latn')
                    elif i == 'por-po':
                        self.epi = epitran.Epitran('por-Latn')
                    elif i == 'swe':
                        self.epi = epitran.Epitran('swe-Latn')
                    elif i == 'ron':
                        self.epi = epitran.Epitran('ron-Latn')
                    elif i == 'rus':
                        self.epi = epitran.Epitran('rus-Cyrl')
                    elif i == 'tgl':
                        self.epi = epitran.Epitran('tgl-Latn')
                    elif i == 'tur':
                        self.epi = epitran.Epitran('tur-Latn')
                    elif i == 'tha':
                        self.epi = epitran.Epitran('tha-Thai')
                    elif i == 'vie-n':
                        self.epi = epitran.Epitran('vie-Latn')
                    elif i == 'dut':
                        self.epi = epitran.Epitran('nld-Latn')
                    elif i == 'ukr':
                        self.epi = epitran.Epitran('ukr-Cyrl')
                    self.data.update(self.load_lang_to_list(i))

    def load_lang_to_list(self, lang):
        file_loc = (Path(__file__).parent / 'data' / (lang + '.tsv')).resolve()
        if nlp2.is_file_exist(file_loc):
            tdict = nlp2.read_csv(file_loc, delimiter='\t')
            t = {}
            for i in tdict:
                t[i[0]] = i[1]
            return t
        else:
            raise FileNotFoundError(f"{lang} not supported as `data/{lang}.tsv` is not provided...")

    def hanzi_to_ipa(self, text, retrieve_all=False):
        if retrieve_all:
            s = dragonmapper.hanzi.to_ipa(text, all_readings=True)
            s = s.replace('/', ' ')
            s = s.replace('[', '["')
            s = s.replace(']', '"]')
            s = s.replace('][', ',')
            return eval(s)
        return [dragonmapper.hanzi.to_ipa(text, all_readings=False)]

    def retrieve_not_converted_char(self, not_converted_char, retrieve_all=False):
        if (isinstance(self.lang, str) and self.lang.startswith('zho-')) or (isinstance(self.lang, list) and True in [s.startswith('zho-') for s in self.lang]):
            return self.hanzi_to_ipa(not_converted_char, retrieve_all)
        elif (isinstance(self.lang, str) and self.lang.startswith('eng-')) or (isinstance(self.lang, list) and True in [s.startswith('eng-') for s in self.lang]):
            return [ipa.convert(not_converted_char)]
        elif self.epi is not None:
            return [self.epi.transliterate(not_converted_char)]
        else:
            return [not_converted_char]

    def convert_sent(self, _input, retrieve_all=False):
        if (isinstance(self.lang, str) and self.lang == 'kan') or (isinstance(self.lang, list) and True in [s == 'kan' for s in self.lang]):
            return [kannada2ipa(_input)]
        if (isinstance(self.lang, str) and self.lang == 'lao') or (isinstance(self.lang, list) and True in [s == 'lao' for s in self.lang]):
            return [self.lao_epi.transliterate(_input)]
        if (isinstance(self.lang, str) and self.lang.startswith('eng-')) or (isinstance(self.lang, list) and True in [s.startswith('eng-') for s in self.lang]):
            return [ipa.convert(_input)]

        _input = nlp2.split_sentence_to_array(_input.lower(), False)
        result = []
        # maximum match
        senlen = len(_input)
        start = 0
        while start < senlen:
            matched = False
            for i in range(senlen, 0, -1):
                string = "".join(_input[start:start + i])
                if string in self.data:
                    result.append(string)
                    matched = True
                    break
            if not matched:
                i = 1
                result.append(_input[start])
            start += i

        # get all combination
        ipa_result = []
        not_converted_char = None
        for i in result:
            if i in self.data:
                if not_converted_char is not None:
                    ipa_result.append(self.retrieve_not_converted_char(not_converted_char, retrieve_all))
                if retrieve_all:
                    ipa_result.append(self.data[i].split(","))
                else:
                    ipa_result.append([self.data[i].split(",")[0]])
                not_converted_char = None
            else:
                if not_converted_char is None:
                    not_converted_char = ''
                not_converted_char += i
        if not_converted_char is not None:
            ipa_result.append(self.retrieve_not_converted_char(not_converted_char, retrieve_all))

        return [" ".join(x).strip() for x in itertools.product(*ipa_result)]
