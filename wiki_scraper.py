# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import os
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError
import pickle
import numpy as np

XPATH_LINK_TO_PAGE = '//ul[@id="mw-whatlinkshere-list"]/li//a/@href'
XPATH_LINK_TO_TITLE = '//h1[@id="section_0"]/text()'
XPATH_LINK_TO_ARTICLE = '//div[@class="mw-parser-output"]//p//text()'

"""Scraper of wikipedia articles on keywords"""

dictionary ={}

def _new_parse():
    
    key_word = 'Colombia'
    page_limit=5
    words_limit=5
    fname = 'out_file'
    touch(fname)
    fd = os.open(fname+'.txt', os.O_RDWR)
    
    links_to_page = _visit(define_url(key_word)).xpath(XPATH_LINK_TO_PAGE)#list pages
    print (links_to_page)
    num_page=0
    for page in links_to_page:#visit each pages

        if page_limit<num_page:
            break
        
        title = _visit('https://es.m.wikipedia.org/'+page).xpath(XPATH_LINK_TO_TITLE)[0]#Save title
        links_to_article = _visit('https://es.m.wikipedia.org/'+page).xpath(XPATH_LINK_TO_ARTICLE)#Save content
        
        num_words=0
        article =[]
        for word in links_to_article:

            article.append(word+' ')
            
            
            if words_limit<num_words:
                break
            num_words+=1

        _save_txt(fname,title,article,fd)
        _save_dic(title,article)

       
        
def _visit(url):
    response = requests.get(url)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)

    return parsed


def _save_txt(fname, raw_title, raw_article,fd):

    """Create the file to save the information"""

    if raw_title and raw_article:
        
        marks = str.encode('"') 
        title = str.encode(raw_title.replace('\n',' ').replace('\r', ''))
        colons = str.encode('":"')
        article = "".join(raw_article)
        article = str.encode(article.replace('\n',' ').replace('\r', '').replace(':',' ').replace('...',' ').replace('"',' '))
        #article = bytes(article, 'utf-8').decode('utf-8', 'ignore')
        comma = str.encode(',')

        out = os.write(fd,marks)#
        out = os.write(fd,title)#
        out = os.write(fd,colons)#
        out = os.write(fd,article)#
        out = os.write(fd,marks)#
        out = os.write(fd,comma)#
    else:
        print("Empty article")


def _save_dic(title,article):
    global dictionary
    dictionary[title] = article


def _save_pickle():
    global dictionary
    data = list(dictionary.items())
    an_array = np.array(data)

    pickle_out = open("out_pickle.pkl","wb")
    pickle.dump(an_array, pickle_out)
    pickle_out.close()


def touch(fname):
    """Create the file to save the information"""
    fname = fname +'.txt'
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()


def define_url(key_word):
    
    #Replace special characters
    key_word=key_word.replace('%C3%A1','a').replace('%C3%A9','e').replace('%C3%AD','i').replace('%C3%B3','o').replace('%C3%BA','u')

    HOME_URL= 'https://es.wikipedia.org/w/index.php?title=Especial%3ALoQueEnlazaAqu%C3%AD&target='+key_word+'&namespace='
    return HOME_URL

  
def run():
    _new_parse()
    #is_pickle=input("Save as pickle file? \n yes:[y] \n no[n]")
    #if is_pickle == 'y':
    #   _save_pickle(dictionary)

if __name__ == '__main__':
    run()