# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import os

HOME_URL ='http://famma.org/diccionario-tecnico'

XPATH_LINK_TO_LETRA = '//div[@class="glossaryalphabet seopagination"]/ul/li/a/@href'

XPATH_LINK_TO_TITULO = '//table[@id="glossarylist"]/tbody/tr/td/a/text()'
XPATH_LINK_TO_DEFINICION = '//table[@id="glossarylist"]/tbody/tr/td/div/text()[1]'

def parse_home():

    fd = os.open('ejemplo_2.txt', os.O_RDWR)
    response = requests.get(HOME_URL)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)

    links_to_pagina = parsed.xpath(XPATH_LINK_TO_LETRA)
   
    
    for letra in links_to_pagina:
        
        response = requests.get('http://famma.org/'+letra)
        home = response.content.decode('utf-8')
        parsed = html.fromstring(home)

        links_to_titulo = parsed.xpath(XPATH_LINK_TO_TITULO)
        links_to_definicion = parsed.xpath(XPATH_LINK_TO_DEFINICION)

        j=0
        
        for t in links_to_titulo:
            if len(links_to_definicion[j].replace(' ','')) > 7:
                linedef = str.encode('" -def- -tec- ') 
                numBytes = os.write(fd,linedef)#
                lineaux = t
                lineaux.rstrip('\n')
                linedefinicion = str.encode(lineaux)
                n= t.count(' ')
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
                
                lineaux3 = links_to_definicion[j].replace('\n',' ').replace('\r', '').replace('...','').replace('	','')
                lineaux3.rstrip('\n')
                lineadescripcion = str.encode(lineaux3)
                n2= links_to_definicion[j].count(' ')
                n2String = str(n2) 
                n2String2 = str.encode(n2String)
                numBytes = os.write(fd,linenum)#
                numBytes = os.write(fd,n2String2)#
                numBytes = os.write(fd,linecierrenum)#
                numBytes = os.write(fd,lineadescripcion)#
                lineacierretotal = str.encode('",')
                numBytes = os.write(fd,lineacierretotal)#
                j=j+1
                
       
            
def run():
    parse_home()

if __name__ == '__main__':
    run()
