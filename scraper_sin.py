# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import os

#HOME_URL ='https://www.sinonimosonline.com/sinonimos-populares/'

XPATH_LINK_TO_PAGINA = 'https://www.sinonimosonline.com/sinonimos-populares/'#num'/'
XPATH_LINK_TO_PALABRA = '//ul[@id="sinonimos-populares"]/li/a/@href'

XPATH_LINK_TO_DIV = '//div[@class="wrapper-box p20"]/div[@class="synonim"]'

XPATH_LINK_TO_TITULO = '//p[@class="total"]/strong[2]/text()'
XPATH_LINK_TO_SINONIMOS = '//div[@class="wrapper-box p20"]/div[@class="synonim"]/p[@class="sinonimos"]/a/text()'



def parse_home():
      
    fd = os.open('sinonimos4.txt', os.O_RDWR)

    

    #links_to_pagina = parsed.xpath(XPATH_LINK_TO_PAGINA)
    
    
    for pagina in range(19):
        

        
        response = requests.get(XPATH_LINK_TO_PAGINA + str(pagina)+'/')
        home = response.content.decode('utf-8')
        parsed = html.fromstring(home)

        
        links_to_palabras = parsed.xpath(XPATH_LINK_TO_PALABRA)
        
        
        for palabra in links_to_palabras:
            try:
                response = requests.get('https://www.sinonimosonline.com/'+palabra)
                home = response.content.decode('utf-8')
                parsed = html.fromstring(home)

                titulo = parsed.xpath(XPATH_LINK_TO_TITULO)[0]
                sinonimosList = parsed.xpath(XPATH_LINK_TO_SINONIMOS)[0]
                #divs = parsed.xpath(XPATH_LINK_TO_DIV)
                
                
                linedef = str.encode('"') 
                lineaux = titulo.replace('\n','').replace('\r','').strip()
                lineaux.rstrip('\n')
                linetitulo = str.encode(lineaux)
                lineadospuntos = str.encode('":"')
                lineaux4 = sinonimosList.replace('\n','').replace('\r','').replace(':','').replace('...','')
                lineaux3 = lineaux4.replace('"','').strip()
                lineaux3.rstrip('\n')
                lineaux3 = bytes(lineaux3, 'utf-8').decode('utf-8', 'ignore')
                lineadescripcion = str.encode(lineaux3)
                lineacierretotal = str.encode('",')



                numBytes = os.write(fd,linedef)#
                numBytes = os.write(fd,linetitulo)#
                numBytes = os.write(fd,lineadospuntos)#
                numBytes = os.write(fd,lineadescripcion)# 
                numBytes = os.write(fd,lineacierretotal)#

                '''for div in divs:
                    lineaux = titulo.replace('\n',' ').replace('\r', '')
                    linedef = str.encode('"') 
                    #linenum = str.encode(' -num ') 
                    #linecierrenum = str.encode('- ')
                    lineadospuntos = str.encode(' ":" ')
                    #for concat in sinonimosList:
                       
                    numBytes = os.write(fd,linedef)#
                    lineaux.rstrip('\n')
                    linetitulo = str.encode(lineaux)
                    numBytes = os.write(fd,linetitulo)#
                    numBytes = os.write(fd,lineadospuntos)#

                    lineaux4 = concat.replace('\n',' ').replace('\r', '').replace(':',' ').replace('...',' ')
                    lineaux3 = lineaux4.replace('"',' ')
                    lineaux3.rstrip('\n')
                    lineaux3 = bytes(lineaux3, 'utf-8').decode('utf-8', 'ignore')
                    lineadescripcion = str.encode(lineaux3)
                    numBytes = os.write(fd,lineadescripcion)# 
                    lineacierretotal = str.encode('",')
                    numBytes = os.write(fd,lineacierretotal)#
                '''
                
            except: 
                print('error, pag:'+str(pagina))
            


                

def run():
    parse_home()

if __name__ == '__main__':
    run()
