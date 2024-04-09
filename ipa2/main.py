import os
import re
import itertools

import nlp2
import eng_to_ipa as ipa
from pathlib import Path
#from .tamil2ipa import txt2ipa
from .kannada2ipa import kannada2ipa
from .worker import to_jamo
from .kana2ipa import kana2ipa
from .vphon import vPhon
import epitran
import pykakasi
from pypinyin import pinyin, Style
from pinyin_to_ipa import pinyin_to_ipa
from pypinyin_dict.phrase_pinyin_data import large_pinyin
#from persian_phonemizer import Phonemizer


class IPA2:
    def __init__(self, lang='yue'):
        super().__init__()
        self.data = {}
        self.lang = lang
        self.epi = None
        self.lao_epi = None
        self.ur2sr = None
        self.phonemizer = None
        if isinstance(lang, str):
            if lang.startswith('zho-'):
                large_pinyin.load()
            elif lang == 'fas':
                self.phonemizer = Phonemizer()
            elif lang == 'kor':
                os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
                from fairseq.models.transformer import TransformerModel
                resources = Path(__file__).parent / 'resources'
                data_bin = str(resources / 'bin')
                model = str(resources / 'model_transformer')
                self.ur2sr = TransformerModel.from_pretrained(
                    model,
                    checkpoint_file='checkpoint200.pt',
                    data_name_or_path=data_bin,
                    bpe='sentencepiece',
                    sentencepiece_model=str(resources / 'spm.model'),
                    source_lang='ur',
                    target_lang='sr'
                )
            elif lang == 'kan':
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
                if self.lang == 'jpn':
                    self.kks = pykakasi.kakasi()
                self.data = self.load_lang_to_list(lang)
        elif isinstance(lang, list):
            for i in lang:
                if i.startswith('zho-'):
                    large_pinyin.load()
                elif i == 'fas':
                    self.phonemizer = Phonemizer()
                elif i == 'kor':
                    os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
                    from fairseq.models.transformer import TransformerModel
                    resources = Path(__file__).parent / 'resources'
                    data_bin = str(resources / 'bin')
                    model = str(resources / 'model_transformer')
                    self.ur2sr = TransformerModel.from_pretrained(
                        model,
                        checkpoint_file='checkpoint200.pt',
                        data_name_or_path=data_bin,
                        bpe='sentencepiece',
                        sentencepiece_model=str(resources / 'spm.model'),
                        source_lang='ur',
                        target_lang='sr'
                    )
                elif i == 'kan':
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
                    if i == 'jpn':
                        self.kks = pykakasi.kakasi()
                    self.data.update(self.load_lang_to_list(i))

    def load_lang_to_list(self, lang):
        file_loc = (Path(__file__).parent / 'data' / (lang + '.tsv')).resolve()
        t = {}
        if nlp2.is_file_exist(file_loc):
            tdict = nlp2.read_csv(file_loc, delimiter='\t')
            for i in tdict:
                t[i[0]] = i[1]
        else:
            file_loc = None

        if lang == 'ar':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'ar.txt').resolve()
        elif lang == 'ger':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'de.txt').resolve()
        elif lang == 'eng-us':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'en_US.txt').resolve()
        elif lang == 'eng-uk':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'en_UK.txt').resolve()
        elif lang == 'spa':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'es_ES.txt').resolve()
        elif lang == 'spa-me':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'es_MX.txt').resolve()
        elif lang == 'fas':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'fa.txt').resolve()
        elif lang == 'fin':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'fi.txt').resolve()
        elif lang == 'fra':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'fr_FR.txt').resolve()
        elif lang == 'fra-qu':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'fr_QC.txt').resolve()
        elif lang == 'isl':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'is.txt').resolve()
        elif lang == 'jpn':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'ja.txt').resolve()
        elif lang == 'khm':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'km.txt').resolve()
        elif lang == 'kor':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'ko.txt').resolve()
        elif lang == 'msa':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'ma.txt').resolve()
        elif lang == 'nob':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'nb.txt').resolve()
        elif lang == 'dut':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'nl.txt').resolve()
        elif lang == 'ori':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'or.txt').resolve()
        elif lang == 'por-bz':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'pt_BR.txt').resolve()
        elif lang == 'ron':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'ro.txt').resolve()
        elif lang == 'swe':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'sv.txt').resolve()
        elif lang == 'swa':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'sw.txt').resolve()
        elif lang == 'tha':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'tts.txt').resolve()
        elif lang == 'vie-c':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'vi_C.txt').resolve()
        elif lang == 'vie-n':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'vi_N.txt').resolve()
        elif lang == 'vie-s':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'vi_S.txt').resolve()
        elif lang == 'yue':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'yue.txt').resolve()
        elif lang == 'zho-s':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'zh_hans.txt').resolve()
        elif lang == 'zho-t':
            file_loc = (Path(__file__).parent / 'ipa-dict' / 'zh_hant.txt').resolve()

        if file_loc is None:
            raise FileNotFoundError(f"{lang} not supported as `data/{lang}.tsv` is not provided...")

        if str(file_loc).endswith('.txt'):
            tdict = nlp2.read_csv(file_loc, delimiter='\t')
            for i in tdict:
                t[i[0]] = re.sub(',\s*', ',', i[1].replace('/', ''))
        return t

    def hanzi_to_kana(self, text):
        result = self.kks.convert(text)
        if result is not None and len(result) >0:
            spell = ''
            sep = ''
            for item in result:
                hira = kana2ipa(item['hira'])
                spell += sep + hira
                sep  = ' '
        else:
            spell = text
        return spell

    def retrieve_not_converted_char(self, not_converted_char, retrieve_all=False):
        if (isinstance(self.lang, str) and self.lang.startswith('eng-')) or (isinstance(self.lang, list) and True in [s.startswith('eng-') for s in self.lang]):
            return [ipa.convert(not_converted_char)]
        elif (isinstance(self.lang, str) and self.lang == 'jpn') or (isinstance(self.lang, list) and True in [s == 'jpn' for s in self.lang]):
            return [self.hanzi_to_kana(not_converted_char)]
        elif self.epi is not None:
            return [self.epi.transliterate(not_converted_char)]
        else:
            return [not_converted_char]

    def pinyin2ipa(self, txt):
        try:
            res_ipa = pinyin_to_ipa(txt)
            return ''.join(res_ipa[0])
        except:
            return txt

    def convert_sent(self, _input, retrieve_all=False):
        if self.ur2sr is not None:
            jamo = to_jamo(_input)
            return [self.ur2sr.translate(jamo)]
        elif self.lao_epi is not None:
            return [self.lao_epi.transliterate(_input)]
        elif self.phonemizer is not None:
            return [self.phonemizer.phonemize(_input)]
        if (isinstance(self.lang, str) and self.lang == 'kan') or (isinstance(self.lang, list) and True in [s == 'kan' for s in self.lang]):
            return [kannada2ipa(_input)]
        if (isinstance(self.lang, str) and self.lang.startswith('zho-')) or (isinstance(self.lang, list) and True in [s.startswith('zho-') for s in self.lang]):
            result = pinyin(_input, style=Style.TONE3, heteronym=retrieve_all)
            if result is not None and len(result) > 0:
                return [' '.join([self.pinyin2ipa(y) for y in x]) for x in itertools.product(*result)]
        if (isinstance(self.lang, str) and self.lang.startswith('eng-')) or (isinstance(self.lang, list) and True in [s.startswith('eng-') for s in self.lang]):
            return [ipa.convert(_input)]
        if (isinstance(self.lang, str) and self.lang == 'vie-n') or (isinstance(self.lang, list) and True in [s == 'vie-n' for s in self.lang]):
            return [vPhon.main(['--text', _input,'--dialect', 'n'])]
        if (isinstance(self.lang, str) and self.lang == 'vie-c') or (isinstance(self.lang, list) and True in [s == 'vie-c' for s in self.lang]):
            return [vPhon.main(['--text', _input,'--dialect', 'c'])]
        if (isinstance(self.lang, str) and self.lang == 'vie-s') or (isinstance(self.lang, list) and True in [s == 'vie-s' for s in self.lang]):
            return [vPhon.main(['--text', _input,'--dialect', 's'])]

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
