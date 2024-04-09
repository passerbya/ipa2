import re
from ipa2 import IPA2
from ipa2.tamil2ipa import txt2ipa
from ipa2.kannada2ipa import kannada2ipa
from ipa2.kana2ipa import kana2ipa
import epitran
import pykakasi
from ipa2.vphon import vPhon

print(vPhon.main(['--text', 'Chúng tôi','--dialect', 'n']))
ipa = IPA2('vie-n')
print(ipa.convert_sent('Chúng tôi'))


ipa = IPA2('zho-s')
print(ipa.convert_sent("长牛羊", retrieve_all=True))
print(ipa.convert_sent("一一"))
print(ipa.convert_sent("一共 26859 人"))
print(ipa.convert_sent("在 Python 3.4 及以上版本，你可以使用 pathlib 模块"))
print(ipa.convert_sent("你可以使用pathlib模块"))

text = "你可以使用pathlib模块"
print(ipa.convert_sent("长长", retrieve_all=True))

import pykakasi
kks = pykakasi.kakasi()
text = "かな漢字123"
result = kks.convert(text)
spell = ''
sep = ''
for item in result:
    kana = item['kana']
    if len(kana) == 0:
        kana = item['hira']
    spell += sep + kana
    sep  = ' '

print(spell)

text = 'வணக்கம் தமிழகம் '
print(txt2ipa(text))
ipa = IPA2('tam')

epi = epitran.Epitran('tam-Taml')
print(epi.transliterate(text))

print(ipa.convert_sent(text))

text = 'ಇವತ್ತಿನ ಹವಾಮಾನ ಚನ್ನಾಗಿದೆ'
print(kannada2ipa(text))

ipa = IPA2(['kan'])
print(ipa.convert_sent(text))

ipa = IPA2('eng-us')
print(ipa.convert_sent("Hello, how are you?"))
print(ipa.convert_sent("The trains were late, and, of course, overcrowded; there was enough luggage in our compartment to have filled it, and still there was one more passenger than there ought to have been; an ill conditioned old fellow who wanted my hat box put into the van because it happened to tumble off the rack on to his head."))

string_array = ["apple", "banana", "orange"]
print(True in [s.startswith('aaa') for s in string_array])

text='ぴゃ'
kks = pykakasi.kakasi()
result = kks.convert(text)
if result is not None and len(result) >0:
    spell = ''
    sep = ''
    for item in result:
        spell += sep + kana2ipa(item['hepburn'])
        sep  = ' '
    print(spell)
print(kana2ipa(text))


text='좋거든요'
ipa = IPA2(['kor'])
print(ipa.convert_sent(text))

text='国際音声記号 は、ラテンアルファベットに基づく音声システムであり、19世紀の終わりに国際音声記号協会によって音声発音の標準表記として設計されました。'
ipa = IPA2(['jpn'])
print(ipa.convert_sent(text))

import jaconv
text = 'ティロ・フィナーレａｂｃ１２３'
print(jaconv.z2h(text, kana=False, ascii=True, digit=True))
#text='て'
print(jaconv.alphabet2kana(jaconv.normalize(text, mode='NFKC')))
