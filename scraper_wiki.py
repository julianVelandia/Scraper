# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import os

HOME_URL ='https://es.wikipedia.org/w/index.php?title=Especial%3ALoQueEnlazaAqu%C3%AD&limit=500&target=Ingenier%C3%ADa+mecatr%C3%B3nica&namespace='

XPATH_LINK_TO_PAGINA = '//ul[@id="mw-whatlinkshere-list"]/li//a/@href'
XPATH_LINK_TO_TITULO = '//h1[@id="section_0"]/text()'
XPATH_LINK_TO_DEFINICION = '//div[@class="mw-parser-output"]//p//text()'



def parse_home():
      
    #fd = os.open('ejemplo_3.txt', os.O_RDWR)

    response = requests.get(HOME_URL)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)
    links_to_pagina = parsed.xpath(XPATH_LINK_TO_PAGINA)
    
    
    for pagina in links_to_pagina:
        
        print('https://es.m.wikipedia.org/'+pagina)
        break

        response = requests.get('https://es.m.wikipedia.org/'+pagina)
        home = response.content.decode('utf-8')
        parsed = html.fromstring(home)

        
        links_to_titulo = parsed.xpath(XPATH_LINK_TO_TITULO)[0]
        links_to_definicion = parsed.xpath(XPATH_LINK_TO_DEFINICION)
        
        #print(len(links_to_definicion))

        
        

        linedef = str.encode('" -wiki- ') 
        numBytes = os.write(fd,linedef)#

        lineaux = links_to_titulo.replace('\n',' ').replace('\r', '')
        lineaux.rstrip('\n')
        linedefinicion = str.encode(lineaux)
        n= links_to_titulo.count(' ')+1
        nString = str(n) 
        nString2 = str.encode(nString)
        linenum = str.encode(' -num ') 
        numBytes = os.write(fd,linenum)#
        numBytes = os.write(fd,nString2)#
        linecierrenum = str.encode('- ') 
        numBytes = os.write(fd,linecierrenum)#
        numBytes = os.write(fd,linedefinicion)#
        lineadospuntos = str.encode(' ":" ')
        numBytes = os.write(fd,lineadospuntos)#
        n2=0
        for t in links_to_definicion:

            
            lineaux4 = t.replace('\n',' ').replace('\r', '').replace(':',' ').replace('...',' ')
            lineaux3 = lineaux4.replace('"',' ')
            lineaux3.rstrip('\n')
            lineaux3 = bytes(lineaux3, 'utf-8').decode('utf-8', 'ignore')
            lineadescripcion = str.encode(lineaux3)
            numBytes = os.write(fd,lineadescripcion)# 
            n2 = t.count(' ')+n2
            if n2>320:
                break

            
        n2String = str(n2) 
        n2String2 = str.encode(n2String)
        numBytes = os.write(fd,linenum)#
        numBytes = os.write(fd,n2String2)#
        numBytes = os.write(fd,linecierrenum)#
        
        lineacierretotal = str.encode('",')
        numBytes = os.write(fd,lineacierretotal)#
            
  
def run():
    parse_home()

if __name__ == '__main__':
    run()
