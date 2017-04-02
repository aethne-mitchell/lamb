<h1>Lλmb</h1>
<p align="left">
A small lambda calculus reducer using PLY<br>
Example: (2 * 3) * 2
  <img src="https://raw.githubusercontent.com/aethne-mitchell/lamb/master/sample.png"/>
</p>
The expression is converted into an abstract syntax tree according to the algebraic rules of the lambda calculus system. The beta reductions are done within the tree structure, and because of this alpha-conversion is not needed. The method of avoiding naming conflics is very simple: convert each instance of the bound variable to the 'argument' expression unless the variable is 're-rebound' by another 'function' (expression of the form &x.x) further down the tree. Eta conversions have not yet been implemented.

Todo:
<li>Error handling</li>
<li>Verbose Output</li>
<li>More tests</li>
<li>Clean up code</li>
