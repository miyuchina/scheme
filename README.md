# Scheme

This repository contains a working implementation of the Scheme interpreter in Python.

# Usage

Only Python 3.6 or higher is supported.
Backports to Python 3.5 could probably be done by removing all the f-strings,
but earlier versions might have further trouble with star operators.

```sh
python3 -m scheme
```

... will land you in the Scheme interpreter.
Alternatively, pass in a filename, and the interpreter will print out its result:

```sh
python3 -m scheme foo.scm
```

As a bonus, running:

```sh
python3 -i scheme.py
```

... will run Scheme and Python back-to-back, so you can do weird things like:

```python
[scheme]
> (define foo 42)
> (define (add x y) (+ x y))
> foo
42
> (add 1 2)
3
[python]
>>> interp.env['foo']
42
>>> interp.env['add'](1, 2)
3
```

# Features

Most arithmetic and boolean operators are built-in.
Integers, floats and booleans are implemented as Python literals.
Pairs are implemented as tuples, and lists are implemented as Python lists.
All expressions are evaluated in applicative order.

Some special forms are listed below:

- [define](#define)
- [lambda](#lambda)
- [if](#if)
- [cond](#cond)
- [let](#let)
- [delay](#delay)
- [force](#force)

## define

### ... a variable

* **syntax**: `(define NAME EXPR)`
* **returns**: `None`
* **example**:
```scheme
> (define x 42)
> x
42
```

### ... a function

* **syntax**: `(define (NAME * PARAM) * EXPR)`
* **returns**: `None`
* **example**:
```scheme
> (define (add x y) (+ x y))
> (add 1 2)
3
```

All expressions in the definition body are evaluated, though only the last one is returned.

## lambda

* **syntax**: `(lambda (* PARAM) * EXPR)`
* **returns**: `<Procedure * PARAM>`
* **example**:
```scheme
> (define add (lambda x y) (+ x y))
> (add 1 2)
3
> ((lambda (x y) (+ x y)) 1 2)
3
```

All expressions in the definition body are evaluated, though only the last one is returned.

## if

* **syntax**: `(if COND_EXPR TRUE_EXPR FALSE_EXPR)`
* **returns**: the result of either `TRUE_EXPR` or `FALSE_EXPR`
* **example**:
```scheme
> (if (< 1 2) 1 2)
1
> (if (> 1 2) 1 2)
2
```

The `if` expression short-circuits; that is, if condition evaluates to true,
the false expression is never evaluated.

## cond

* **syntax**: `(cond * (COND_EXPR EXPR) ? (else EXPR))`
* **returns**: the result of `EXPR` whose `COND_EXPR` evaluates to `True`, or the else branch.
* **example**:
```scheme
> (cond ((> 1 2) 3) ((< 4 5) 6) (else 7))
6
```

## let

* **syntax**: `(let (* (NAME EXPR)) * EXPR)`
* **returns**: the result of the last expression in the block.
* **example**:
```scheme
> (let ((x 3)
        (y 4))
       (+ x y))
7
```

## delay

* **syntax**: `(delay EXPR)`
* **returns**: `<Procedure>`
* **example**:
```scheme
> (define p (delay (+ x y))
> (define x 1)
> (define y 2)
> (p)
3
```

`EXPR` are not evaluated until the expression is called or `force`-d. See below.

## force

* **syntax**: `(force EXPR)`
* **returns**: the result of `EXPR`
* **example**:
```scheme
> (define p (delay (+ x y))
> (define x 1)
> (define y 2)
> (force p)
3
```

