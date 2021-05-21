# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import os
import random

def parse_home():
      
    fd = os.open('aritmetica.txt', os.O_RDWR)

    sim = ['+','-','*','/']
    n1 = 0
    for i in range(5000000):
        
        n1 = random.randrange(150)
        #print('n1: '+ str(n1))
        n2 = random.randrange(150)+1
        #print('n2: '+ str(n2))
        s = random.randrange(4)
        #print('s: '+str(s))
        if s == 0:
            n3 = n1+n2
        elif s == 1:
            n3 = n1-n2
        elif s == 2:
            n3 = n1*n2
        else:
            n3 = n1/n2
        #print('sol: '+ str(n1)+sim[s]+str(n2)+' : '+str(n3))
        linedef = str.encode('" ')
        lineop = str.encode(str(n1)+' '+sim[s]+' '+str(n2))
        lineadospuntos = str.encode(' ":" ')
        lineres = str.encode(str(n3))
        lineacierretotal = str.encode(' ",')

        numBytes = os.write(fd,linedef)
        numBytes = os.write(fd,lineres)###
        #numBytes = os.write(fd,lineop)
        numBytes = os.write(fd,lineadospuntos)
        #numBytes = os.write(fd,lineres)
        numBytes = os.write(fd,lineop)###
        numBytes = os.write(fd,lineacierretotal)#
    '''
     
    #linenum = str.encode(' -num ') 
    #linecierrenum = str.encode('- ')
    lineadospuntos = str.encode(' ":" ')
    for concat in sinonimosList:
        #n2=0
        #n=0
        numBytes = os.write(fd,linedef)#
        lineaux.rstrip('\n')
        linetitulo = str.encode(lineaux)
        #n= titulo.count(' ')+1
        #nString = str(n) 
        #nString2 = str.encode(nString)
        #numBytes = os.write(fd,linenum)#
        #numBytes = os.write(fd,nString2)#
        #numBytes = os.write(fd,linecierrenum)#
        numBytes = os.write(fd,linetitulo)#
        numBytes = os.write(fd,lineadospuntos)#

        lineaux4 = concat.replace('\n',' ').replace('\r', '').replace(':',' ').replace('...',' ')
        lineaux3 = lineaux4.replace('"',' ')
        lineaux3.rstrip('\n')
        lineaux3 = bytes(lineaux3, 'utf-8').decode('utf-8', 'ignore')
        lineadescripcion = str.encode(lineaux3)
        numBytes = os.write(fd,lineadescripcion)# 
        #n2 = concat.count(' ')+n2+1
        #n2String = str(n2) 
        #n2String2 = str.encode(n2String)
        #numBytes = os.write(fd,linenum)#
        #numBytes = os.write(fd,n2String2)#
        #numBytes = os.write(fd,linecierrenum)#
        
        lineacierretotal = str.encode('",')
        numBytes = os.write(fd,lineacierretotal)#


        lineaux = concat.replace('\n',' ').replace('\r', '')

            
'''

                

def run():
    parse_home()

if __name__ == '__main__':
    run()
