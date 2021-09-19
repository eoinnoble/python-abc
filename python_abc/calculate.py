import ast
from functools import singledispatch
from typing import List, Union

from python_abc import vector


@singledispatch
def calculate_abc_for_node(node_class: ast.AST) -> List[vector.Vector]:
    """Used by default"""
    return [vector.empty(node_class)]


def handle_else(
    node_class: Union[ast.For, ast.If, ast.IfExp, ast.Try, ast.While]
) -> vector.Vector:
    """The code in an elif/else block does not have the lineno of the elif/else statement, so
    if we want to accurately decorate the line then we need to manually adjust the lineno

    This relies on the code following PEP-8, and will notably fall down with code like this:
        while True: pass
        else: pass

    We assume that second `pass` will be on the line _after_ the `else` statement.
    """
    if not getattr(node_class, "orelse", None):
        return vector.empty(node_class)

    if isinstance(node_class.orelse, list):
        node = node_class.orelse[0]  # type: ast.AST
    else:
        node = node_class.orelse

    if not isinstance(node, ast.If):
        lineno = node.lineno - 1 if node.lineno != node_class.lineno else node.lineno
    else:
        lineno = node.lineno

    return vector.condition(node, lineno)


# Node classes that do not, of themselves, contribute to any particular count, but may have
# components that do, and so need to be decomposed
@calculate_abc_for_node.register
def ast_for(node_class: ast.For):
    return [handle_else(node_class)]


@calculate_abc_for_node.register
def ast_while(node_class: ast.While):
    return [handle_else(node_class)]


# Syntax contributing to assignment count
@calculate_abc_for_node.register
def ast_assign(node_class: ast.Assign):
    vectors = []
    for target in node_class.targets:
        if isinstance(target, ast.Tuple):
            # This is likely assignment by destructuring
            for elt in target.elts:
                vectors.append(vector.assignment(elt))
        else:
            vectors.append(vector.assignment(target))

    return vectors


@calculate_abc_for_node.register
def ast_annassign(node_class: ast.AnnAssign):
    return [vector.assignment(node_class)]


@calculate_abc_for_node.register
def ast_augassign(node_class: ast.AugAssign):
    return [vector.assignment(node_class)]


# Syntax contributing to branch count
@calculate_abc_for_node.register
def ast_call(node_class: ast.Call):
    return [vector.branch(node_class)]


# Syntax contributing to condition count
@calculate_abc_for_node.register
def ast_boolop(node_class: ast.BoolOp):
    return [
        vector.condition(v)
        for v in node_class.values
        if not isinstance(v, (ast.BoolOp, ast.Compare))
    ] or [vector.empty(node_class)]


@calculate_abc_for_node.register
def ast_compare(node_class: ast.Compare):
    return [vector.condition(node_class)]


@calculate_abc_for_node.register
def ast_excepthandler(node_class: ast.ExceptHandler):
    return [vector.condition(node_class)]


@calculate_abc_for_node.register
def ast_if(node_class: ast.If):
    if not isinstance(node_class.test, (ast.BoolOp, ast.Compare, ast.Constant)):
        # This is essentially saying `if variable is True`, so we should count it as such
        return [vector.condition(node_class.test), handle_else(node_class)]
    else:
        return [handle_else(node_class)]


@calculate_abc_for_node.register
def ast_ifexp(node_class: ast.IfExp):
    if not isinstance(node_class.test, (ast.BoolOp, ast.Compare, ast.Constant)):
        # This is essentially saying `if variable is True`, so we should count it as such
        return [vector.condition(node_class.test), handle_else(node_class)]
    else:
        return [handle_else(node_class)]


@calculate_abc_for_node.register
def ast_try(node_class: ast.Try):
    # `except` clauses are handled by `ast_excepthandler`
    # `finalbody` is always executed so no need to count it
    return [handle_else(node_class)]


@calculate_abc_for_node.register
def ast_assert(node_class: ast.Assert):
    if isinstance(node_class.test, ast.Name):
        # This is a tacit conditional like `assert a`
        return [vector.condition(node_class.test)]
    else:
        return [vector.empty(node_class)]


def calculate_abc(
    source: str, debug: bool = False, verbose: bool = False
) -> vector.Vector:
    final_vector = vector.Vector(0, 0, 0)

    source_split = source.split("\n")
    temp = {
        lineno: {"decoration": ""} for lineno, _ in enumerate(source_split, start=1)
    }

    tree = ast.parse(source)
    if debug:
        print(ast.dump(tree, indent=4), end="\n\n")

    print_lines = []
    for node in ast.walk(tree):
        temp_vectors = calculate_abc_for_node(node)

        if debug:
            print_lines.append((getattr(node, "lineno", 0), temp_vectors, node))

        for v in temp_vectors:
            if lineno := getattr(v, "lineno", 0):
                final_vector += v
                temp[lineno]["decoration"] += v.as_notation

    if debug:
        # ast.walk doesn't have a specific order, but for debugging purposes it's much
        # easier to have the vectors ordered by line number
        print_lines.sort(key=lambda x: x[0])
        for lineno, vectors, node in print_lines:
            if any(vectors):
                print_line = f"Line {lineno} -> {vectors}"
                print_node = f"{ast.dump(node, indent=4)}"
                print(print_line + "\n" + print_node + "\n")

    if verbose:
        decoration_length = max(len(line["decoration"]) for line in temp.values())
        decorated_text = zip(
            [line["decoration"] for line in temp.values()], source_split
        )
        for decoration, line in decorated_text:
            decoration = "".join(sorted(decoration))
            print(
                f"{decoration:<{decoration_length}} | {line:<{88 - decoration_length - 3}}"
            )

    return final_vector
