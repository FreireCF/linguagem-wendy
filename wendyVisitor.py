# Generated from wendy.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .wendyParser import wendyParser
else:
    from wendyParser import wendyParser

# This class defines a complete generic visitor for a parse tree produced by wendyParser.

class wendyVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by wendyParser#program.
    def visitProgram(self, ctx:wendyParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#functDecl.
    def visitFunctDecl(self, ctx:wendyParser.FunctDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#statement.
    def visitStatement(self, ctx:wendyParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#varDecl.
    def visitVarDecl(self, ctx:wendyParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#varType.
    def visitVarType(self, ctx:wendyParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#ifStmt.
    def visitIfStmt(self, ctx:wendyParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#whileStmt.
    def visitWhileStmt(self, ctx:wendyParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#block.
    def visitBlock(self, ctx:wendyParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#exprStmt.
    def visitExprStmt(self, ctx:wendyParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#identifier.
    def visitIdentifier(self, ctx:wendyParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#parens.
    def visitParens(self, ctx:wendyParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#negation.
    def visitNegation(self, ctx:wendyParser.NegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#comparison.
    def visitComparison(self, ctx:wendyParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#or.
    def visitOr(self, ctx:wendyParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#assignment.
    def visitAssignment(self, ctx:wendyParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#multiplicative.
    def visitMultiplicative(self, ctx:wendyParser.MultiplicativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#boolLiteral.
    def visitBoolLiteral(self, ctx:wendyParser.BoolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#additive.
    def visitAdditive(self, ctx:wendyParser.AdditiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#callFunct.
    def visitCallFunct(self, ctx:wendyParser.CallFunctContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#and.
    def visitAnd(self, ctx:wendyParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#integerLiteral.
    def visitIntegerLiteral(self, ctx:wendyParser.IntegerLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#floatLiteral.
    def visitFloatLiteral(self, ctx:wendyParser.FloatLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#args.
    def visitArgs(self, ctx:wendyParser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#params.
    def visitParams(self, ctx:wendyParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#param.
    def visitParam(self, ctx:wendyParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wendyParser#returnStmt.
    def visitReturnStmt(self, ctx:wendyParser.ReturnStmtContext):
        return self.visitChildren(ctx)



del wendyParser