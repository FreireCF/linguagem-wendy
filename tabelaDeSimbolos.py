class TabelaDeSimbolos:
    def __init__(self):
        self.escopos = [{}]   # pilha de escopos: cada um é um dict {nome: tipo}
        self.funcoes = {}     # {nome: {"retorno": tipo, "params": [tipos]}}


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


    def declarar_funcao(self, nome, tipo_retorno, tipos_params):
        if nome in self.funcoes:
            return False
        self.funcoes[nome] = {"retorno": tipo_retorno, "params": tipos_params}
        return True


    def existe_funcao(self, nome):
        return nome in self.funcoes


    # retorna {"retorno": tipo, "params": [tipos]} ou None
    def obter_funcao(self, nome):
        return self.funcoes.get(nome)


    def obter_tipo_funcao(self, nome):
        return self.funcoes.get(nome)
 
 
    def obter_parametros(self, nome):
        return self.parametros.get(nome, [])