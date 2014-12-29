#!/usr/bin/env python
# -*- coding: utf_8 -*-
from googlegeocoder import GoogleGeocoder
from bs4 import BeautifulSoup
import urllib2
import re

class urlOpener:
    """class to open any website and parse it"""
    def urlopen(self,url):
        """c"""
        data = urllib2.urlopen(url).read() #opening the website and reading the contents.
        soap=BeautifulSoup(data) # using Beautifulsoup to prettify the contents and make them readable.
        return soap


class URL(urlOpener):
    """class to inherite urlOpener objects and implement it here"""
    def __init__(self):
        self.listo=['topCategory3518','topCategory3517','topCategory39','topCategory7','topCategory4595','topCategory88854','topCategory9','topCategory3520']# categories in the website
        self.categories=[] #type of category the user needs to get data with 
        self.categoriesTitle=[]
        self.dicta={}
        self.ContentsLink=[]
        self.items=[]
        self.places=[]
        self.final_places=[]
        self.final={}

    def openURL(self):
        geocoder= GoogleGeocoder()
        opena=urlOpener()
        soap= opena.urlopen('http://www.sahibinden.com/')

        for number in self.listo:
            productDivs = soap.findAll('li', attrs={'class' : '%s' %number})
            for div in productDivs:
                self.categories.append("http://www.sahibinden.com/"+div.find('a')['href'])
                self.categoriesTitle.append(div.find('a')['title'])
        count=0
        dicta={}
        for i in range(len(self.categoriesTitle)):
            category,link=(self.categoriesTitle[i],self.categories[i])
            count+=1
            dicta.setdefault(count,{})
            dicta[count][category]=link
            print count,category
        choice=raw_input("pick a number for the category above except 6 & 7 & 8:\n")
        choice=int(choice)

        dictafinal={i:dicta[i] for i in dicta if i!=6 and 7 and 8}#element 6 is deleted because is not a category


        for num in dictafinal:
            if choice == 6 or choice == 7 or choice == 8:
                print "There are no contents detected"
            else:
                for li in dictafinal[num].values():
                    if choice == num:
                        try:
                            website=urllib2.urlopen(li).read()
                            bs=BeautifulSoup(website)
                            bss=bs.find_all('div',attrs={'class':'uiInlineBoxTitle'})
                            self.ContentsLink.append("http://www.sahibinden.com/"+bss[1].find('a')['href'])
                        except:
                            self.ContentsLink.append("http://www.sahibinden.com/"+bss[2].find('a')['href'])

        for page in self.ContentsLink:
            soap2=opena.urlopen(page)
            g_data=soap2.findAll("table",{"id":"searchResultsGallery"})
            for item in g_data:
                for i in range(1,len(item.contents),2):
                    h=item.contents[i].find_all("div",{"class":"searchResultsGallerySubContent"})
                    for item2 in h:
                        p= item2.contents[3].text
                        self.places.append(p)
                    for j in range(20):
                        try:
                            itema=item.contents[i].find_all("a",{"class":"classifiedTitle"})[j].text #this code gets the items on all the page only
                            self.items.append(itema)
                        except:
                            pass

        for place,it in zip(self.places,self.items):
            k=place.split(" ")[-1]+' '+place.split(" ")[-3]
            self.final_places.append(k)
        for ii in range(len(self.final_places)):
            dots= geocoder.get('%s' %self.final_places[ii].encode("utf-8"))[0].geometry.location
            print self.items[ii],dots
'''
            output=open("index.html","w")
            output.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'+'\n')
            output.write('<html lang="en">'+'\n')
            output.write('<head>'+'\n')
            output.write('<meta http-equiv="content-type" content="text/html; charset=utf-8">'+'\n')
            output.write('<title>Director v1.0</title>'+'\n')
            output.write('</head>'+'\n')
            output.write('<body>'+'\n')
            output.write('<center><iframe width="600" height="450" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/place?q='+dots+'&key=..."></iframe>'+'\n')
            output.write('</body>'+'\n')
            output.write('</html>'+'\n')

'''




if __name__ == '__main__':
    c= URL()
    c.openURL()

