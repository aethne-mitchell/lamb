<h1>Lλmb</h1>
<p align="left">
A small lambda calculus reducer using PLY<br>
Example: (2 * 3) * 2
  <img src="https://raw.githubusercontent.com/aethne-mitchell/lamb/master/sample.png"/>
</p>
The expression is converted into an abstract syntax tree according to the algebraic rules of the lambda calculus system. The beta-reductions are done within the tree structure, and because of this alpha-conversion is not needed. The method of beta-reducing while avoiding naming conflicts and the need to alpha-convert is very simple: in an 'application' subtree, convert each instance of the bound variable in the left child to the right child (the 'argument' expression) unless the variable has 're-rebound' by another 'function' (expression of the form &x.x) further down the tree. Eta conversions have not yet been implemented.

Todo:
<li>Error handling</li>
<li>Verbose Output</li>
<li>More tests</li>
<li>Clean up code</li>
