from functools import reduce
from collections import ChainMap

def parse(text):
    parts = text.replace('(', ' ( ').replace(')', ' ) ').split()
    new_parts = []
    for part in parts:
        try:
            float(part)
        except ValueError:
            part = part if part in '()' else repr(part)
        new_parts.append(part)
    py_text = ','.join(new_parts).replace('(,', '(')
    return eval(py_text)

class Interpreter:
    def __init__(self):
        self.env = ChainMap(self.init_library)

    def __call__(self, text):
        return self.eval(parse(text))

    @property
    def init_library(self):
        library = {'+': lambda *args: sum(map(self.eval, args)),
                   '-': lambda *args: reduce(lambda x, y: x - y, map(self.eval, args)),
                   '*': lambda *args: reduce(lambda x, y: x * y, map(self.eval, args)),
                   '/': lambda *args: reduce(lambda x, y: x / y, map(self.eval, args)),
                   'true': True,
                   'false': False,
                   '<=': lambda x, y: self.eval(x) <= self.eval(y),
                   '>=': lambda x, y: self.eval(x) >= self.eval(y),
                   '<': lambda x, y: self.eval(x) < self.eval(y),
                   '>': lambda x, y: self.eval(x) > self.eval(y),
                   '=': lambda x, y: self.eval(x) == self.eval(y),
                   'and': lambda *args: all(map(self.eval, args)),
                   'or': lambda *args: any(map(self.eval, args)),
                   'not': lambda x: not self.eval(x),
                   'if': lambda cond, true, false: self.eval(true) if self.eval(cond) else self.eval(false),
                   'define': self.define,
                   'lambda': lambda params, *exprs: Procedure(params, exprs, self),
                   'display': lambda *args: print(*map(self.eval, args)),
                   'cons': lambda first, rest: (self.eval(first), self.eval(rest)),
                   'first': lambda pair: pair[0],
                   'rest': lambda pair: pair[1],
                   'list': lambda *args: [*map(self.eval, args)],
                   'empty?': lambda l: bool(l),
                   'none': None,
                   'none?': lambda x: self.eval(x) is None,
                   'let': self.let,
                   }
        for key, value in library.items():
            try:
                value.__qualname__ = key
            except AttributeError:
                pass
        return library

    def define(self, *args):
        name, *exprs = args
        if isinstance(name, tuple):
            name, *params = name
            self.env[name] = Procedure(params, exprs, self)
        else:
            if len(exprs) > 1:
                raise TypeError('argument length mismatch')
            self.env[name] = self.eval(exprs[0])

    def let(self, assignments, *body):
        params, exprs = zip(*assignments)
        proc = Procedure(params, body, self)
        return proc(*(self.eval(expr) for expr in exprs))

    def eval(self, token):
        if isinstance(token, (int, float)):
            return token
        if isinstance(token, str):
            return self.env[token]
        return self.eval(token[0])(*token[1:])

    def repl(self):
        while True:
            line_buffer = []
            nested = 0
            try:
                while True:
                    text = input('> ' if not nested else '  ')
                    nested += text.count('(') - text.count(')')
                    line_buffer.append(text)
                    if nested == 0:
                        break
                try:
                    result = self(' '.join(line_buffer))
                    if result is not None:
                        print(result)
                except Exception as e:
                    print(f"{e.__class__.__name__}: {e}")
            except EOFError:
                print()
                break

class Procedure:
    def __init__(self, params, exprs, interp):
        self.params = params
        self.exprs = exprs
        self.interp = interp

    def __call__(self, *args):
        old_env = self.interp.env
        self.interp.env = self.interp.env.new_child()
        if len(args) != len(self.params):
            raise TypeError('argument length mismatch')
        try:
            for param, arg in zip(self.params, args):
                self.interp.env[param] = self.interp.eval(arg)
            result = None
            for expr in self.exprs:
                result = self.interp.eval(expr)
        finally:
            self.interp.env = old_env
        return result

    def __repr__(self):
        return f'<Procedure {self.params}>'

if __name__ == '__main__':
    import readline
    interp = Interpreter()
    print('[scheme]')
    interp.repl()

