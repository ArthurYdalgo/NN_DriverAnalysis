import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

# MatPlotlib
from matplotlib import pylab
import matplotlib.pyplot as plt
'''
data = np.array([3,6,2,5,8,9,5,3,6,8,4,7,8,6,5])
fig4, ax4 = plt.subplots()
ax4.set_title('Amostra de evolução')
ax4.boxplot(data, showfliers=False)
plt.show()
'''
DEGREE = 1

Qtd1=12
Qtd2=12
Qtd3=12
Qtd4=4
#Ler amostras da Rede 1
amostras1 = np.zeros((12,120))
for i in range(Qtd1):  
    linha=0      
    with open('Logs/Rede1_4-3/R1_'+str(i+1)+".txt") as f:
        for line in f:
            num = int([int(x) for x in line.split()][0])
            if(num>=1000000):#normalizacao
                num = 1000000
            amostras1[i][linha]=num
            linha+=1

#Ler amostras da Rede 2
amostras2 = np.zeros((12,120))
for i in range(Qtd2):
    linha=0
    with open('Logs/Rede2_4-10-3/R2_'+str(i+1)+".txt") as f:
        for line in f:
            num = int([int(x) for x in line.split()][0])
            if(num>=1000000):#normalizacao
                num = 1000000
            amostras2[i][linha]=num
            linha+=1

#Ler amostras da Rede 3
amostras3 = np.zeros((12,120))
for i in range(Qtd3):
    linha=0
    with open('Logs/Rede3_4-12-8-3/R3_'+str(i+1)+".txt") as f:
        for line in f:
            num = int([int(x) for x in line.split()][0])
            if(num>=1000000):#normalizacao
                num = 1000000
            amostras3[i][linha]=num
            linha+=1

#Ler amostras da Rede 4
amostras4 = np.zeros((12,120))
for i in range(Qtd4):
    linha=0
    with open('Logs/Rede4_4-24-3/R4_'+str(i+1)+".txt") as f:
        for line in f:
            num = int([int(x) for x in line.split()][0])
            if(num>=1000000):#normalizacao
                num = 1000000
            amostras4[i][linha]=num
            linha+=1

#Media das amostras 1
evolucao1 = np.zeros(120)
for i in range(120):
    m = 0
    for j in range(Qtd1):    
        m+=amostras1[j][i]    
    evolucao1[i] = m/Qtd1



'''
plt.plot(amostras1[0], marker='', color='g', linestyle='dashed',linewidth=1,label='Rede 1 (1)')
plt.plot(amostras1[1], marker='', color='lawngreen', linestyle='dashed',linewidth=1,label='Rede 1 (2)')
plt.plot(amostras1[2], marker='', color='red', linestyle='dashed',linewidth=1,label='Rede 1 (3)')

plt.plot(amostras1[3], marker='', color='magenta', linestyle='dashed',linewidth=1,label='Rede 1 (4)')
plt.plot(amostras1[4], marker='', color='aqua', linestyle='dashed',linewidth=1,label='Rede 1 (5)')
plt.plot(amostras1[5], marker='', color='orange',linestyle='dashed',linewidth=1,label='Rede 1 (6)')
'''
'''
plt.plot(amostras1[6], marker='', color='purple',linestyle='dashed',linewidth=1,label='Rede 1 (7)')
plt.plot(amostras1[7], marker='', color='firebrick', linestyle='dashed',linewidth=1,label='Rede 1 (8)')
plt.plot(amostras1[8], marker='', color='deeppink', linestyle='dashed',linewidth=1,label='Rede 1 (9)')
'''
'''
plt.plot(amostras1[9], marker='', color='grey', linestyle='dashed',linewidth=1,label='Rede 1 (10)')
plt.plot(amostras1[10], marker='', color='deeppink', linestyle='dashed',linewidth=1,label='Rede 1 (11)')
plt.plot(amostras1[11], marker='', color='grey', linestyle='dashed',linewidth=1,label='Rede 1 (12)')
'''

'''
#Analise do impacto do numero de amostras no calculo da evolução
COLOR = ['aqua','grey','pink','deeppink','purple','red']
SPAN = 6
analiseEvolucao1 = np.zeros((SPAN-1,120))
for QtdAmostras in range(SPAN-1):    
    for i in range(120):
        m = 0
        for j in range(QtdAmostras+1):    
            m+=amostras1[j][i]    
        analiseEvolucao1[QtdAmostras][i] = m/Qtd1
    plt.plot(analiseEvolucao1[QtdAmostras], marker='', linestyle='dashed',color=COLOR[QtdAmostras],linewidth=1)
'''
plt.plot(evolucao1, marker='', color='blue',linewidth=2,label='Rede 1 4-3')    

