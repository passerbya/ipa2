from pypinyin import pinyin, Style
from pinyin_to_ipa import pinyin_to_ipa
import itertools

txt = '您需要使用另一种方式来表达'
result = pinyin(txt, style=Style.TONE3)
if result is not None and len(result) > 0:
    print(result)
    ch_ipa = ''
    sep = ''
    for res in result:
        res_ipa = pinyin_to_ipa(res[0])
        if len(res_ipa) > 0:
            ch_ipa += sep + ''.join(res_ipa[0])
        else:
            ch_ipa += sep + res[0]
        sep = ' '

print(ch_ipa)