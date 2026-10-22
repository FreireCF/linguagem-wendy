"""
Uso:
    python lexer_aluno.py [arquivo]

Ordem sugerida:
  TODOs 1-3  : primitivas do AFD
  TODOs 4-5  : construtores genéricos (literal, trie)
  TODOs 6-7  : construtores específicos (ID, NUM)
  TODOs 8-9  : motor do lexer
  Config     : palavras reservadas, operadores, símbolos, alfabeto

"""
from __future__ import annotations
from dataclasses import dataclass
import sys

# =====================================================================
# 1. TOKEN
# =====================================================================

@dataclass
class Token:
    tipo: str
    valor: str
    linha: int
    coluna: int

    def __repr__(self) -> str:
        return f"<{self.tipo}, {self.valor!r}> @ {self.linha}:{self.coluna}"


# =====================================================================
# 2. AFD — tabela de transições
# =====================================================================

class AFD:
    """AFD representado por tabela (estado, símbolo) -> estado."""

    def __init__(self, nome: str):
        self.nome = nome
        self.transicoes: dict[tuple[int, str], int] = {}
        self.finais: set[int] = set()
        self.inicial: int = 0
        self._prox: int = 1

    def novo_estado(self) -> int:
        e = self._prox
        self._prox += 1
        return e

    def transicao(self, origem: int, simbolos: str, destino: int) -> None:
        """TODO 1: para CADA caractere c em `simbolos`, registre
        transicoes[(origem, c)] = destino."""
        for c in simbolos:
            self.transicoes[(origem, c)] = destino
        #raise NotImplementedError

    def marcar_final(self, estado: int) -> None:
        """Adiciona `estado` ao conjunto de estados finais."""
        self.finais.add(estado)
        #raise NotImplementedError

    def maior_prefixo(self, texto: str) -> int:
        """Retorna o comprimento do MAIOR prefixo de `texto`
        aceito pelo AFD, ou -1 se nenhum prefixo for aceito.
        """
        estado = self.inicial
        ultimo = 0 if estado in self.finais else -1
        for i, c in enumerate(texto):
            prox = self.transicoes.get((estado, c))
            if prox is None:
                break
            estado = prox
            if estado in self.finais: 
                ultimo = i + 1
        return ultimo
    
        #raise NotImplementedError


# =====================================================================
# 3. CONFIGURAÇÃO DA LINGUAGEM
# ---------------------------------------------------------------------
# =====================================================================

# --- Alfabeto de identificadores -----------------------------------
LETRAS_ID       = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
INICIAIS_ID     = LETRAS_ID                # 1º caractere
CONTINUACAO_ID  = LETRAS_ID + "0123456789_"      # caracteres seguintes

# --- Dígitos (para números) -----------------------------------------
DIGITOS = "0123456789"

# --- Espaços em branco ignorados ------------------------------------
ESPACOS = " \t\r\n"

# --- Palavras reservadas: lexema -> tipo ---------------------------
PALAVRAS_RESERVADAS: dict[str, str] = {
    # Estruturas
    "si":     "IF",
    "sinon":  "ELSE",
    "tant":   "WHILE",
    "retour": "RETURN",
    
    # Tipos primitivos e  literais
    "int":    "TP_INT",
    "float":  "TP_FLOAT",
    "void":   "TP_VOID",
    "bool":   "TP_BOOL",
    "vrai":   "BOOL_LIT",
    "faux":   "BOOL_LIT",
}

# --- Operadores compostos: lexema -> tipo --------------------------
# Todos reconhecidos por um único AFD-trie ("FIXO").
OPERADORES: dict[str, str] = {
    # Atribuição 
    "=":  "ASSIG",
    
    #Operadores aritméticos
    "+":  "SUM",
    "-":  "SUB",
    "*":  "MULT",
    "/":  "DIV",
    
    # Operadores relacionais 
    "==": "EQ",
    "!=": "NE",
    "<=": "LE",
    ">=": "GE",
    "<":  "LT",
    ">":  "GT",
    
    # Lógicos
    "&&": "AND",
    "||": "OR",
}

