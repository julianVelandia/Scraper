# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import os

HOME_URL ='http://diccionariofacil.org/diccionario/'

XPATH_LINK_TO_LETRA = '//div[@id="listadoLetras"]//li/a/@href'
XPATH_LINK_TO_PAGINA_LETRA_0 = 'http://diccionariofacil.org/diccionario/' #LETRA EN MAYUSCULAS
XPATH_LINK_TO_PAGINA_LETRA_1 =  '.html?p=' #NUMERO DE LA PAGINA
XPATH_LINK_TO_TITULO = '//div[@id="elListadoPalabras"]/div/div/h4/text()'
XPATH_LINK_TO_DEFINICION = '//div[@id="elListadoPalabras"]/div/div/div/p/text()'

def parse_home():
    letras = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N'
    ,'Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    p=1
 
    fd = os.open('definiciones.txt', os.O_RDWR)

    for l in letras:
        p=1
        for i in range(39):
            
            pString = str(p) 
            p=p+1
            try:
                response = requests.get(XPATH_LINK_TO_PAGINA_LETRA_0 + l + XPATH_LINK_TO_PAGINA_LETRA_1 + pString)
                home = response.content.decode('utf-8')
                parsed = html.fromstring(home)
            except:
                print('error, p: '+pString+' l: '+l+'error')
            
            links_to_titulo = parsed.xpath(XPATH_LINK_TO_TITULO)
            links_to_definicion = parsed.xpath(XPATH_LINK_TO_DEFINICION)
            
            j=0
            '''
            n= links_to_titulo[0].count(' ')+1
            nString = str(n)
            print('p: '+links_to_titulo[0]+' n: '+nString)
            '''
            
            
            for t in links_to_titulo:

                linedef = str.encode('"') 
                numBytes = os.write(fd,linedef)#
                lineaux = t
                lineaux.rstrip('\n')
                linedefinicion = str.encode(lineaux)
                #n= t.count(' ')+1
                #nString = str(n) 
                #nString2 = str.encode(nString)
                #linenum = str.encode(' -num ') 
                #numBytes = os.write(fd,linenum)#
                #numBytes = os.write(fd,nString2)#
                #linecierrenum = str.encode('- ') 
                #numBytes = os.write(fd,linecierrenum)#
                numBytes = os.write(fd,linedefinicion)#
                lineadospuntos = str.encode(' ":" ')
                numBytes = os.write(fd,lineadospuntos)#
                
                lineaux3 = links_to_definicion[j].replace('\n',' ').replace('\r', '').replace('...','')
                lineaux3.rstrip('\n')
                lineadescripcion = str.encode(lineaux3)
                #n2= links_to_definicion[j].count(' ')+1
                #n2String = str(n2) 
                #n2String2 = str.encode(n2String)
                #numBytes = os.write(fd,linenum)#
                #numBytes = os.write(fd,n2String2)#
                #numBytes = os.write(fd,linecierrenum)#
                numBytes = os.write(fd,lineadescripcion)#
                lineacierretotal = str.encode('",')
                numBytes = os.write(fd,lineacierretotal)#
                j=j+1
                
            
            
def run():
    parse_home()

if __name__ == '__main__':
    run()
