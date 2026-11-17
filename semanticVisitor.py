from tabelaDeSimbolos import TabelaDeSimbolos
from WendyVisitor import WendyVisitor


class SemanticVisitor(WendyVisitor):
    def __init__(self):
        self.tabela = TabelaDeSimbolos()
        self.erros = []
        
        
    def registrar_erro(self, mensagem):
        self.erros.append(mensagem)
        print(f"ERRO SEMÂNTICO: {mensagem}")


    def visitVarDecl(self, ctx):
        tipo = ctx.varType_().getText()
        nome = ctx.ID().getText()
        if not self.tabela.declarar(nome, tipo):
            self.registrar_erro(
                f"Variável '{nome}' já foi declarada."
            )
        if ctx.expr():
            self.visit(ctx.expr())


    def visitIdentifier(self, ctx):
        nome = ctx.ID().getText()
        if not self.tabela.existe(nome):
            self.registrar_erro(
                f"Variável '{nome}' utilizada antes da declaração."
            )


    def visitAssignment(self, ctx):
        nome = ctx.ID().getText()
        if not self.tabela.existe(nome):
            self.registrar_erro(
                f"Variável '{nome}' utilizada antes da declaração."
            )
        self.visit(ctx.expr())


    def visitFunctDecl(self, ctx):
        self.tabela.entrar_escopo()
        if ctx.params():
            for param in ctx.params().param():
                tipo = param.type_().getText()
                nome = param.ID().getText()
                if not self.tabela.declarar(nome, tipo):
                    self.registrar_erro(
                        f"Parâmetro '{nome}' já foi declarado."
                    )
        for statement in ctx.block().statement():
            self.visit(statement)
        self.tabela.sair_escopo()

    
    def visitBlock(self, ctx):
        self.tabela.entrar_escopo()
        for statement in ctx.statement():
            self.visit(statement)
        self.tabela.sair_escopo()

    
    def visitCallFunct(self, ctx):
        if ctx.args():
            self.visit(ctx.args())