import re
from ipa2 import IPA2, dragonmapper

#ipa = IPA2('eng-us')
#print(ipa.convert_sent("International Phonetic Alphabet"))

string_array = ["apple", "banana", "orange"]
print(True in [s.startswith('aaa') for s in string_array])

ipa = IPA2('zho-s')
print(ipa.convert_sent("一一"))
print(ipa.convert_sent("一共 26859 人"))
print(ipa.convert_sent("在 Python 3.4 及以上版本，你可以使用 pathlib 模块"))
print(ipa.convert_sent("你可以使用pathlib模块"))

print('-'*20)
text = "你可以使用pathlib模块"
text = "一一"
pattern_ascii = re.compile(r"[\u0041-\u005A\u0061-\u007A\u00C0-\u00FF\u0100-\u017F\u0180-\u024F]+")
nrm_text = ''
start_idx = 0
end_idx = 0
for item in list(pattern_ascii.finditer(text)):
    start_idx, end_idx = item.span()
    if start_idx > 0:
        nrm_text += dragonmapper.hanzi.to_ipa(text[:start_idx]) + ' '
    nrm_text += item.group() + ' '
if end_idx < len(text):
    nrm_text += dragonmapper.hanzi.to_ipa(text[end_idx:])

print(text)
print(nrm_text)
print(dragonmapper.hanzi.to_pinyin(nrm_text))
print(dragonmapper.hanzi.to_ipa(nrm_text))
print(dragonmapper.hanzi.to_pinyin('殷'))
print(dragonmapper.hanzi.to_ipa('a'))