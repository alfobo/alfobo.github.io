#!/bin/python3
import os, re, time, argparse

parser = argparse.ArgumentParser(prog='md2html', usage='%(prog)s [path]')
parser.add_argument('mdDir', type=str)

pathList:list = []
oList:list = []
uList:list = []
lType:int = 0

def getContentDir():
    for dir in os.scandir(pathList[0]):
        if (os.path.isdir(dir)):
            pathList.append(dir.path+'/')

def findMD(path):
    nuPath:str= ""
    for file in os.scandir(path):
        if re.search(".md$",file.name):
            nuPath = path + str(file.name)
            md2HTML(nuPath)

def headers(line):
    word = line.split()
    if len(word) == 0:
        return line
    if word[0] == "#":
        word[0] = '<h1>'
        word.append('</h1>')
    elif word[0] == "##":
        word[0] = '<h2>'
        word.append('</h2>')
    elif word[0] == "###":
        word[0] = '<h3>'
        word.append('</h3>')
    elif word[0] == "####":
        word[0] = '<h4>'
        word.append('</h4>')
    elif word[0] == "#####":
        word[0] = '<h5>'
        word.append('</h5>')
    elif word[0] == "######":
        word[0] = '<h6>'
        word.append('</h6>')
    else:
        return line

    line=" ".join(word)
    return line

def mediaClass(line):
    word = line.split()

    if (re.search(r'^\<img',line) or
        re.search(r'^\<iframe',line)):
        word.insert(0,"<div class=media>")
        word.append("</div>")
    elif re.search(r'^\<video',line):
        word.insert(0,"<div class=media>")
    elif re.search('/video>$',line):
        word.append("</div>")
    line=" ".join(word)
    return line

def para(line):
    # if (re.search('^<h',line) or
    #     re.search('^<div',line) or
    #     re.search('^<video',line) or
    #     re.search('^<source',line) or
    #     re.search('/video>$',line)):
    if(re.search('^<',line)):
        return line

    word = line.split()
    word.insert(0,'<p>')
    word.append('</p>')

    line=" ".join(word)
    return line

def font(line):
    word = line.split()
    i = 0
    for e in word:
        if (re.search(r'^\*\*\*',e) or
              re.search(r'\*\*\*$',e) or
              re.search(r'\*\*\*.$',e)):
            e = bold(e)
            e = italic(e)
        elif (re.search(r'^\*\*',e) or
              re.search(r'\*\*$',e) or
              re.search(r'\*\*.$',e)):
            e =bold(e)
        elif (re.search(r'^\*',e) or
              re.search(r'\*$',e) or
              re.search(r'\*.$',e)):
            e =italic(e)
        word[i] = e
        i+=1

    line=" ".join(word)
    return line

def bold(word):
    tag:str = word
    tag = re.sub(r'^\*\*','<b>',tag)
    tag = re.sub(r'\*\*$','</b>',tag)
    tag = re.sub(r'\*\*.$','</b>.',tag)

    return tag

def italic(word):
    tag:str = word
    if re.search('^<b>',tag):
        tag = re.sub(r'\*','<i>',tag,count=1)
        tag = re.sub(r'\*','</i>',tag,count=1)
    else:
        tag = re.sub(r'^\*','<i>',tag)
        tag = re.sub(r'\*$','</i>',tag)
        tag = re.sub(r'\*.$','</i>.',tag)
    return tag

def thematicBreak(line):
    word = line.split()
    if len(word) == 0:
        return line
    if word[0]=="---":
        word[0] = '<hr>'

    line=" ".join(word)
    return line

def lists(line):
    global lType
    if re.search('^-',line):
        lType = 1
        line = line.split()
        del(line[0])
        line = " ".join(line)
        unorderedList(line)
    elif re.search(r'^\d{1,4}\.',line):
        lType = 2
        line = line.split()
        del(line[0])
        line = " ".join(line)
        orderedList(line)
    elif uList != [] or oList != []:
        if lType == 1:
            lType = 0
            return unorderedList()
        elif lType == 2:
            lType = 0
            return orderedList()
    return line