#Regressao linear da evoluçao 1
x = np.arange(120)
y = evolucao1
z = np.polyfit(x, y, DEGREE)
f = np.poly1d(z)

x_ = np.linspace(x[0], x[-1], 50)
y_ = f(x_)

plt.plot(x_, y_,'',color="dodgerblue")
pylab.title('Média de alcance de cada geração e regressão linear com Matplotlib')
ax = plt.gca()
fig = plt.gcf()



#Media das amostras 2
evolucao2 = np.zeros(120)
for i in range(120):
    m = 0
    for j in range(Qtd2):
        m+=amostras2[j][i]
    evolucao2[i] = m/Qtd2

'''
plt.plot(amostras2[0], marker='', color='g', linestyle='dashed',linewidth=1,label='Rede 2 (1)')
plt.plot(amostras2[1], marker='', color='lawngreen', linestyle='dashed',linewidth=1,label='Rede 2 (2)')
plt.plot(amostras2[2], marker='', color='red', linestyle='dashed',linewidth=1,label='Rede 2 (3)')
plt.plot(amostras2[3], marker='', color='magenta', linestyle='dashed',linewidth=1,label='Rede 2 (4)')
'''
'''
plt.plot(amostras2[4], marker='', color='aqua', linestyle='dashed',linewidth=1,label='Rede 2 (5)')
plt.plot(amostras2[5], marker='', color='orange', linestyle='dashed',linewidth=1,label='Rede 2 (6)')
plt.plot(amostras2[6], marker='', color='purple', linestyle='dashed',linewidth=1,label='Rede 2 (7)')
plt.plot(amostras2[7], marker='', color='firebrick', linestyle='dashed',linewidth=1,label='Rede 2 (8)')
plt.plot(amostras2[8], marker='', color='deeppink', linestyle='dashed',linewidth=1,label='Rede 2 (9)')
plt.plot(amostras2[9], marker='', color='grey', linestyle='dashed',linewidth=1,label='Rede 2 (10)')
plt.plot(amostras2[10], marker='', color='deeppink', linestyle='dashed',linewidth=1,label='Rede 2 (11)')
plt.plot(amostras2[11], marker='', color='grey', linestyle='dashed',linewidth=1,label='Rede 2 (12)')
'''

'''
#Analise do impacto do numero de amostras no calculo da evolução
COLOR = ['aqua','grey','pink','deeppink','purple','red']
SPAN = 6
analiseEvolucao2 = np.zeros((SPAN-1,120))
for QtdAmostras in range(SPAN-1):    
    for i in range(120):
        m = 0
        for j in range(QtdAmostras+1):    
            m+=amostras2[j][i]    
        analiseEvolucao2[QtdAmostras][i] = m/Qtd1
    plt.plot(analiseEvolucao2[QtdAmostras], marker='', linestyle='dashed',color=COLOR[QtdAmostras],linewidth=1)
'''
plt.plot(evolucao2, marker='', color='green',linewidth=2,label='Rede 2 4-10-3')


#Regressao linear da evoluçao 2
x = np.arange(120)
y = evolucao2
z = np.polyfit(x, y, DEGREE)
f = np.poly1d(z)

x_ = np.linspace(x[0], x[-1], 50)
y_ = f(x_)

plt.plot(x_, y_,'',color="mediumseagreen")
pylab.title('Média de alcance de cada geração e regressão linear com Matplotlib')
ax = plt.gca()
fig = plt.gcf()


#Media das amostras 3
evolucao3 = np.zeros(120)
for i in range(120):
    m = 0
    for j in range(Qtd3):
        m+=amostras3[j][i]
    evolucao3[i] = m/Qtd3

