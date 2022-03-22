import re
import sys
from functools import reduce

"""
使用people-daily.txt的数据进行分词
原数据是每一行数据进行了词性标注
将词性标注的数据转为分词的数据

crf++的example中示例数据如下：
よ	h	I
っ	h	I
て	h	I
私	k	B
た	h	B

需要上数据也处理成示例数据的模式,如下:
处理前:
    完成/v 祖国/n 统一/vn ，/w 是/v 大势所趋/i ，/w 民心所向/l 。/w
处理后：(B标识分词开头,E标识分词结束,M标识分词中间,S标识单个分词)
    完   B
    成   E
    祖   B
    国   E
    统   B
    一   E
    ，   S
    是   S
    大   B
    势   M
    所   M
    趋   E
    ，   S
    民   B
    心   M
    所   M
    向   E
    。   S
"""


def write2file(cleared_tokens, f):
    for token in cleared_tokens:
        if len(token) == 1:
            f.write(token + '\t' + 'S\n')
            continue
        if len(token) == 2:
            f.write(token[0] + '\t' + 'B\n')
            f.write(token[1] + '\t' + 'E\n')
            continue
        for index, char in enumerate(token):
            if index == 0:
                f.write(char + '\t' + 'B\n')
            elif index == len(token) - 1:
                f.write(char + '\t' + 'E\n')
            else:
                f.write(char + '\t' + 'M\n')


filename = './corpus/people-daily.txt'
train_filename = './corpus/people-daily-train.txt'
test_filename = './corpus/people-daily-test.txt'
f_train = open(train_filename, 'w', encoding='utf-8')
f_test = open(test_filename, 'w', encoding='utf-8')
count = 0
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        # line = '19980101-01-001-006/m 在/p １９９８年/t 来临/v 之际/f ，/w 我/r 十分/m 高兴/a 地/u 通过/p [中央/n 人民/n 广播/vn 电台/n]nt 、/w [中国/ns 国际/n 广播/vn 电台/n]nt 和/c [中央/n 电视台/n]nt ，/w 向/p 全国/n 各族/r 人民/n ，/w 向/p [香港/ns 特别/a 行政区/n]ns 同胞/n 、/w 澳门/ns 和/c 台湾/ns 同胞/n 、/w 海外/s 侨胞/n ，/w 向/p 世界/n 各国/r 的/u 朋友/n 们/k ，/w 致以/v 诚挚/a 的/u 问候/vn 和/c 良好/a 的/u 祝愿/vn ！/w '
        tokens = re.split(r'\s', line)
        # 将类似[中央/n 人民/n 广播/vn 电台/n]nt拆分为'[中央/n', '人民/n', '广播/vn', '电台/n]nt'的进行合并操作
        processed_tokens = []
        combine_token = ''
        for token in tokens:
            # 检测token是否以[开头
            if re.match(r'\[', token) and combine_token == '':
                combine_token += token
                continue
            # 检测token是否以]结尾
            if combine_token != '':
                combine_token += token
                if re.findall(r'\]', token):
                    processed_tokens.append(combine_token)
                    combine_token = ''
                continue
            # 上述两种情况不符合且combine_token为空的情况
            if combine_token == '':
                processed_tokens.append(token)
        # 对processed_token中每个元素进行重新处理
        # 去掉第一个token 去掉标注
        cleared_tokens = []
        for index, token in enumerate(processed_tokens):
            if index == 0:
                continue
            else:
                if re.findall(r'/[a-z]+$', token):
                    cleared_token = re.sub(r'/[a-z]+$', '', token)
                    cleared_tokens.append(cleared_token)
                if re.findall(r'^\[.*][a-z]+$', token):
                    cleared_token = re.sub(r'/[a-z]+', '', re.sub(r'^\[|][a-z]+$', '', token))
                    cleared_tokens.append(cleared_token)
        # print(processed_tokens)
        # print(cleared_tokens)
        # print(reduce(lambda x, y: x + y, cleared_tokens))
        if not cleared_tokens:
            continue
        if count <= 2001:
            write2file(cleared_tokens, f_train)
            f_train.write('\n')
        else:
            write2file(cleared_tokens, f_test)
            f_test.write('\n')
        count += 1
f_train.close()
f_test.close()
