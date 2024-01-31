import itertools

import nlp2
from pathlib import Path


class IPA2:
    def __init__(self, lang='yue'):
        super().__init__()
        self.data = {}
        if isinstance(lang, str):
            self.data = self.load_lang_to_list(lang)
        elif isinstance(lang, list):
            for i in lang:
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
            assert FileNotFoundError(f"{lang} not supported as `data/{lang}.tsv` is not provided...")

    def convert_sent(self, _input='測試的句子'):
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
                    ipa_result.append([not_converted_char])
                ipa_result.append(self.data[i].split(","))
                not_converted_char = None
            else:
                if not_converted_char is None:
                    not_converted_char = ''
                not_converted_char += i

        return [" ".join(x) for x in itertools.product(*ipa_result)]