'''
plt.plot(amostras3[0], marker='', color='g', linestyle='dashed',linewidth=1,label='Rede 3 (1)')
plt.plot(amostras3[1], marker='', color='lawngreen', linestyle='dashed',linewidth=1,label='Rede 3 (2)')
plt.plot(amostras3[2], marker='', color='red', linestyle='dashed',linewidth=1,label='Rede 3 (3)')
plt.plot(amostras3[3], marker='', color='magenta', linestyle='dashed',linewidth=1,label='Rede 3 (4)')
plt.plot(amostras3[4], marker='', color='aqua', linestyle='dashed',linewidth=1,label='Rede 3 (5)')
plt.plot(amostras3[5], marker='', color='orange', linestyle='dashed',linewidth=1,label='Rede 3 (6)')
plt.plot(amostras3[6], marker='', color='purple', linestyle='dashed',linewidth=1,label='Rede 3 (7)')
plt.plot(amostras3[7], marker='', color='firebrick', linestyle='dashed',linewidth=1,label='Rede 3 (8)')
plt.plot(amostras3[8], marker='', color='deeppink', linestyle='dashed',linewidth=1,label='Rede 3 (9)')
plt.plot(amostras3[9], marker='', color='grey', linestyle='dashed',linewidth=1,label='Rede 3 (10)')
plt.plot(amostras3[10], marker='', color='deeppink', linestyle='dashed',linewidth=1,label='Rede 3 (11)')
plt.plot(amostras3[11], marker='', color='grey', linestyle='dashed',linewidth=1,label='Rede 3 (12)')
'''
'''
#Analise do impacto do numero de amostras no calculo da evolução
COLOR = ['aqua','grey','pink','deeppink','purple','red']
SPAN = 6
analiseEvolucao3 = np.zeros((SPAN-1,120))
for QtdAmostras in range(SPAN-1):    
    for i in range(120):
        m = 0
        for j in range(QtdAmostras+1):    
            m+=amostras3[j][i]    
        analiseEvolucao3[QtdAmostras][i] = m/Qtd1
    plt.plot(analiseEvolucao3[QtdAmostras], marker='', linestyle='dashed',color=COLOR[QtdAmostras],linewidth=1)
'''
plt.plot(evolucao3, marker='', color='gold',linewidth=2,label='Rede 3 4-12-8-3')

#Regressao linear da evoluçao 3
x = np.arange(120)
y = evolucao3
z = np.polyfit(x, y, DEGREE)
f = np.poly1d(z)

x_ = np.linspace(x[0], x[-1], 50)
y_ = f(x_)

plt.plot(x_, y_,'',color="yellow")
pylab.title('Média de alcance de cada geração e regressão linear com Matplotlib')
ax = plt.gca()
fig = plt.gcf()


#Media das amostras 4
evolucao4 = np.zeros(120)
for i in range(120):
    m = 0
    for j in range(Qtd4):
        m+=amostras4[j][i]
    evolucao4[i] = m/Qtd4


'''
plt.plot(amostras4[0], marker='', color='g', linestyle='dashed',linewidth=1,label='Rede 4 (1)')
plt.plot(amostras4[1], marker='', color='lawngreen',linestyle='dashed',linewidth=1,label='Rede 4 (2)')
plt.plot(amostras4[2], marker='', color='red',linestyle='dashed',linewidth=1,label='Rede 4 (3)')
plt.plot(amostras4[3], marker='', color='magenta', linestyle='dashed',linewidth=1,label='Rede 4 (4)')
plt.plot(amostras4[4], marker='', color='aqua',linestyle='dashed',linewidth=1,label='Rede 4 (5)')
plt.plot(amostras4[5], marker='', color='orange',linestyle='dashed',linewidth=1,label='Rede 4 (6)')
plt.plot(amostras4[6], marker='', color='purple', linestyle='dashed',linewidth=1,label='Rede 4 (7)')
plt.plot(amostras4[7], marker='', color='firebrick',linestyle='dashed',linewidth=1,label='Rede 4 (8)')
plt.plot(amostras4[8], marker='', color='deeppink',linestyle='dashed', linewidth=1,label='Rede 4 (9)')
plt.plot(amostras4[9], marker='', color='grey',linestyle='dashed',linewidth=1,label='Rede 4 (10)')
plt.plot(amostras4[10], marker='', color='deeppink',linestyle='dashed', linewidth=1,label='Rede 4 (9)')
plt.plot(amostras4[11], marker='', color='grey',linestyle='dashed',linewidth=1,label='Rede 4 (10)')
'''
'''
#Analise do impacto do numero de amostras no calculo da evolução
COLOR = ['aqua','grey','pink','deeppink','purple','red']
SPAN = 6
analiseEvolucao4 = np.zeros((SPAN-1,120))
for QtdAmostras in range(SPAN-1):    
    for i in range(120):
        m = 0
        for j in range(QtdAmostras+1):    
            m+=amostras4[j][i]    
        analiseEvolucao4[QtdAmostras][i] = m/Qtd1
    plt.plot(analiseEvolucao4[QtdAmostras], marker='', linestyle='dashed',color=COLOR[QtdAmostras],linewidth=1)
'''

#Regressao linear da evoluçao 4
x = np.arange(120)
y = evolucao4
z = np.polyfit(x, y, DEGREE)
f = np.poly1d(z)

x_ = np.linspace(x[0], x[-1], 50)
y_ = f(x_)

#plt.plot(x_, y_,'',color="firebrick")
pylab.title('Média de alcance de cada geração e regressão linear com Matplotlib')
ax = plt.gca()
fig = plt.gcf()


plt.plot(evolucao4, marker='', color='red',linewidth=2,label='Rede 4 4-24-3')
plt.legend()
plt.show()  
