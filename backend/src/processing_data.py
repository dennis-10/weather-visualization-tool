

class Observacao:
    def __init__(self, data_inicio, data_fim, hora_inicio, hora_fim):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim

    def formataDataInicio(self):
        sd = str(self.data_inicio)
        d = sd[8:10]
        m = sd[5:7]
        y = sd[0:4]
        sd = d + '/' + m + '/' + y
        return sd
    
    def formataDataFim(self):
        sd = str(self.data_fim)
        d = sd[8:10]
        m = sd[5:7]
        y = sd[0:4]
        sd = d + '/' + m + '/' + y
        return sd
