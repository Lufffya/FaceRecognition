#
# 一个爬虫项目
#

import requests
import re
import os
#from pypinyin import pinyin, lazy_pinyin

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("")

def getPageUrls(text,name):
    re_pageUrl=r'href="(.+)">\s*<img src="(.+)" alt="'+name
    #re_pageUrl=r'href="(.+)">\s*<img src="(.+)"'
    return re.findall(re_pageUrl,text)

def downPictures(text,root,name,L):
    pageUrls=getPageUrls(text,name)
    titles=re.findall(r'alt="'+name+r'(.+)" ',text)
    for i in range(len(pageUrls)):
        pageUrl=pageUrls[i][0]
        path = root
        if not os.path.exists(path):
            os.mkdir(path)
        if pageUrl.find("http://www.win4000.com") < 0:
            continue
        #if not os.listdir(path):
        #pageUrl = pageUrl.split()[0].split("\"")[0]

        print(pageUrl)

        pageText=getHTMLText(pageUrl)
        totalPics=int(re.findall(r'<em>(.+)</em>）',pageText)[0])
        downUrl=re.findall(r'href="(.+?)" class="">',pageText)


        cnt=1;
        while(cnt<=totalPics):
            L += 1
            picPath=path+"%s.jpg"%str(L)
            r=requests.get(downUrl)
            with open(picPath,'wb') as f:
                f.write(r.content)
                f.close()
            print('{} - 第{}张下载已完成\n'.format(titles[i],L))
            cnt+=1
            nextPageUrl=re.findall(r'href="(.+?)">下一张',pageText)[0]
            pageText=getHTMLText(nextPageUrl)
            downUrl=re.findall(r'href="(.+?)" class="">下载图片',pageText)[0]
    return L

def main():
    name=input("请输入你喜欢的明星的名字:")
    nameUrl="http://www.win4000.com/mt/"+''.join("liuyifei")+".html"
    #nameUrl = "http://www.win4000.com/zt/ziranfengguang.html"
    L  = 0
    try:
        text=getHTMLText(nameUrl)
        if not re.findall(r'暂无(.+)!',text):
            root = "DataSet/pachong/"+name+"//"
            if not os.path.exists(root):
                os.mkdir(root)
            L = downPictures(text,root,name, L)
            try:
                nextPage=re.findall(r'next" href="(.+)"',text)[0]
                while(nextPage):
                    nextText=getHTMLText(nextPage)
                    L = downPictures(nextText,root,name,L)
                    nextPage=re.findall(r'next" href="(.+)"',nextText)[0]
            except IndexError:
                print("已全部下载完毕")
    except TypeError:
        print("不好意思，没有{}的照片".format(name))
    return

if __name__ == '__main__':
    main()
