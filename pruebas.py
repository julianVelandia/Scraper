def parse_home():


    a = {'uno':' unob', 'dos': 'dosa', 'tres': 'tresb','cuatro':'cuatroa'}


    b = {'unoc':' unod', 'dos': 'dosb', 'tresc': 'tresd','cuatro':'cuatrob'}

    c={}
    
    
    n=0
    for i,j in a.items():
        for k,m in b.items():

            if i == k:
                aux={j:m}
                c.update(aux)

    print(a)  
    print(b)     
    print(c)  

def run():
    parse_home()

if __name__ == '__main__':
    run()