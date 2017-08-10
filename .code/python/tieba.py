# -*- coding = 'utf-8' -*-
import urllib2
import re
import urllib

class Tieba():
    def __init__(self, baseUrl, seeLZ):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz' + str(seelz)

    def getPage(self, pageNum):
        try:
            url = self.baseUrl + self.seeLZ + '&pn'+ pageNum
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            print response.read()          
            return response
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "error", e.reason
                return None

    def getTitle(self, page):
        page = self.getPage()
        pattern = re.compile('<h3 class=core_title_txt.*?>(.*?)</h3>',re.S)
        result = re.findall(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def setFileTitle(self,title):
        #如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")

    def writeData(self,contents):
        #向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                #楼之间的分隔符
                floorLine = "\n" + str(self.floor) + u"-----------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL已失效，请重试"
            return
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        #出现写入异常
        except IOError,e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"

        

