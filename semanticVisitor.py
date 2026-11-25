from tabelaDeSimbolos import TabelaDeSimbolos
from wendyVisitor import wendyVisitor


class SemanticVisitor(wendyVisitor):
    def __init__(self):
        self.tabela = TabelaDeSimbolos()
        self.erros = []
        self.profundidade_laco = 0     # > 0 quando estamos dentro de um 'tant'
        self.funcao_atual = None       # tipo de retorno da função sendo visitada
        self.nome_funcao_atual = None  # usado só nas mensagens de erro


    def registrar_erro(self, ctx, mensagem):
        token = ctx.start
        mensagem = f"Linha {token.line}:{token.column} - {mensagem}"
        self.erros.append(mensagem)
        print(f"ERRO SEMÂNTICO: {mensagem}")


    # int -> float é permitido (alargamento); float -> int não (estreitamento).
    # Se algum tipo é None, já houve erro antes: não gera erro em cascata.
    def compativel(self, destino, origem):
        if destino is None or origem is None:
            return True
        if destino == origem:
            return True
        return destino == "float" and origem == "int"
    

    # condições de 'si' e 'tant' precisam ser int (a linguagem não tem booleano)
    def verificar_condicao(self, ctx_expr, comando):
        tipo = self.visit(ctx_expr)
        if tipo == "float":
            self.registrar_erro(ctx_expr, f"Condição do '{comando}' deve ser int, mas é float.")


    def visitVarDecl(self, ctx):
        tipo = ctx.varType().getText()
        nome = ctx.ID().getText()
        # visita a expressão antes de declarar
        if ctx.expr():
            tipo_expr = self.visit(ctx.expr())
            if not self.compativel(tipo, tipo_expr):
                self.registrar_erro(ctx, f"Não é possível atribuir {tipo_expr} à variável "
                                         f"'{nome}' do tipo {tipo}.")
        if not self.tabela.declarar(nome, tipo):
            self.registrar_erro(ctx, f"Variável '{nome}' já foi declarada.")


    def visitFunctDecl(self, ctx):
        tipo = ctx.varType().getText()
        nome = ctx.ID().getText()
        params = ctx.params().param() if ctx.params() else []
        tipos_params = [p.varType().getText() for p in params]

        # registra a função antes do corpo, permitindo recursão
        if not self.tabela.declarar_funcao(nome, tipo, tipos_params):
            self.registrar_erro(ctx, f"Função '{nome}' já foi declarada.")

        self.funcao_atual = tipo
        self.nome_funcao_atual = nome
        self.tabela.entrar_escopo()
        for param in params:
            tipo_param = param.varType().getText()
            nome_param = param.ID().getText()
            if not self.tabela.declarar(nome_param, tipo_param):
                self.registrar_erro(param, f"Parâmetro '{nome_param}' já foi declarado.")
        # o corpo compartilha o escopo dos parâmetros
        for statement in ctx.block().statement():
            self.visit(statement)
        self.tabela.sair_escopo()
        self.funcao_atual = None
        self.nome_funcao_atual = None


    def visitBlock(self, ctx):
        self.tabela.entrar_escopo()
        for statement in ctx.statement():
            self.visit(statement)
        self.tabela.sair_escopo()


    def visitIfStmt(self, ctx):
        self.verificar_condicao(ctx.expr(), "si")
        for bloco in ctx.block():   # lista: bloco do 'si' e, se houver, do 'sinon'
            self.visit(bloco)


    def visitWhileStmt(self, ctx):
        self.verificar_condicao(ctx.expr(), "tant")
        self.profundidade_laco += 1
        self.visit(ctx.block())
        self.profundidade_laco -= 1


    def visitBreakStmt(self, ctx):
        if self.profundidade_laco == 0:
            self.registrar_erro(ctx, "'casser' usado fora de um laço 'tant'.")


    def visitReturnStmt(self, ctx):
        tipo_expr = self.visit(ctx.expr()) if ctx.expr() else None

        if self.funcao_atual is None:
            self.registrar_erro(ctx, "'retour' usado fora de uma função.")
        elif not ctx.expr():
            # todas as funções retornam int ou float, então o valor é obrigatório
            self.registrar_erro(ctx, f"Função '{self.nome_funcao_atual}' deve retornar "
                                     f"um valor do tipo {self.funcao_atual}.")
        elif not self.compativel(self.funcao_atual, tipo_expr):
            self.registrar_erro(ctx, f"Função '{self.nome_funcao_atual}' deve retornar "
                                     f"{self.funcao_atual}, mas retorna {tipo_expr}.")


    def visitIntegerLiteral(self, ctx):
        return "int"


    def visitFloatLiteral(self, ctx):
        return "float"


    def visitIdentifier(self, ctx):
        nome = ctx.ID().getText()
        if not self.tabela.existe(nome):
            self.registrar_erro(ctx, f"Variável '{nome}' utilizada antes da declaração.")
            return None
        return self.tabela.obter_tipo(nome)


    def visitParens(self, ctx):
        return self.visit(ctx.expr())


    def tipo_aritmetico(self, ctx):
        esq = self.visit(ctx.expr(0))
        dir = self.visit(ctx.expr(1))
        if esq is None or dir is None:
            return None
        return "float" if "float" in (esq, dir) else "int"


    def visitAdditive(self, ctx):
        return self.tipo_aritmetico(ctx)


    def visitMultiplicative(self, ctx):
        return self.tipo_aritmetico(ctx)


    # comparações e operadores lógicos resultam em int 
    def visitComparison(self, ctx):
        for e in ctx.expr():
            self.visit(e)
        return "int"


    def visitAnd(self, ctx):
        for e in ctx.expr():
            self.visit(e)
        return "int"


    def visitOr(self, ctx):
        for e in ctx.expr():
            self.visit(e)
        return "int"


    def visitAssignment(self, ctx):
        nome = ctx.ID().getText()
        tipo_expr = self.visit(ctx.expr())
        if not self.tabela.existe(nome):
            self.registrar_erro(ctx, f"Variável '{nome}' utilizada antes da declaração.")
            return None
        tipo_var = self.tabela.obter_tipo(nome)
        if not self.compativel(tipo_var, tipo_expr):
            self.registrar_erro(ctx, f"Não é possível atribuir {tipo_expr} à variável "
                                     f"'{nome}' do tipo {tipo_var}.")
        return tipo_var


    def visitCallFunct(self, ctx):
        nome = ctx.ID().getText()
        args = ctx.args().expr() if ctx.args() else []
        tipos_args = [self.visit(a) for a in args]

        funcao = self.tabela.obter_funcao(nome)
        if funcao is None:
            self.registrar_erro(ctx, f"Função '{nome}' utilizada antes da declaração.")
            return None

        params = funcao["params"]
        if len(args) != len(params):
            self.registrar_erro(ctx, f"Função '{nome}' espera {len(params)} argumento(s), "
                                     f"mas recebeu {len(args)}.")
        else:
            # compara posição a posição com a regra de compatibilidade
            for i, (tipo_param, tipo_arg) in enumerate(zip(params, tipos_args)):
                if not self.compativel(tipo_param, tipo_arg):
                    self.registrar_erro(args[i], f"Argumento {i + 1} da função '{nome}' deve ser "
                                                 f"{tipo_param}, mas é {tipo_arg}.")
        return funcao["retorno"]