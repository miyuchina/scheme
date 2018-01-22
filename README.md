# Scheme

This repository contains a working implementation of the Scheme interpreter in Python.

## Usage

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

## Features

Most arithmetic and boolean operators are built-in.
Integers, floats and booleans are implemented as Python literals.
Pairs are implemented as Python tuples, and lists are implemented as Scheme linked lists.
All expressions are evaluated in applicative order.

Functions have lexical scoping, but can see everything in its parent scope as well:

```scheme
> (define x 2)
> (define y 4)
> (define (foo) (define x 3) (+ x y))
> (foo)
7
> x
2
```

There are no for loops or while loops, but recursion works as expected.

Some special forms are listed below:

- [define](#define)
- [lambda](#lambda)
- [if](#if)
- [cond](#cond)
- [let](#let)
- [delay](#delay)
- [force](#force)
- [Scheme functions](#scheme-functions)

### define

#### ... a variable

* **syntax**: `(define NAME EXPR)`
* **returns**: `None`
* **example**:
```scheme
> (define x 42)
> x
42
```

#### ... a function

* **syntax**: `(define (NAME * PARAM) * EXPR)`
* **returns**: `None`
* **example**:
```scheme
> (define (add x y) (+ x y))
> (add 1 2)
3
```

All expressions in the definition body are evaluated, though only the last one is returned.

### lambda

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

### if

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

### cond

* **syntax**: `(cond * (COND_EXPR EXPR) ? (else EXPR))`
* **returns**: the result of `EXPR` whose `COND_EXPR` evaluates to `True`, or the else branch.
* **example**:
```scheme
> (cond ((> 1 2) 3) ((< 4 5) 6) (else 7))
6
```

### let

* **syntax**: `(let (* (NAME EXPR)) * EXPR)`
* **returns**: the result of the last expression in the block.
* **example**:
```scheme
> (let ((x 3)
        (y 4))
       (+ x y))
7
```

### delay

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

`EXPR` is not evaluated until the expression is called or `force`-d. See below.

### force

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

### Scheme functions

Some functions are easier to define in Scheme than in Python,
so their implementation is not included in the interpreter.
Here are, however, a few examples:

**list-ref**: list indexing.

```scheme
(define (list-ref l n)
  (if (= 0 n)
      (first l)
      (list-ref (rest l) (- n 1))))
```

**length**: similar to Python built-in function `len`.

```scheme
(define (length xs)
  (if (null? xs)
      0
      (+ 1 (length (rest xs)))))
```

**map**: similar to Python built-in function `map`.

```scheme
(define (map proc xs)
  (if (null? xs)
      xs
      (cons (proc (first xs)) (map proc (rest xs)))))
```

**filter**: similar to Python built-in function `filter`.

```scheme
(define (filter proc xs)
  (cond ((null? xs) xs)
        ((proc (first xs)) (cons (first xs)
                                 (filter proc (rest xs))))
        (else (filter proc (rest xs)))))
```

