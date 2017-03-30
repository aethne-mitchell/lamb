import sys
sys.path.insert(0, "../..")

tokens = ('LAMBDA', 'IDENTIFIER')
literals =['(',')','.']

def t_LAMBDA(t):
	r'[&λ]'
	return t

def t_IDENTIFIER(t):
	r'[a-z]'
	return t

t_ignore = " \t"

def t_newline(t):
	 r'\n+'
	 t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal char '%s'" % t.value[0])
    t.lexer.skip(1) # TODO 

import ply.lex as lex
lex.lex(debug=1)

# PARSER **************
def p_expr(p):
	"""expr : funct 
		| variable 
		| application"""
	p[0] = ('expr', p[1])

def p_expr_parens(p):
	"""expr : parens"""
	p[0] = p[1]

def p_funct(p):
	"""funct : LAMBDA variable '.' expr"""
	p[0] = ('funct', p[2], p[4])

def p_variable(p):
	"""variable : IDENTIFIER"""
	p[0] = ('id', p[1])

def p_application(p):
	"""application : expr expr"""
	p[0] = ('app', p[1], p[2])

def p_parens(p):
	"""parens : '(' expr ')'"""
	p[0] = p[2]

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
parser = yacc.yacc()
#prg = "&x.x(xx)"
prg = "(λm.λn.λf.m (n f)) (λa.λb.a(a(b))) (λc.λd.c(c(c(d))))"
tree = parser.parse(prg, debug=1)

def replace_at(s, i, c):
	return s[0:i] + c + s[i+1:]

tree = str(tree)
for i in range(len(tree)):
	if tree[i] == '(':
		tree = replace_at(tree, i, '[')
	elif tree[i] == ')':
		tree = replace_at(tree, i, ']')
	elif tree[i] == ',':
		tree = replace_at(tree, i, ' ')

print('\n',tree,'\n')