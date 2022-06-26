# Python ABC

[![Python 3.9.5](https://img.shields.io/badge/python-3.9.5-blue.svg)][1]

A python implementation of [the ABC Software metric][2]:

> The ABC software metric was introduced by Jerry Fitzpatrick in 1997 to overcome the drawbacks of the LOC. The metric defines an ABC score as a triplet of values that represent the size of a set of source code statements. An ABC score is calculated by counting the number of assignments (A), number of branches (B), and number of conditionals (C) in a program. ABC score can be applied to individual methods, functions, classes, modules or files within a program.

Fitzpatrick's original paper is, at the time of writing, only [available via the Wayback
Machine][3], so [a copy of it is included in this repo][4] as well.

The paper lists the counting rules for C, C++ and Java, so here are the rules this repo uses for
Python:

- Add one to the assignment count when:
  - Occurrence of an assignment operator (excluding default parameter assignments).
- Add one to the branch count when:
  - Occurrence of a function call/await or a class method call/await.
  - Occurrence of a class instantiation.
- Add one to the condition count when:
  - Occurrence of a conditional operator.
  - Occurrence of the following keywords: `else`, `elif`, `except`.
  - Occurrence of an `assert` statement without a conditional operator.

## Usage

Install the requirements in your virtual environment of choice, then you can see the command line
arguments that are available:

```bash
$ python -m python_abc --help
usage: python_abc [-h] [--debug DEBUG] [--sort SORT] [--verbose VERBOSE] path

A python implementation of the ABC Software metric: https://en.wikipedia.org/wiki/ABC_Software_Metric

positional arguments:
  path               path to directory or file

optional arguments:
  -h, --help         show this help message and exit
  --debug DEBUG      display AST output for each element in the parsed tree
  --sort SORT        sort files from highest to lowest magnitude
  --verbose VERBOSE  display marked-up file
```

Given `file.py` that contains the following text:

```python
if a and b:
    print(a)
else:
    print(b)

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
```

You can get the barebones output as follows:

```bash
$ python -m python_abc /path/to/file.py
/path/to/file.py         <1, 7, 10> (12.2)
```

Passing the `verbose` flag will give more detail:

```bash
$ python -m python_abc file.py --verbose=true
cc    | if a and b:
b     |     print(a)
c     | else:
b     |     print(b)
      |
abbcc | a = sum(i for i in range(1000) if i % 3 == 0 and i % 5 == 0)
      |
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
file.py          <1, 7, 10> (12.2)
```

If you want to inspect the abstract syntax tree for the file you can pass the `debug` flag, which
will print out each node from the tree and the vector that resulted from it.

The `path` argument can also be a path to a directory, in which case all Python files in that
directory (and its sub-directories) will be scanned, at which point it can be useful to pass the
`sort` flag to rank the files by ABC magnitude:

```bash
$ python -m python_abc . --sort
./calculate.py                              <18, 56, 23> (63.2)
./vector.py                                 <12, 23, 11> (28.2)
./main.py                                    <10, 23, 8> (26.3)
./tests/test_vector.py                       <4, 19, 10> (21.8)
./tests/__init__.py                           <4, 12, 1> (12.7)
./tests/test_radon_test_cases.py                <1, 2, 1> (2.4)
./tests/test_calculate_condition.py             <1, 2, 1> (2.4)
./tests/test_calculate_empty.py                 <1, 2, 1> (2.4)
./tests/test_calculate_assignment.py            <1, 2, 1> (2.4)
./tests/test_calculate_branch.py                <1, 2, 1> (2.4)
```

Finally you can pass a `cores` argument to tell the library how many CPU cores to use. By
default the library will try to use all the cores that are available on your machine.

[1]: https://www.python.org/downloads/release/python-395/
[2]: https://en.wikipedia.org/wiki/ABC_Software_Metric
[3]: https://web.archive.org/web/20210606115110/https://www.softwarerenovation.com/ABCMetric.pdf
[4]: https://github.com/eoinnoble/python-abc/blob/main/ABCMetric.pdf
