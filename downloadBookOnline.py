import codecs
import re
import requests
import urllib2

class OnlineBook:
    def __init__(self, filename):
        self.filename = filename
        self.fileArray = self.fileToArray()
        self.fileString = self.fileToString()
        self.pageCount = self.getPageCount()
        self.checkLinks = self.checkLinkCount()

        if (self.checkLinks):
            self.pageLinks = self.getPageLinks()
            self.realLinks = self.getRealLinks()
            self.savePdfImages()

    '''Add file contents to array'''
    def fileToArray(self):
        self.fileArray = []
        file = codecs.open(self.filename, "r", "utf-8")
        array = []
        for line in file:
            array.append(line)
        file.close()

        return array

    '''Add file contents to string'''
    def fileToString(self):
        self.fileString = ""
        file = codecs.open(self.filename, "r", "utf-8")
        string = ""
        for line in file:
            string += line
        file.close()

        return string

    '''Get page count'''
    def getPageCount(self):
        string = '"page_count":'
        pageCountIndex = self.fileString.index(string)
        return int(self.fileString[pageCountIndex+len(string):pageCountIndex+len(string)+3])


    '''Check if number of pages equals number of links'''
    def checkLinkCount(self):
        if (self.pageCount == self.fileString.count("pageParams.contentUrl")):
            print("Page count is the same as number of links.")
        else:
            self.pageCount = self.fileString.count("pageParams.contentUrl")

        return True

    '''Get page links listed in source code using regular expressions'''
    def getPageLinks(self):
        numOfPages = self.pageCount
        prevIndex = 0
        searchString = "pageParams.contentUrl"
        links = []
        while (numOfPages > 0):
            nextIndex = self.fileString.index(searchString, prevIndex+1)
            m = re.search('(\".+?\")', self.fileString[nextIndex:])
            links.append(m.group(0).strip('"'))
            prevIndex = nextIndex
            numOfPages -= 1
        return links

    '''get real pdf image download links by looking at orig attribute in url content'''
    def getRealLinks(self):
        realLinks = []
        for links in self.pageLinks:
            headers = {
                'cache-control': "no-cache",
                'postman-token': "8af4828e-133e-5c8f-e4bd-10ac70d6048a"
            }

            try:
                response = requests.request("GET", links, headers=headers)
            except:
                response = requests.request("GET", links, headers=headers)

            m = re.search('(orig=.+?"http.+?")', response.text)

            try:
                cleanUrl = m.group(0)[m.group(0).index("http"):]
                cleanUrl = cleanUrl[:cleanUrl.rindex("\\")]
            except ValueError as e:
                print(response.text)
                print(e)

            realLinks.append(cleanUrl)

        return realLinks

    '''save pdf images in images folder'''
    def savePdfImages(self):
        index = 1
        for links in self.realLinks:
            resource = urllib2.urlopen(links)
            output = open("images/page{0:04d}.jpg".format(index),"wb")
            output.write(resource.read())
            output.close()
            index += 1
        print("Saved Images")

pdf = OnlineBook("book.html")
print ("Finished!")
