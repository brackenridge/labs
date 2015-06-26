#!/usr/bin/python

from HTMLParser import HTMLParser
import urllib

class BasicLinkData:
    def __init__(self, text, ref):
        self.text = text
        self.ref = ref

class BasicDVCData:
    def __init__(self, id, resort, points, desc, price):
        self.id = id
        self.resort = resort
        self.description = desc
        self.price = price
        self.points = points

class LinksParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording=0
        self.data = []
        self.currData = None
        self.currRef = None
        
    def handle_starttag(self, tag, attributes):
        if tag != 'a':
            return
        self.recording = 1
        for name, value in attributes:
            if name == 'href':
                self.currRef = value

    def handle_endtag(self,tag):
        if tag != 'a' and self.recording:
            return
        self.data.append(BasicLinkData(self.currData,self.currRef))
        self.recording = 0

    def handle_data(self, data):
        if self.recording:
            self.currData = data


class DVCTableParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rec_table = 0
        self.rec_row = 0
        self.rec_col = 0
        self.found_dvc_header = False
        self.data = []
        self.curr_data = []
        self.temp_row = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.rec_table += 1
        elif tag == 'tr':
            self.rec_row += 1
        elif tag == 'td':
            self.rec_col += 1
            self.curr_data = []

    def handle_data(self, data):
        if self.rec_col and data.rstrip():
            self.curr_data.append(data)

    def handle_entityref(self, name):
        if self.rec_col:
            self.handle_data(self.unescape("&%s" % name))

    def handle_endtag(self, tag):
        if tag == 'tr' and self.rec_row and self.rec_table:
            self.rec_row -= 1
            if self.found_dvc_header and len(self.temp_row) > 6:
                if self.temp_row[0] != 'ID #':
                    self.data.append(BasicDVCData(self.temp_row[0],self.temp_row[1],self.temp_row[2],self.temp_row[5],self.temp_row[6]))
                    self.temp_row = []
                    return
            for x in ['ID #', 'RESORT', 'POINTS']:
                if x not in self.temp_row:
                    self.temp_row = []
                    return # not the dvc table
            self.found_dvc_header = True
            self.temp_row = []
        elif tag == 'td' and self.rec_col and self.rec_table and self.rec_row:
            self.rec_col -= 1
            self.temp_row.append(''.join(self.curr_data))
            self.curr_data = []
        elif tag == 'table' and self.rec_table:
            self.rec_table -= 1
            self.found_dvc_header = False # just always set to false
            
if __name__ == '__main__':

    dvc = "http://www.resalesdvc.com"
    sitemap = dvc + "/SiteMap.html"
    smParser = LinksParser()
    smParser.feed(urllib.urlopen(sitemap).read())
    matches = [x for x in smParser.data if x.text == 'Buy DVC Timeshare']
    if matches:
        url = dvc + matches[0].ref
        dvcParser = DVCTableParser()
        dvcParser.feed(urllib.urlopen(url).read())
        for x in dvcParser.data:
            if x.price != 'Sale pending':
                print x.resort, x.points, x.price
