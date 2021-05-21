# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import os

HOME_URL ='https://definicion.de/'

XPATH_LINK_TO_LETRA = '//nav[@id="main-nav"]//ul//li//a//@href'
XPATH_LINK_TO_PALABRA = '//section[@id="content"]//@href'
XPATH_LINK_TO_TITULO = '//article[@id="definicion-post-box"]/h2[@class="title-definicion"]/a/strong/text()'
XPATH_LINK_TO_DEFINICION = '//article[@id="definicion-post-box"]/div[@class="post-entry"]//p//text()'



def parse_home():
      
    fd = os.open('definiciones.txt', os.O_RDWR)

    response = requests.get(HOME_URL)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)
    links_to_letras = parsed.xpath(XPATH_LINK_TO_LETRA)
    p=0
    pp=0
    
    for letra in links_to_letras:

        response = requests.get(letra)
        home = response.content.decode('utf-8')
        parsed = html.fromstring(home)
        links_to_palabras = parsed.xpath(XPATH_LINK_TO_PALABRA)

        for palabra in links_to_palabras:
            p=p+1
            if p>1000:
                p=0
                break
            response = requests.get(palabra)
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_titulo = parsed.xpath(XPATH_LINK_TO_TITULO)[0]
            links_to_definicion = parsed.xpath(XPATH_LINK_TO_DEFINICION)

            lineaux = links_to_titulo.replace('\n',' ').replace('\r', '')
            lineaux.rstrip('\n')
            linetitulo = str.encode(lineaux)
            
            linedef = str.encode('"') 
            lineadospuntos = str.encode(' ":" ')
            
            numBytes = os.write(fd,linedef)#
            numBytes = os.write(fd,linetitulo)#
            numBytes = os.write(fd,lineadospuntos)#
            
            for t in links_to_definicion:
                pp=pp+1
                if pp>100:
                    pp=0
                    break
                lineaux4 = t.replace('\n',' ').replace('\r', '').replace(':',' ').replace('...',' ')
                lineaux3 = lineaux4.replace('"',' ')
                lineaux3.rstrip('\n')
                lineaux3 = bytes(lineaux3, 'utf-8').decode('utf-8', 'ignore')
                lineadescripcion = str.encode(lineaux3)
                numBytes = os.write(fd,lineadescripcion)# 
                
            lineacierretotal = str.encode('",')
            numBytes = os.write(fd,lineacierretotal)#
                
            
def run():
    parse_home()

if __name__ == '__main__':
    run()
