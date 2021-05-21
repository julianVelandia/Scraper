# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import os
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError
import numpy as np
#import nltk

#nltk.download('stopwords')
#from nltk.corpus import stopwords

HOME_URL ='https://es.wikipedia.org/w/index.php?title=Especial:LoQueEnlazaAqu%C3%AD/Futbol&namespace=0&limit=100'


XPATH_LINK_TO_PAGE = '//ul[@id="mw-whatlinkshere-list"]/li//a/@href'
XPATH_LINK_TO_TITLE = '//h1[@id="section_0"]/text()'
XPATH_LINK_TO_ARTICLE = '//div[@class="mw-parser-output"]//p//text()'
stopwords = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos', 'habríais', 'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 'hubieran', 'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido', 'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea', 'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 'seremos', 'seréis', 'serán', 'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos', 'erais', 'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 'fuesen', 'sintiendo', 'sentido', 'sentida', 'sentidos', 'sentidas', 'siente', 'sentid', 'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos', 'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán', 'tendría', 'tendrías', 'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 'tenidos', 'tenidas', 'tened']


dictionary ={}

def complete_parser():
    response = requests.get(HOME_URL)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)
    links_to_pagina = parsed.xpath(XPATH_LINK_TO_PAGE)

    fname = 'out_file'
    touch(fname)
    fd = os.open(fname+'.txt', os.O_RDWR)

    for page in links_to_pagina:
        if 'w/index.php?title=Especial:' not in page:
            #print(page)
            save_txt(new_parser(page,35), fd)
        
         


def new_parser(key_word,words_limit):
    article =''
    num_words=0
    en_basura =False
    links_to_article = visit(define_url(key_word)).xpath(XPATH_LINK_TO_ARTICLE)#list pages
    
    for word in links_to_article:
        
        if '(' in word:
            en_basura=True
        
        if not en_basura and '\u200b' not in word and '[' not in word and ']' not in word:
            
            #article.append(word)
            article += word.replace(';','').replace(',',' , ').replace('.','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')

        if ')' in word:
            en_basura=False

        if '.' in word:
            break

        if words_limit<num_words:
            break
        num_words+=1

    filtered_article = []
    filtered_article = [word for word in article.split(' ') if word not in stopwords]

    #return('"'+ str(filtered_article)+':'+ str(article)+'"')
    #return "".join(article)
    fart = " ".join(filtered_article).replace('  ','').replace('\n','').replace('"','')
    art = "".join(article).replace('\n','').replace('"','').replace('  ','')
    #return('"' + art + '":"' + fart+'", ')
    print('"' + art + '":"' + fart+'", ')


def visit(url):
    response = requests.get(url)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)

    return parsed

def save_txt(text,fd):

    """Create the file to save the information"""

    if text:
        text = str.encode(text.replace('\n',' ').replace('\r', ''))
        out = os.write(fd,text)#
    else:
        print("Empty article")


def touch(fname):
    """Create the file to save the information"""
    fname = fname +'.txt'
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()

def define_url(key_word):
        
    #Replace special characters
    key_word=key_word.replace('%C3%A1','a').replace('%C3%A9','e').replace('%C3%AD','i').replace('%C3%B3','o').replace('%C3%BA','u').replace(' ','_')

    HOME_URL= 'https://es.m.wikipedia.org/'+key_word
    return HOME_URL

if __name__ == "__main__":
    #complete_parser()
    new_parser('wiki/Música',35)

