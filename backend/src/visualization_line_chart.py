import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from src.processing_data import Observacao



class Grafico(Observacao):
    def __init__(self, num_celula, data_inicio, data_fim, hora_inicio, hora_fim, titulo="", eixoX="", eixoY=""):
        super().__init__(data_inicio, data_fim, hora_inicio, hora_fim)
        self.num_celula = num_celula
        self.titulo = titulo
        self.eixoX = eixoX
        self.eixoY = eixoY

    def processaObservacao(self):

        folder = './src/static/data/dados_pluviometros'

        if os.path.exists(folder):
            if len(os.listdir(folder)) == 0:
                #retornar mensagem para o frontend
                print("A pasta destinada aos arquivos com os dados pluviométricos está vazia!")
                exit()
        else:
            print("Não existe uma pasta destinada aos arquivos com os dados pluviométricos!")
            exit()

        startDay = self.data_inicio[0:10]
        endDay = self.data_fim[0:10]

        startDayFile = startDay[6:10] + startDay[3:5]
        endDayFile = endDay[6:10] + endDay[3:5]

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
  
        cel_number = int(self.num_celula)        
        stations = celulas[cel_number]

        horaInicio = str(self.hora_inicio)+":00"
        horaFim = str(self.hora_fim)+":00"

        #se nao tiver estacao na celula nao vai precisar gerar grafico
        if stations == "":
            #retornar mensagem no front
            print("Célula do grid não tem estação pluviométrica.")
            exit()

        volume = []
        dates = []
        first = True

        #busca dos arquivos no path do usuario
        if type(stations) == list:
            for i in stations:
                stationPatternStart = os.path.join(folder, i+'_'+startDayFile+'_Plv.txt')
                stationPatternEnd = os.path.join(folder, i+'_'+endDayFile+'_Plv.txt')
                if not os.path.exists(stationPatternStart):
                    #retornar mensagem no front
                    print("O arquivo de data-início não está na pasta.")
                    if not os.path.exists(stationPatternEnd):
                        print("O arquivo de data-fim não está na pasta.")
                    exit()
                
                fileStart = open(stationPatternStart, 'r')
                lines = fileStart.readlines()
                stop=False
                for i in range(5,len(lines)):
                    line = lines[i].split()
                    if line[0]==startDay and line[1]==horaInicio:
                        register=0
                        while stop==False:
                            if first:
                                volume.append(float(line[2]))
                                dates.append(str(line[1]))
                            else:
                                volume[register] = volume[register] + float(line[2])
                                register+=1
                            i+=1
                            line = lines[i].split()
                            if line[0]==endDay and line[1]==horaFim:
                                if first:
                                    volume.append(float(line[2]))
                                    dates.append(str(line[1]))
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
                if line[0]==startDay and line[1]==horaInicio:
                    while stop==False:
                        volume.append(float(line[2]))
                        dates.append(str(line[1]))
                        i+=1
                        line = lines[i].split()
                        if line[0]==endDay and line[1]==horaFim:
                            volume.append(float(line[2]))
                            dates.append(str(line[1]))
                            stop=True
            fileStart.close()
        
        self.eixoY = volume
        self.eixoX = dates

    def geraGrafico(self):
        print("CHEGOU AQUI")
        self.titulo = 'Grid Cell: ' + str(self.num_celula)
        #self.eixoX = np.arange(1,len(self.eixoY)+1,1)
        x = self.eixoX
        y = self.eixoY
        tfinal = x[-1]
        x0 = x[0]
        fig, ax = plt.subplots(1, 1, figsize = (6, 3))

        def animate(i):
            ax.cla() # clear the previous image
            ax.plot(x[:i], y[:i]) # plot the line
            ax.set_xlim([x0, tfinal]) # fix the x axis
            ax.set_ylim([1.1*np.min(y), 1.1*np.max(y)]) # fix the y axis
            ax.set_title(self.titulo)

        #plot do grafico

        anim = animation.FuncAnimation(fig, animate, frames = len(x) + 1, interval = 1000, blit = False, repeat=False)
        anim = anim.to_html5_video()

        return anim

