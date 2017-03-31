import sys, copy
sys.path.insert(0, "../..")
NAME = "Lλmb:  "
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
lex.lex() #debug=1)

# PARSER ***************
precedence = (
	('left', 'LEFT'),
	)

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
	"""application : expr expr %prec LEFT"""
	p[0] = ('appl', p[1], p[2])

def p_parens(p):
	"""parens : '(' expr ')'"""
	p[0] = p[2]

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
parser = yacc.yacc()
prg = "(λm.λn.λf.m (n f)) (λa.λb.a(a(b))) (λc.λd.c(c(c(d))))"
print(NAME + "Parsing...")
tree = parser.parse(prg) #, debug=1)

def replace_at(s, i, c):
	return s[0:i] + c + s[i+1:]

if False:
	tree_str = str(tree)
	for i in range(len(tree_str)):
		if tree_str[i] == '(':
			tree_str = replace_at(tree_str, i, '[')
		elif tree_str[i] == ')':
			tree_str = replace_at(tree_str, i, ']')
		elif tree_str[i] == ',':
			tree_str = replace_at(tree_str, i, ' ')
	print(NAME + "Parse tree for mshang.ca/syntree/\n")
	print(tree_str, '\n')

# REDUCTION

#isinstance(s,str)
#please remember its a binary tree
# b_f is filter, b_s is stop condition
#adapting this function to anything else will be dicey
def tree_to_str(t):
	#print(t)
	if t[0] == 'id':
		return t[1]
	if t[0] == 'expr':
		return tree_to_str(t[1])
	if t[0] == 'funct':
		return 'λ' + tree_to_str(t[1]) + '.' + tree_to_str(t[2])
	if t[0] == 'appl':
		ls = rs = ""
		if t[1][1][0] == 'id':
			ls = tree_to_str(t[1])
		else:
			ls = '(' + tree_to_str(t[1]) + ')'
		if t[2][1][0] == 'id':
			rs = tree_to_str(t[2])
		else:
			rs = '(' + tree_to_str(t[2]) + ')'
		return ls + rs

def tuple_to_list(t):
	if isinstance(t, tuple):
		out = []
		for i in t:
			out.append(tuple_to_list(i))
		return out
	return t

print(NAME + "Statement: " + tree_to_str(tree))
print(NAME + "Reducing...")

def dfdo(t, f): #left depth first search applying f whenever possible
	if len(t) == 2:
		if t[0] == 'expr':
			return dfdo(t[1], f)
		else:
			return
	dfdo(t[1], f)
	dfdo(t[2], f)
	f(t)

def replace_if_not_bound(t, v, a):
	#print("replace debug:  " + tree_to_str(t) + " v,a: " + v + ' ' + tree_to_str(a))
	#print("RD    \n", t)
	if len(t) == 2:
		if t[0] == 'expr':
			if t[1][0] == 'id':
				if t[1][1] == v:
					t[1] = copy.deepcopy(a)
			else:
				replace_if_not_bound(t[1], v, a)
		else: #function
			replace_if_not_bound(t[1], v, a)
	else:
		if t[0] == 'funct':
			if t[1][1] != v:
				replace_if_not_bound(t[2], v, a)
		else: #application
			replace_if_not_bound(t[1], v, a)
			replace_if_not_bound(t[2], v, a)

def app(t):
	#print(NAME + tree_to_str(t))
	if t[0] == 'appl':
		#print(NAME + 'Application?: ' + tree_to_str(t))
		if t[1][1][0] == 'funct':
			#print(NAME + 'Application found.')
			arg = t[2]
			pointer = t
			while pointer[0] != 'id':
				pointer = pointer[1]
			var = pointer[1]
			#print(NAME + 'β reducing (' + tree_to_str(arg) + ') for bound variable: ' + var)
			#t_sub = t[1]
			#t[1][1][2] = replace_if_not_bound(t[1][1][2], var, arg)
			replace_if_not_bound(t[1][1][2], var, arg)
			del t[2]
			t[0] = 'expr'
			t[1] = t[1][1][2]
			#print(tree_to_str(t))

def clean_tree(t):
	while len(t) == 2 and t[0] == 'expr' and t[1][0] == 'expr':
			t[1] = t[1][1]
	if t[0] != 'id':
		clean_tree(t[1])
		if len(t) > 2:
			clean_tree(t[2])

def nocomma(s):
	for i in range(len(s)):
		if s[i] == ',':
			s = replace_at(s, i, ' ')
	return s

prev_tree = ['eval', ['id', 'wew']]
tree = tuple_to_list(tree)
stepcounter = 1
while tree_to_str(prev_tree) != tree_to_str(tree):
	prev_tree = copy.deepcopy(tree)
	dfdo(tree, app)
	clean_tree(tree)
	stepstr = ("%.2d" % (stepcounter))
	print(' '*len(NAME) + 'β:'+("%.2d" % (stepcounter)) + ': ' + tree_to_str(tree))
	stepcounter += 1
	#print(nocomma(str(tree)))
print(NAME + "Done")
clean_tree(tree)
#print(nocomma(str(tree)))
print(NAME + tree_to_str(tree))