# --- Símbolos simples (1 caractere): lexema -> tipo ----------------
DELIMITADORES: dict[str, str] = {
    "(": "LEF_PAR",
    ")": "RIG_PAR",
    "{": "LEF_KEY",
    "}": "RIG_KEY",
    ";": "SEMICOL",
    ",": "COMMA",
}

# --- Comentário 
COMENT = "//"
COMENT_BLOCK = ("/*", "*/")


# Tabela combinada (operadores + símbolos). Usada no trie e na
# reclassificação. Não precisa editar.
FIXOS: dict[str, str] = {**OPERADORES, **DELIMITADORES}


# =====================================================================
# 4. CONSTRUTORES GENÉRICOS DE AFDs
# ---------------------------------------------------------------------
# Estes dois construtores bastam para reconhecer QUALQUER conjunto
# finito de lexemas fixos (operadores, palavras-chave, símbolos).
# =====================================================================


def afd_literal(nome: str, texto: str) -> AFD:
    """Constrói AFD que reconhece EXATAMENTE a string `texto`.

    Ex.: afd_literal("PV", ";")
         afd_literal("OP_EQ", "==")

    Dica: crie um estado para cada prefixo de `texto`.
    O estado correspondente ao texto completo é o único final.
    """
    afd = AFD(nome)
    # TODO 4:
    atual = afd.inicial
    for c in texto:
        prox = afd.novo_estado()
        afd.transicao(atual, c, prox)
        atual = prox
    afd.marcar_final(atual)
    return afd


def afd_conjunto_literais(nome: str, textos: list[str]) -> AFD:
    """Constrói AFD que reconhece QUALQUER uma das strings.

    Ex.: afd_conjunto_literais("FIXO", ["==", "!=", "<=", ">=", "=", "<", ">"])

    Compartilha estados para prefixos comuns (ex.: "==" e "="
    compartilham o primeiro estado). A classificação fina é feita
    depois, olhando o valor reconhecido.
    """
    afd = AFD(nome)
    # TODO 5: para cada texto, desça no trie a partir de afd.inicial;
    #         crie estados quando não houver transição; marque o nó
    #         final de cada texto.
    for texto in textos:
        atual = afd.inicial
        for c in texto:
            prox = afd.transicoes.get((atual, c))
            if prox is None:
                prox = afd.novo_estado()
                afd.transicao(atual, c, prox)
            atual = prox
        afd.marcar_final(atual)
    return afd


# =====================================================================
# 5. CONSTRUTORES ESPECÍFICOS — ID e NUM
# ---------------------------------------------------------------------
# Ajuste estes conforme a forma dos tokens da SUA linguagem.
# =====================================================================


def afd_identificador() -> AFD:
    """[INICIAIS_ID][CONTINUACAO_ID]* -> tipo ID.

    Usa as constantes da CONFIGURAÇÃO. Para permitir, por exemplo,
    `$` no meio de identificadores, basta editar CONTINUACAO_ID.
    """
    afd = AFD("ID")
    # TODO 6:
    q1 = afd.novo_estado()
    afd.transicao(afd.inicial, INICIAIS_ID, q1)
    afd.transicao(q1, CONTINUACAO_ID, q1)
    afd.marcar_final(q1)
    return afd


def afd_numero() -> AFD:
    """[DIGITOS]+ -> tipo NUM.

    Para aceitar floats, adicione estados e transições para '.'
    (ex.: 12.5) e para expoente 'e'/'E'.
    Para hexadecimal, aceite o prefixo '0x' e A-F em DIGITOS.
    """
    afd = AFD("NUM")
    q1 = afd.novo_estado()   # parte inteira 
    q2 = afd.novo_estado()   # leu o .
    q3 = afd.novo_estado()   # parte decimal
    afd.transicao(afd.inicial, DIGITOS, q1)
    afd.transicao(q1, DIGITOS, q1)
    afd.transicao(q1, ".", q2)
    afd.transicao(q2, DIGITOS, q3)
    afd.transicao(q3, DIGITOS, q3)
    afd.marcar_final(q1)
    afd.marcar_final(q3)
    return afd


