grammar wendy;


// Regra inicial: um programa é uma sequência de comandos
program:
    (functDecl | statement)* EOF
    ;


// Declaração de função; void só é permitido como tipo de retorno
functDecl: 
    (type | TP_VOID) ID LEF_PAR params? RIG_PAR block
    ;


// Um comando pode ser declaração de variável, if, while, bloco, expressão ou retorno
statement:
    varDecl
    | ifStmt
    | whileStmt
    | block
    | exprStmt
    | returnStmt
    ;


// Declaração de variável: tipo nome (= valor)? ;
varDecl:
    type ID (ASSIG expr)? SEMICOL
    ;


// Tipos básicos de variáveis e parâmetros suportados
type:
    TP_INT | TP_FLOAT | TP_BOOL
    ;


// Estrutura if
ifStmt: 
    IF LEF_PAR expr RIG_PAR block (ELSE block)?
    ;


// Estrutura while
whileStmt:
    WHILE LEF_PAR expr RIG_PAR block
    ;


// Bloco delimitado por chaves { comandos }
block:
    LEF_KEY statement* RIG_KEY
    ;


// Expressão seguida de ponto e vírgula
exprStmt:
    expr SEMICOL
    ;


// Expressões com precedência no estilo C
expr:
    LEF_PAR expr RIG_PAR                        #parens
    | ID LEF_PAR args? RIG_PAR                  #callFunct 
    | SUB expr                                  # negation
    | expr ( MULT | DIV ) expr                  # multiplicative
    | expr ( SUM | SUB) expr                    # additive
    | expr ( EQ | NE | LT | GT | LE | GE ) expr # comparison
    | expr AND expr                             # and
    | expr OR expr                              # or
    | <assoc=right> ID ASSIG expr               # assignment
    | ID                                        # identifier
    | INT                                       # integerLiteral
    | FLOAT                                     # floatLiteral
    | BOOL_LIT                                  # boolLiteral
    ;


// Argumentos para chamada de função
args:
    expr (COMMA expr)*
    ;


// Parâmtros para declaração de função 
params:
    param (COMMA param)*
    ;


param:
    type ID
    ;


//retorno de função 
returnStmt:
    RETURN expr? SEMICOL
    ;


// ------------------- Lexer -------------------
//ESTRUTURAS 
IF    : 'si';
ELSE  : 'sinon';
WHILE  :  'tant';
RETURN : 'retour';


//TIPOS
TP_INT   : 'int';
TP_FLOAT : 'float';
TP_BOOL  : 'bool';
TP_VOID : 'void';
BOOL_LIT : 'vrai' | 'faux';


//IDENTIFICADORES
ID  : [a-zA-Z][a-zA-Z_0-9]* ;
INT : [0-9]+ ;
FLOAT : [0-9]+ '.' [0-9]+;


//ATRIBUIÇÃO
ASSIG: '=';

//ARITMÉTICOS
SUM  : '+';
SUB  : '-';
MULT : '*';
DIV  : '/';


//RELACIONAIS
EQ : '==';
NE : '!=';
LE : '<=';
GE : '>=';
LT : '<';
GT : '>';


//LÓGICOS 
AND : '&&';
OR  : '||';


//DELIMITADORES
LEF_PAR : '(';
RIG_PAR : ')';
LEF_KEY: '{';
RIG_KEY: '}';
SEMICOL: ';';
COMMA: ',';



//IGNORADOS
//TABULAÇÃO
WS : [ \t\r\n]+ -> skip ;
//COMENTÁRIOS
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;