import pytest

from tests import assert_source_returns_expected

# These test cases were taken from the Radon package test suite, with overlapping ones removed
# It's very useful to have some tests that were written by other people!
# https://github.com/rubik/radon/blob/master/radon/tests/test_complexity_visitor.py

RADON_CASES = [
    (
        """\
        if a: pass
        elif b: pass
        """,
        """\
        c  | if a: pass
        cc | elif b: pass
        """,
    ),
    (
        """\
        if a and b:
            pass
        elif c and d:
            pass
        else:
            pass
        """,
        """\
        cc  | if a and b:
            |     pass
        ccc | elif c and d:
            |     pass
        c   | else:
            |     pass
        """,
    ),
    (
        """\
        if a and b or c and d:
            pass
        else:
            pass
        """,
        """\
        cccc | if a and b or c and d:
             |     pass
        c    | else:
             |     pass
        """,
    ),
    (
        """\
        if a and b or c:
            pass
        else:
            pass
        """,
        """\
        ccc | if a and b or c:
            |     pass
        c   | else:
            |     pass
        """,
    ),
    ("for x in range(10): print(x)", "bb | for x in range(10): print(x)"),
    ("while a < 4: pass", "c | while a < 4: pass"),
    ("while a < 4 and b < 42: pass", "cc | while a < 4 and b < 42: pass"),
    (
        "with open('raw.py') as fobj: print(fobj.read())",
        "bbb | with open('raw.py') as fobj: print(fobj.read())",
    ),
    ("[i for i in range(4) if i&1]", "b | [i for i in range(4) if i&1]"),
    ("k = lambda a, b, c: c if a else b", "acc | k = lambda a, b, c: c if a else b"),
    (
        "v = a if sum(i for i in xrange(c)) < 10 else c",
        "abbcc | v = a if sum(i for i in xrange(c)) < 10 else c",
    ),
    (
        """\
        for i in range(10):
            print(i)
        else:
            print('wah')
            print('really not found')
            print(3)
        """,
        """\
        b | for i in range(10):
        b |     print(i)
        c | else:
        b |     print('wah')
        b |     print('really not found')
        b |     print(3)
        """,
    ),
    ("assert i < 0", "c | assert i < 0"),
    (
        """\
        def f(a, b, c):
            if a and b == 4:
                return c ** c
            elif a and not c:
                return sum(i for i in range(41) if i&1)
            return a + b
        """,
        """\
            | def f(a, b, c):
        cc  |     if a and b == 4:
            |         return c ** c
        ccc |     elif a and not c:
        bb  |         return sum(i for i in range(41) if i&1)
            |     return a + b
        """,
    ),
    (
        """\
        if a and not b:
            pass
        elif b or c:
            pass
        else:
            pass
        for i in range(4):
            print(i)
        def g(a, b):
            while a < b:
                b, a = a **2, b ** 2
            return b
        """,
        """\
        cc  | if a and not b:
            |     pass
        ccc | elif b or c:
            |     pass
        c   | else:
            |     pass
        b   | for i in range(4):
        b   |     print(i)
            | def g(a, b):
        c   |     while a < b:
        aa  |         b, a = a **2, b ** 2
            |     return b
        """,
    ),
    (
        """\
        while a**b:
            a, b = b, a * (b - 1)
            if a and b:
                b = 0
            else:
                b = 1
        return sum(i for i in range(b))
        """,
        """\
           | while a**b:
        aa |     a, b = b, a * (b - 1)
        cc |     if a and b:
        a  |         b = 0
        c  |     else:
        a  |         b = 1
        bb | return sum(i for i in range(b))
        """,
    ),
    (
        """\
        def f(a, b):
            return a if b else 2
        def g(a, b, c):
            if a and b:
                return a / b + b / a
            elif b and c:
               return b / c - c / b
            return a + b + c
        def h(a, b):
            return 2 * (a + b)
        """,
        """\
            | def f(a, b):
        cc  |     return a if b else 2
            | def g(a, b, c):
        cc  |     if a and b:
            |         return a / b + b / a
        ccc |     elif b and c:
            |        return b / c - c / b
            |     return a + b + c
            | def h(a, b):
            |     return 2 * (a + b)
        """,
    ),
    (
        """\
        def f(p, q):
            while p:
                p, q = q, p - q
            if q < 1:
                return 1 / q ** 2
            elif q > 100:
                return 1 / q ** .5
            return 42 if not q else p
        def g(a, b, c):
            if a and b or a - b:
                return a / b - c
            elif b or c:
                return 1
            else:
                k = 0
                with open('results.txt', 'w') as fobj:
                    for i in range(b ** c):
                        k += sum(1 / j for j in range(i ** 2) if j > 2)
                    fobj.write(str(k))
                return k - 1
        """,
        """\
             | def f(p, q):
             |     while p:
        aa   |         p, q = q, p - q
        c    |     if q < 1:
             |         return 1 / q ** 2
        cc   |     elif q > 100:
             |         return 1 / q ** .5
        cc   |     return 42 if not q else p
             | def g(a, b, c):
        ccc  |     if a and b or a - b:
             |         return a / b - c
        ccc  |     elif b or c:
             |         return 1
        c    |     else:
        a    |         k = 0
        b    |         with open('results.txt', 'w') as fobj:
        b    |             for i in range(b ** c):
        abbc |                 k += sum(1 / j for j in range(i ** 2) if j > 2)
        bb   |             fobj.write(str(k))
             |         return k - 1
        """,
    ),
    (
        """\
        class A(object):
            def m(self, a, b):
                if not a or b:
                    return b - 1
                try:
                    return a / b
                except ZeroDivisionError:
                    return a
            def n(self, k):
                while self.m(k) < k:
                    k -= self.m(k ** 2 - min(self.m(j) for j in range(k ** 4)))
                return k
        """,
        """\
              | class A(object):
              |     def m(self, a, b):
        cc    |         if not a or b:
              |             return b - 1
              |         try:
              |             return a / b
        c     |         except ZeroDivisionError:
              |             return a
              |     def n(self, k):
        bc    |         while self.m(k) < k:
        abbbb |             k -= self.m(k ** 2 - min(self.m(j) for j in range(k ** 4)))
              |         return k
        """,
    ),
    (
        """\
        class B(object):
            ATTR = 9 if A().n(9) == 9 else 10
            import sys
            if sys.version_info >= (3, 3):
                import os
                AT = os.openat('/random/loc')
            def __iter__(self):
                return __import__('itertools').tee(B.__dict__)
            def test(self, func):
                a = func(self.ATTR, self.AT)
                if a < self.ATTR:
                    yield self
                elif a > self.ATTR ** 2:
                    yield self.__iter__()
                yield iter(a)
        """,
        """\
              | class B(object):
        abbcc |     ATTR = 9 if A().n(9) == 9 else 10
              |     import sys
        c     |     if sys.version_info >= (3, 3):
              |         import os
        ab    |         AT = os.openat('/random/loc')
              |     def __iter__(self):
        bb    |         return __import__('itertools').tee(B.__dict__)
              |     def test(self, func):
        ab    |         a = func(self.ATTR, self.AT)
        c     |         if a < self.ATTR:
              |             yield self
        cc    |         elif a > self.ATTR ** 2:
        b     |             yield self.__iter__()
        b     |         yield iter(a)
        """,
    ),
    (
        """\
        if a and b:
            print
        else:
            print
        a = sum(i for i in range(1000) if i % 3 == 0 and i % 5 == 0)
        def f(n):
            def inner(n):
                return n ** 2
            if n == 0:
                return 1
            elif n == 1:
                return n
            elif n < 5:
                return (n - 1) ** 2
            return n * pow(inner(n), f(n - 1), n - 3)
        """,
        """\
        cc    | if a and b:
              |     print
        c     | else:
              |     print
        abbcc | a = sum(i for i in range(1000) if i % 3 == 0 and i % 5 == 0)
              | def f(n):
              |     def inner(n):
              |         return n ** 2
        c     |     if n == 0:
              |         return 1
        cc    |     elif n == 1:
              |         return n
        cc    |     elif n < 5:
              |         return (n - 1) ** 2
        bbb   |     return n * pow(inner(n), f(n - 1), n - 3)
        """,
    ),
    (
        """\
        try:
            1 / 0
        except ZeroDivisonError:
            print
        except TypeError:
            pass
        class J(object):
            def aux(self, w):
                if w == 0:
                    return 0
                return w - 1 + sum(self.aux(w - 3 - i) for i in range(2))
        def f(a, b):
            def inner(n):
                return n ** 2
            if a < b:
                b, a = a, inner(b)
            return a, b
        """,
        """\
            | try:
            |     1 / 0
        c   | except ZeroDivisonError:
            |     print
        c   | except TypeError:
            |     pass
            | class J(object):
            |     def aux(self, w):
        c   |         if w == 0:
            |             return 0
        bbb |         return w - 1 + sum(self.aux(w - 3 - i) for i in range(2))
            | def f(a, b):
            |     def inner(n):
            |         return n ** 2
        c   |     if a < b:
        aab |         b, a = a, inner(b)
            |     return a, b
        """,
    ),
    (
        """\
        def f(n):
            def g(l):
                return l ** 4
            def h(i):
                return i ** 5 + 1 if i & 1 else 2
            return sum(g(u + 4) / float(h(u)) for u in range(2, n))
        """,
        """\
              | def f(n):
              |     def g(l):
              |         return l ** 4
              |     def h(i):
        cc    |         return i ** 5 + 1 if i & 1 else 2
        bbbbb |     return sum(g(u + 4) / float(h(u)) for u in range(2, n))
        """,
    ),
    (
        """\
        def memoize(func):
            cache = {}
            def aux(*args, **kwargs):
                key = (args, kwargs)
                if key in cache:
                    return cache[key]
                cache[key] = res = func(*args, **kwargs)
                return res
            return aux
        """,
        """\
            | def memoize(func):
        a   |     cache = {}
            |     def aux(*args, **kwargs):
        a   |         key = (args, kwargs)
        c   |         if key in cache:
            |             return cache[key]
        aab |         cache[key] = res = func(*args, **kwargs)
            |         return res
            |     return aux
        """,
    ),
]


@pytest.mark.parametrize("source,expected", RADON_CASES)
def test_radon(capsys, source, expected):
    assert_source_returns_expected(capsys, source, expected) is True
