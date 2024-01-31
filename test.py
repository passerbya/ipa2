from ipa2 import IPA2

ipa = IPA2('eng-us')
print(ipa.convert_sent("International Phonetic Alphabet"))

ipa = IPA2('zho-s')
print(ipa.convert_sent("一共 26859 人"))
print(ipa.convert_sent("在 Python 3.4 及以上版本，你可以使用 pathlib 模块"))
