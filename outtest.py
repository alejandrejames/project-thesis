def nmfout(fl2):
    fl = open('nmfresult.res','r')
    conts = fl.readline()
    flag=0
    num = 0
    for x in conts:
        if(x=='['):
            tagstr = '<tr><td>Topic'+str(num)+'</td><td>'
            fl2.write(tagstr)
        elif(x==']'):
            fl2.write('</td></tr>')
            num = int(num) + 1
        elif(x=="'"):
            q = 0
        else:
            fl2.write(x)
    fl.close()
    fl2.close()

def ldaout(fl4):
    fl3 = open('ldaresult.res','r')
    conts = fl3.readline()
    flag=0
    num = 0
    for x in conts:
        if(x=='('):
            tagstr = '<tr><td>Topic'+str(num)+'</td><td>'
            fl4.write(tagstr)
        elif(x==')'):
            fl4.write('</td></tr>')
            num = int(num) + 1
        elif(x=='*'):
            fl4.write('-')
        elif(x=='+'):
            fl4.write(',')
        elif(x==','):
            q = 0
        elif(x=='"'):
            q = 0
        elif(x=='['):
            q = 0
        elif(x==']'):
            q = 0
        elif(x=="'"):
            q = 0
        else:
            fl4.write(x)
    fl3.close()
    fl4.close()
