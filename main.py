#coding=utf-8
import jieba as jb

jb.set_dictionary('./library/dict.txt.big')

file = open('./text/data.txt', 'r', encoding='utf-8')
article_origin = []
for line in file:
    article_origin.append(line)
file.close()
article = ''.join(article_origin)

with open('./library/NTUSD_positive_unicode.txt', encoding='utf-8', mode='r') as f:
    positive_words = []
    for i in f:
        positive_words.append(i.strip())

with open('./library/positive.txt', encoding='utf-8', mode='r') as f:
    for i in f:
        positive_words.append(i.strip())

with open('./library/NTUSD_negative_unicode.txt', encoding='utf-8', mode='r') as f:
    negative_words = []
    for k in f:
        negative_words.append(k.strip())

with open('./library/negative.txt', encoding='utf-8', mode='r') as f:
    for k in f:
        negative_words.append(k.strip())

score = 0
jieba_result = jb.cut(article, cut_all=False, HMM=True)
for word in jieba_result:
    add = False
    neg = False
    sign = "0123456789abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+-*/<>,.[]\/，。、 ！？©；「」～※【】《》（）"
    if word in sign:
        continue
    elif word in positive_words:
        score += 1
        add = True
    elif word in negative_words:
        score -= 1
        neg = True
    else:
        pass
    #每個拆完的字的狀況
    print(f'word:{word}, add:{add}, neg:{neg}, now_sum:{score}')

print("\n Total score is : ", score)

#DB schema:
#id, title, url, time, keyword, content, emotional_value
