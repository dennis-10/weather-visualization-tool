import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

#vem do front
#data inicial e final com horario inicial e final trazidos do input
startDate = "01/01/2022 00:00:00"
endDate = "01/01/2022 04:00:00"
selectedCell2 = 16

#procura a pasta definida pelo path que o usuário colocou
folder = './src/static/dados_pluviometros'
if os.path.exists(folder):
    if len(os.listdir(folder)) == 0:
        print("A pasta destinada aos arquivos com os dados pluviométricos está vazia!")
        exit()
else:
    print("Não existe uma pasta destinada aos arquivos com os dados pluviométricos!")
    exit()

#trata o formato das datas 
startDay = startDate[0:10]
endDay = endDate[0:10]
startHour = startDate[11:19]
endHour = endDate[11:19]
startDayFile = startDay[6:10] + startDay[3:5]
endDayFile = endDay[6:10] + endDay[3:5]


#dicionario das celulas que contem estações
celulas = {
    1: '',
    2: '',
    3: '',
    4: '',
    5: '',
    6: '',
    7: '',
    8: '',
    9: '',
    10: 'guaratiba',
    11: ['grota_funda', 'recreio'],
    12: 'barrinha',
    13: '',
    14: '',
    15: '',
    16: 'sepetiba',
    17: '',
    18: '',
    19: ['cidade_de_deus', 'riocentro'],
    20: ['alto_da_boa_vista','tijuca_muda','rocinha','tijuca','jardim_botanico',
    'vidigal','santa_teresa','copacabana','laranjeiras','urca'],
    21: '',
    22: '',
    23: 'santa_cruz',
    24: 'campo_grande',
    25: 'bangu',
    26: ['grajau_jacarepagua','madureira','piedade','tanque'],
    27: ['grande_meier','grajau','sao_cristovao','saude'],
    28: '',
    29: '',
    30: '',
    31: 'av_brasil_mendanha',
    32: '',
    33: ['anchieta','iraja'],
    34: ['penha','ilha_do_governador'],
    35: '',
    36: '',
    37: '',
    38: '',
    39: '',
    40: '',
    41: '',
    42: '',
    43: '',
    44: '',
    45: '',
    46: '',
    47: '',
    48: '',
    49: ''
}

stations = celulas[selectedCell2]

#se nao tiver estacao na celula nao vai precisar gerar grafico
if stations == "":
    print("Célula do grid não tem estação pluviométrica.")
    exit()

volume = []
first = True

#busca dos arquivos no path do usuario
if type(stations) == list:
    for i in stations:
        stationPatternStart = os.path.join(folder, i+'_'+startDayFile+'_Plv.txt')
        stationPatternEnd = os.path.join(folder, i+'_'+endDayFile+'_Plv.txt')
        if not os.path.exists(stationPatternStart):
            print("O arquivo de data-início não está na pasta.")
            if not os.path.exists(stationPatternEnd):
                print("O arquivo de data-fim não está na pasta.")
            exit()
        
        fileStart = open(stationPatternStart, 'r')
        lines = fileStart.readlines()
        stop=False
        for i in range(5,len(lines)):
            line = lines[i].split()
            if line[0]==startDay and line[1]==startHour:
                register=0
                while stop==False:
                    if first:
                        volume.append(float(line[2]))
                    else:
                        volume[register] = volume[register] + float(line[2])
                        register+=1
                    i+=1
                    line = lines[i].split()
                    if line[0]==endDay and line[1]==endHour:
                        if first:
                            volume.append(float(line[2]))
                        else:
                            volume[register] = volume[register] + float(line[2])
                            register+=1
                        stop=True
                first=False
        fileStart.close()
    for k in range(0,len(volume)):
        volume[k] = float(volume[k]/len(stations))

else:
    stationPatternStart = os.path.join(folder, stations+'_'+startDayFile+'_Plv.txt')
    stationPatternEnd = os.path.join(folder, stations+'_'+endDayFile+'_Plv.txt')
    if not os.path.exists(stationPatternStart):
        print("O arquivo de data-início não está na pasta.")
        if not os.path.exists(stationPatternEnd):
            print("O arquivo de data-fim não está na pasta.")
        exit()
    fileStart = open(stationPatternStart, 'r')
    lines = fileStart.readlines()
    stop=False
    for i in range(5,len(lines)):
        line = lines[i].split()
        if line[0]==startDay and line[1]==startHour:
            while stop==False:
                volume.append(float(line[2]))
                i+=1
                line = lines[i].split()
                if line[0]==endDay and line[1]==endHour:
                    volume.append(float(line[2]))
                    stop=True
    fileStart.close()


#dados para o grafico
title = 'Grid Cell: ' + str(selectedCell2)
x = np.arange(1,len(volume)+1,1)
y = volume
tfinal = max(x)
x0 = 1
fig, ax = plt.subplots(1, 1, figsize = (6, 3))

def animate(i):
    ax.cla() # clear the previous image
    ax.plot(x[:i], y[:i]) # plot the line
    ax.set_xlim([x0, tfinal]) # fix the x axis
    ax.set_ylim([1.1*np.min(y), 1.1*np.max(y)]) # fix the y axis
    ax.set_title(title)

#plot do grafico

anim2 = animation.FuncAnimation(fig, animate, frames = len(x) + 1, interval = 1000, blit = False, repeat=False)
anim2 = anim2.to_html5_video()
