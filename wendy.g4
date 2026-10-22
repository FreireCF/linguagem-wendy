grammar wendy;

//est. repetição, est. condição, oper. lógico, oper. booleanos, declaração função 

// Regra inicial: um programa é uma sequência de comandos
program:
    (functDecl | statement)* EOF
    ;


functDecl
    : (type) ID LEF_PAR params? RIG_PAR block
    ;


// Um comando pode ser declaração de variável, if, while, bloco ou expressão
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
    type ID (ASSIG expr)? COLON
    ;


// Tipos básicos suportados
type:
    TP_INT | TP_FLOAT | TP_CHAR | TP_BOOL | TP_VOID
    ;


// Estrutura if
ifStmt: 
    IF LEF_KEY expr RIG_PAR statement (ELSE statement)?
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
    expr COLON
    ;


// Expressões com precedência no estilo C
expr:
    ID ASSIG expr                 # assignment                               
    | ID LEF_PAR args? RIG_PAR #callFunct 
    | LEF_PAR expr RIG_PAR #parens
    | expr ('==' | '!=' | '<' | '>' | '<=' | '>=') expr  # comparison
    | expr ('+' | '-') expr                     # additive
    | expr ('*' | '/') expr                     # multiplicative
    | ID                                        # identifier
    | INT                                       # integerLiteral
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
    RETURN expr? COLON
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
TP_CHAR  : 'char';
TP_BOOL  : 'bool';
TP_VOID : 'void';
BOOL_LIT : 'vrai' | 'faux';


//IDs
ID  : [a-zA-Z_][a-zA-Z_0-9]* ;
INT : [0-9]+ ;
FLOAT : [0-9]+ '.' [0-9]+;


//DELIMITADORES
ASSIG: '=';
LEF_PAR : '(';
RIG_PAR : ')';
LEF_KEY: '{';
RIG_KEY: '}';
COLON: ';';
COMMA: ',';


//TABULAÇÃO
WS           : [ \t\r\n]+ -> skip ;


//COMENTÁRIOS
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;