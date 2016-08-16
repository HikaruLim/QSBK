# -*- coding:utf-8 -*-

import urllib.request
import re


class QSBK:
    '''
            糗事百科爬虫类
    '''
    def __init__(self):
        self.pageIndex = 2  #第一页的这个值是空，所以不用它
        self.user_agent = "Mozilla/4.0(compatible; MSIE 5.5; Windows NT)"
        #初始化headers
        self.headers = {'User-Agent':self.user_agent}
        #存放每一页的笑话
        self.jokes = []
        #程序是否继续运行
        self.enable = False
        #count
        self.count = 1
        
    def getPage(self,pageIndex):
        url = 'http://www.qiushibaike.com/text/page/'+str(pageIndex)+'/?s=4901285'
        request = urllib.request.Request(url,headers = self.headers)
        response = urllib.request.urlopen(request)
        pageContent = response.read().decode('UTF-8')
        return pageContent
    
    def getPageItem(self,pageIndex):
        '''
                        同时读取每一页中的所有笑话
        '''
        pageContent = self.getPage(pageIndex)
        if not pageContent:
            print("page load failed...")
            return None
        
        pattern = re.compile(r'<div class="content">\n\n(.*?)</div>',re.S)
        jokes = re.findall(pattern, pageContent)
        
        pageJokes = []
        for item in jokes:
            replaceBR = re.compile("<br/>")
            item = re.sub(replaceBR, "\n", item)
            pageJokes.append(item)
        
        return pageJokes
    
    
    def loadPage(self):
        if self.enable == True:   
            if len(self.jokes) < 1:
                pageJokes = self.getPageItem(self.pageIndex)
                if pageJokes:
                    self.jokes.append(pageJokes)
                    self.count = 1
                    self.pageIndex += 1
                    
    
    def getOneJoke(self,pageJokes,page):
        '''
        for joke in pageJokes:
            self.loadPage()
            ifLoad = input()
            if ifLoad == "Q":
                self.enable = False
                return
            print("<第【%d】页\t第【%d】条>\n%s" % (page,self.count,joke))
            self.count += 1
        '''
        self.loadPage()
        ifLoad = input()
        if ifLoad == "Q":
            self.enable = False
            return
        print("<第【%d】页\t第【%d】条>\n%s" % (page,self.count,pageJokes))
        self.count += 1    
            
            
    def start(self):
        print("正在读取，按回车查看新笑话，Q退出\n")
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.jokes) > 0:
                pageJokes = self.jokes[0]
                #print("jokes =>>>>>> %s\n" % self.jokes)
                #print("jokes[0] =>>>>> %s\n" % self.jokes[0])
                nowPage += 1
                del self.jokes[0]
                self.getOneJoke(pageJokes, nowPage)
                
                

spider = QSBK()
spider.start()
    
    
    
    