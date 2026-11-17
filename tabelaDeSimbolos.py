class TabelaDeSimbolos:
    def __init__(self):
        self.escopos = [{}]


    def entrar_escopo(self):
        self.escopos.append({})


    def sair_escopo(self):
        if len(self.escopos) > 1:
            self.escopos.pop()


    def declarar(self, nome, tipo):
        escopo_atual = self.escopos[-1]
        if nome in escopo_atual:
            return False
        escopo_atual[nome] = tipo
        return True


    def existe(self, nome):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return True
        return False


    def obter_tipo(self, nome):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        return None