grammar wendy;

//est. repetição, est. condição, oper. lógico, oper. booleanos, declaração função 

// Regra inicial: um programa é uma sequência de comandos
program:
    (functDecl | statement)* EOF
    ;


functDecl: 
    (type | TP_VOID) ID LEF_PAR params? RIG_PAR block
    ;


// Um comando pode ser declaração de variável, if, while, bloco, expressão ou retornno
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


// Tipos básicos suportados
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


// Bloco delimitado por chaves
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


args:
    expr (COMMA expr)*
    ;


params:
    param (COMMA param)*
    ;


param:
    type ID
    ;


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


//IDs
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


//TABULAÇÃO
WS : [ \t\r\n]+ -> skip ;


//COMENTÁRIOS
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;