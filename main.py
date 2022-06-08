#coding=utf-8
import os
import jieba as jb
from dotenv import load_dotenv
import mariadb

load_dotenv()

"""
DB schema:
id, title, url, time, keyword, content, emotional_value
"""


def dictionary(positive_words, negative_words):
    with open('./library/NTUSD_positive_unicode.txt', encoding='utf-8', mode='r') as f:
        for i in f:
            positive_words.append(i.strip())

    with open('./library/positive.txt', encoding='utf-8', mode='r') as f:
        for i in f:
            positive_words.append(i.strip())

    with open('./library/NTUSD_negative_unicode.txt', encoding='utf-8', mode='r') as f:
        for k in f:
            negative_words.append(k.strip())

    with open('./library/negative.txt', encoding='utf-8', mode='r') as f:
        for k in f:
            negative_words.append(k.strip())

    return positive_words, negative_words


def analysis(positive_words, negative_words, article):
    score = 0
    jieba_result = jb.cut(article, cut_all=False, HMM=True)
    for word in jieba_result:
        #add = False
        #neg = False
        sign = "0123456789abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+-*/<>,.[]\/，。、 ！？©；「」～※【】《》（）"
        if word in sign:
            continue
        elif word in positive_words:
            score += 1.1
            #add = True
        elif word in negative_words:
            score -= 1.1
            #neg = True
        else:
            pass
        # 每個拆完的字的狀況
        # print(f'word:{word}, add:{add}, neg:{neg}, now_sum:{score}')
    #print("\n Total score is : ", score)
    return score


def sql_query():
    sql_connect = mariadb.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USERNAME'), passwd=os.getenv('DB_PASSWORD'),
                                  database=os.getenv('DB_DATABASE'))

    cursor = sql_connect.cursor()
    sql = "SELECT id,content,emotional_value FROM articles WHERE emotional_value IS NULL "
    cursor.execute(sql)
    data = cursor.fetchall()
    """
    for i in data:
        print(i)
    """
    cursor.close()
    sql_connect.close()
    return data


def send_score_to_sql(id_index, score):
    sql_connect = mariadb.connect(host=os.getenv('DB_HOST'),
                                  user=os.getenv('DB_USERNAME'),
                                  passwd=os.getenv('DB_PASSWORD'),
                                  database=os.getenv('DB_DATABASE'))

    cursor = sql_connect.cursor()
    sql = "UPDATE articles SET emotional_value="+ str(score) +" where id="+ str(id_index)
    cursor.execute(sql)
    sql_connect.commit()
    cursor.close()
    sql_connect.close()


def main():
    positive_words = []
    negative_words = []
    positive_words, negative_words = dictionary(positive_words, negative_words)

    jb.set_dictionary('./library/dict.txt.big')

    # article[][][] (List)分別是 id, contents, emotional_value
    article = sql_query()

    # query 有幾個就要分析幾次並記錄到資料庫
    for i in range(len(article)):
        result_score = analysis(positive_words, negative_words, article[i][1])
        send_score_to_sql(article[i][0], result_score)


if __name__ == '__main__':
    main()
