import os
import random
import re


def scanningdir(dir):
    nameArr = []
    funcArr = []
    for parent, dirnames, filenames in os.walk(dir):
        for file in filenames:
            path = parent + "/" + file
            houzhui = path[-2:]

            if houzhui == ".m" and confusionFileName not in path:
                names,funcs = scanningfile(path)
                nameArr += names
                funcArr += funcs
    nameArr = list(set(nameArr))
    funcArr = list(set(funcArr))
    funcArr2 = [i for i in funcArr if i not in nameArr]
    return (nameArr,funcArr2)

def scanningfile(file):
    with open(file) as f:
        text = f.read()
        pattern = "[^_a-zA-Z0-9](%s[_a-zA-Z0-9]+)"%(confusionPre)
        m1 = re.findall(pattern,text)

        pattern = "@implementation[^_a-zA-Z0-9](%s[_a-zA-Z0-9]+)" % (confusionPre)
        m2 = re.findall(pattern, text)
        m3 = [i for i in m1 if i not in m2]
        return (m2,m3)
    return ([],[])


def randomWord(wordNum):
    text = ""
    for i in range(0,random.randint(0,wordNum)):
        num = random.randint(0,len(wordArr)-1)
        if i != 0:
            text += wordArr[num].title()
        else:
            text += wordArr[num]
    return text


def getPre():
    pre = ""
    for i in range(0, 3):
        pre += chr(random.randint(65, 90))
    return pre
def getConfusionText(dir):
    textArr = []
    names,funcs = scanningdir(dir)
    namePre = getPre()
    funcsPre = getPre()
    for i in range(0,len(names)):
        text = names[i].replace(confusionPre,namePre)
        text += randomWord(classSuffixWordNum)
        text = "#define %s \t %s\n"%(names[i],text)
        textArr.append(text)
    textArr.append("\n\n")
    for i in range(0, len(funcs)):
        text = funcs[i].replace(confusionPre, funcsPre)
        text += randomWord(funcSuffixWordNum)
        text = "#define %s \t %s\n" % (funcs[i],text)
        textArr.append(text)

    text = ""
    for i in textArr:
        text += i
    return text

def writeText(filePath, text):
    dir = os.path.dirname(filePath)
    if os.path.exists(dir) == False:
        os.makedirs(dir)
    with open(filePath, "w") as f:
        f.write(text)

def confusion():
    text = getConfusionText(confusionRootdir)
    writeText(confusionPath,text)

# 单词数组，混淆的单词，从这里选
wordArr = [
            "the", "be", "of", "and", "a",
            "to", "in", "on", "for", "have",
            "it", "that", "with", "as", "not",
            "at", "do", "need", "one", "use",
            "all", "will", "off", "say", "make",
            "if", "no", "out", "go", "take",
            "come","get","set","any","work",
            "now", "may", "such", "give", "over",
            "begin", "part", "way", "back", "long",
            "feel","each","very","old","both"
           ]
# 类名的后缀，添加混淆单词数
classSuffixWordNum = 0
# 方法名的后缀，添加混淆单词数
funcSuffixWordNum = 2


# 带混淆文件目录
confusionRootdir = "/Users/apple/jp/shop/shop/shop"
# 生产的混淆文件，将此文件加入pch中即可混淆
confusionPath = "/Users/apple/jp/shop/shop/shop/HSHXLB.h"
# 工程中类名／方法名的特殊前缀
confusionPre = "JPHX_"


if __name__ == '__main__':
    confusionFileName = confusionPath.split('/')[-1]
    confusion()
