import sys

from antlr4 import FileStream, CommonTokenStream
from WendyLexer import WendyLexer
from WendyParser import WendyParser
from semanticVisitor import SemanticVisitor


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py entrada.wd")
        return

    arquivo = sys.argv[1]

    #análise léxica
    entrada = FileStream(arquivo, encoding="utf-8")
    lexer = WendyLexer(entrada)
    tokens = CommonTokenStream(lexer)

    #analise sintática
    parser = WendyParser(tokens)
    arvore = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("\nAnálise semântica não executada: existem erros sintáticos.")
        return

    #análise semântica
    visitor = SemanticVisitor()
    visitor.visit(arvore)

    print("\nRESULTADO")

    if not visitor.erros:
        print("Nenhum erro semântico encontrado.")
    else:
        print(f"Total de erros semânticos: {len(visitor.erros)}")


if __name__ == "__main__":
    main()