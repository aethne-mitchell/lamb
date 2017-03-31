<h1>Lλmb</h1>
A small lambda calculus reducer using PLY

Sample output, multiplying 2 and 3:
<code><pre>Lλmb:  Parsing...
Lλmb:  Statement: ((λm.λn.λf.m(nf))(λa.λb.a(ab)))(λc.λd.c(c(cd)))
Lλmb:  Reducing...
       β:01:  (λn.λf.(λa.λb.a(ab))(nf))(λc.λd.c(c(cd)))
       β:02:  λf.λb.((λc.λd.c(c(cd)))f)(((λc.λd.c(c(cd)))f)b)
       β:03:  λf.λb.(λd.f(f(fd)))((λd.f(f(fd)))b)
       β:04:  λf.λb.f(f(f(f(f(fb)))))
       β:05:  λf.λb.f(f(f(f(f(fb)))))
Lλmb:  Done
Lλmb:  λf.λb.f(f(f(f(f(fb)))))</pre></code>