# =====================================================================
# 6. LEXER
# =====================================================================

class Lexer:
    def __init__(self, entrada: str, regras: list[tuple[str, AFD]]):
        self.entrada = entrada
        self.regras = regras
        self.pos = 0
        self.linha = 1
        self.coluna = 1

    def _avancar(self, n: int) -> None:
        for _ in range(n):
            if self.pos >= len(self.entrada):
                return
            if self.entrada[self.pos] == "\n":
                self.linha += 1
                self.coluna = 1
            else:
                self.coluna += 1
            self.pos += 1

    def _reclassificar(self, tipo: str, valor: str) -> str:
        """Refina o tipo bruto usando a CONFIGURAÇÃO:
          - ID   -> palavra reservada, se aplicável
          - FIXO -> operador ou símbolo específico
        """
        if tipo == "ID" and valor in PALAVRAS_RESERVADAS:
            return PALAVRAS_RESERVADAS[valor]
        if tipo == "NUM":
            return "FLOAT" if "." in valor else "INT" # sempre existe
        if tipo == "FIXO":
            return FIXOS[valor]         # sempre existe
        return tipo

    def proximo_token(self) -> Token | None:
        # 1) pular espaços em branco
        self.ignorar_coments()
        if self.pos >= len(self.entrada):
            return None

        linha, coluna = self.linha, self.coluna
        resto = self.entrada[self.pos:]

        # 2) processa o máximo de caracteres
        melhor_tipo: str | None = None
        melhor_tam = 0
        for tipo, afd in self.regras:
            tam = afd.maior_prefixo(resto)
            if tam > melhor_tam:
                melhor_tam = tam
                melhor_tipo = tipo

        if melhor_tam == 0:
            raise SyntaxError(
                f"Caractere inesperado {resto[0]!r} em L{linha}:C{coluna}"
            )

        valor = resto[:melhor_tam]
        self._avancar(melhor_tam)

        # 3) reclassificação
        melhor_tipo = self._reclassificar(melhor_tipo, valor)

        return Token(melhor_tipo, valor, linha, coluna)
    

    # COMENTÁRIO 
    # O laço
    # repete até não haver mais nada a pular, então sequências como
    # "  // a \n /* b */  x" são tratadas.
    def ignorar_coments(self) -> None:
        abre_bloco, fecha_bloco = COMENT_BLOCK
        while self.pos < len(self.entrada):
            c = self.entrada[self.pos]
            if c in ESPACOS:
                self._avancar(1)
            elif self.entrada.startswith(COMENT, self.pos):
                fim = self.entrada.find("\n", self.pos)
                if fim == -1:
                    fim = len(self.entrada)
                self._avancar(fim - self.pos)
            elif self.entrada.startswith(abre_bloco, self.pos):
                linha, coluna = self.linha, self.coluna
                fim = self.entrada.find(fecha_bloco, self.pos + len(abre_bloco))
                if fim == -1:
                    raise SyntaxError(f"Comentário de bloco não fechado")
                self._avancar(fim + len(fecha_bloco) - self.pos)
            else:
                return


    def tokenizar(self) -> list[Token]:
        tokens: list[Token] = []
        while (tok := self.proximo_token()) is not None:
            tokens.append(tok)
        return tokens
# =====================================================================
# 7. PROGRAMA PRINCIPAL
# =====================================================================

def construir_regras() -> list[tuple[str, AFD]]:
    """Monta a lista de regras a partir da CONFIGURAÇÃO.
    Se você adicionar novos tipos de token (ex.: floats), acrescente
    aqui uma entrada para o AFD correspondente.
    """
    return [
        ("ID",   afd_identificador()),
        ("NUM",  afd_numero()),
        ("FIXO", afd_conjunto_literais("FIXO", sorted(FIXOS))),
    ]


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            codigo = f.read()
    else:
        codigo = sys.stdin.read()

    tokens = Lexer(codigo, construir_regras()).tokenizar()

    # Sequência de tipos em uma linha, separados por espaço, para o ANTLR
    print(" ".join(tok.tipo for tok in tokens))


if __name__ == "__main__":
    main()