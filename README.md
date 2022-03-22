# 使用CRF++对人民日报的数据进行分词
1. 下载windows版本CRF++0.58
    解压即可,无须其他处理
2. 下载人民日报数据,原始数据路径segmentation/corpus/people-daily.txt,是一个进行词性标注了的数据
3. segmentation/get_data.py对人民日报数据进行预处理,按CRF++中example/seg中数据的模式写入people-daily-train.txt和people-daily-test.txt两个文件中
    people-daily-train.txt可以用于训练,people-daily-test.txt用于测试
4. 参考CRF++中的训练和测试shell脚本,编写train.sh和test.sh两个shell脚本
5. 将CRF++包中的libcrfpp.dll复制粘贴到与train.sh和test.sh同级目录
6. 将CRF++包中的example/seg/template复制粘贴到segmentation下并重命名为seg-template
7. 在windows上执行shell脚本
    1）安装git;
    2) 打开git bash;
    3) 进入train.sh和test.sh所在目录
    4) sh train.sh / sh test.sh

## train.sh

//train command: crf_learn template_file train_file model_file
../CRF++-0.58-windows/crf_learn -f 3 -c 4.0 ./seg-template ./corpus/people-daily-train.txt ./model

## predict.sh

//predict command: crf_test -m model_file test_files ...
../CRF++-0.58-windows/crf_test -m ./model ./corpus/people-daily-test.txt