def unorderedList(item=""):
    if item == "":
        htmlList = ['<ul>']
        for e in uList:
            htmlList.append('<li>')
            htmlList.append(e)
            htmlList.append('</li>')
        htmlList.append('</ul>')
        htmlList = " ".join(htmlList)
        uList.clear()
        return htmlList
    else:
        uList.append(item)

def orderedList(item=""):
    if item == "":
        htmlList = ['<ol>']
        for e in oList:
            htmlList.append('<li>')
            htmlList.append(e)
            htmlList.append('</li>')
        htmlList.append('</ol>')
        htmlList = " ".join(htmlList)
        oList.clear()
        return htmlList
    else:
        oList.append(item)

def hyperlink(line):
    temp = []
    word = line.split()

    if re.search(r'\[.*?\]\(.*?\)',line):
        # Joins text in hyperlink if there's space in the text
        i = 0
        while(i<len(word)-1):
            if re.search(r'^\[',word[i]) and not re.search(r'\]\(.*?\)',word[i]):
                temp.append(word[i])
                j=i+1
                while(j<len(word)):
                    if re.search(r'\]\(.*?\)',word[j]):
                        temp.append(word[j])
                        word.pop(j)
                        word[i] = " ".join(temp)
                        temp.clear()
                        i=j
                        break
                    else:
                        temp.append(word[j])
                    j+=1
            i+=1
        # Converts md hyperlinks to html hyperlinks
        i=0
        while(i<len(word)):
            if re.search(r'\[.*?\]\(.*?\)',word[i]):
                temp = re.split(r'\]\(',word[i])
                temp.reverse()
                temp.insert(0,'<a href="')
                temp[1] = re.sub(r'\)','">',temp[1])
                temp[2] = re.sub(r'\[',"",temp[2])
                temp.append("</a>")
                word[i] = "".join(temp)
                temp.clear()
            i+=1
        line=" ".join(word)
    return line

def md2HTML(path):
    file=open(path,'r')
    buf:str=file.readlines()
    file.close()

    buf.insert(0,'<!doctype html>\n<html id="doc">\n<head>\n<meta charset="utf-8">\n' +
                  '<link rel="stylesheet" href="../../../style.css">\n</head>\n<body>\n')
    i=0
    while(i<len(buf)):
        if buf[i] == '\n':
            i+=1
            continue
        buf[i] = headers(buf[i].strip())
        buf[i] = thematicBreak(buf[i])
        buf[i] = mediaClass(buf[i])
        buf[i] = lists(buf[i])
        if oList != []:
            del buf[i]
            if i == len(buf)-1:
                buf.append("")
            if not re.search(r'^\d{1,4}\.',buf[i+1]):
                buf[i] = lists(buf[i])
            continue
        if uList != []:
            del buf[i]
            if i == len(buf)-1:
                buf.append("")
            if not re.search('^-',buf[i+1]):
                buf[i] = lists(buf[i])
            continue
        buf[i] = para(buf[i])
        buf[i] = font(buf[i])
        buf[i] = hyperlink(buf[i])
        i+=1
    buf.append("\n</body>"+
    "\n</html>")

    content = "".join(buf)
    writePath = path.replace('.md','.html')
    file=open(writePath,'w')
    file.write(content)
    file.close()

def main(mdDir:str=""):
    startTime = time.time()
    if (os.path.isdir(mdDir)):
        global pathList
        pathList.append(mdDir)
        os.chdir(pathList[0])
        getContentDir()
        for dir in pathList:
            findMD(dir)
        endTime = time.time()
        execLength = endTime - startTime
    else:
        print("Invalid path")
    print("Conversion time: " + str(execLength) + " sec")

main(parser.parse_args().mdDir)
