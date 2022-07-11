import time
import numpy as np

def mod_quarter_tam(val, tam):
    key = (val%(int(tam/4)))*4

    return key

def constant(val, tam):
    return 25

mod=0
const=0
for j in range(20):
    x=[]
    for i in range(1000000):
        x.append(np.random.randint(1000000))
    print(j)

    a=0
    t0=time.time()
    for no in x:
        a+=1
        if no == -100:
            a=-1
            break
    t1=time.time()
    mod += t1-t0

    index = 0
    b=0
    t0=time.time()
    valor = x[index]
    while valor != -100:
        index += 1
        b += 1   #conta a próxima query (a próxima pode não entrar no while)
        valor = x[index%1000000]
        if (index%1000000) == 0:
            b = -1
            break
    t1=time.time()
    const += t1-t0

print(mod/10)
print(const/10)
print(const/mod)
