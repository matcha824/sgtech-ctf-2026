import sys
import ast
import builtins
import keyword
import re
import base64
import random
import string


def _make_random_name(used_names: set[str]) -> str:
    while True:
        candidate = "_" + "".join(random.choices(string.ascii_lowercase, k=8))
        if candidate not in used_names:
            used_names.add(candidate)
            return candidate


def _replace_imports(module: ast.Module) -> ast.Module:
    used_names = {node.id for node in ast.walk(module) if isinstance(node, ast.Name)}

    import_bindings: list[tuple[str, str, str]] = []
    retained_body: list[ast.stmt] = []

    for statement in module.body:
        if not isinstance(statement, ast.Import):
            retained_body.append(statement)
            continue

        for imported_name in statement.names:
            bound_name = imported_name.asname or imported_name.name.split(".", 1)[0]
            import_bindings.append(
                (bound_name, _make_random_name(used_names), imported_name.name)
            )

    if not import_bindings:
        return module

    replacement_names = {
        bound_name: random_name for bound_name, random_name, _ in import_bindings
    }

    class ImportedNameRewriter(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.AST:
            if (
                isinstance(node.ctx, (ast.Load, ast.Del))
                and node.id in replacement_names
            ):
                return ast.copy_location(
                    ast.Name(id=replacement_names[node.id], ctx=node.ctx),
                    node,
                )
            return node

    module.body = retained_body
    module = ImportedNameRewriter().visit(module)

    import_assignments = [
        ast.Assign(
            targets=[ast.Name(id=random_name, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id="__import__", ctx=ast.Load()),
                args=[ast.Constant(value=module_name)],
                keywords=[],
            ),
        )
        for _, random_name, module_name in import_bindings
    ]

    insert_at = (
        1
        if (
            module.body
            and isinstance(module.body[0], ast.Expr)
            and isinstance(module.body[0].value, ast.Constant)
            and isinstance(module.body[0].value.value, str)
        )
        else 0
    )
    module.body[insert_at:insert_at] = import_assignments
    ast.fix_missing_locations(module)
    return module


def _replace_names(module: ast.Module) -> ast.Module:
    builtin_names = set(dir(builtins))
    reserved_names = builtin_names | set(keyword.kwlist) | {"__name__", "__import__"}
    used_names = {node.id for node in ast.walk(module) if isinstance(node, ast.Name)}
    rename_table: dict[str, str] = {}

    def is_renamable(name: str) -> bool:
        return name not in reserved_names and not (
            name.startswith("__") and name.endswith("__")
        )

    def assign_name(name: str) -> None:
        if is_renamable(name) and name not in rename_table:
            rename_table[name] = _make_random_name(used_names)

    for node in ast.walk(module):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            assign_name(node.name)
        elif isinstance(node, ast.arg):
            assign_name(node.arg)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            assign_name(node.id)
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
            assign_name(node.attr)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            assign_name(node.name)

    class NameRewriter(ast.NodeTransformer):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
            self.generic_visit(node)
            node.name = rename_table.get(node.name, node.name)
            return node

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
            self.generic_visit(node)
            node.name = rename_table.get(node.name, node.name)
            return node

        def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:
            self.generic_visit(node)
            node.name = rename_table.get(node.name, node.name)
            return node

        def visit_arg(self, node: ast.arg) -> ast.AST:
            node.arg = rename_table.get(node.arg, node.arg)
            return node

        def visit_Name(self, node: ast.Name) -> ast.AST:
            node.id = rename_table.get(node.id, node.id)
            return node

        def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
            self.generic_visit(node)
            node.attr = rename_table.get(node.attr, node.attr)
            return node

        def visit_Global(self, node: ast.Global) -> ast.AST:
            node.names = [rename_table.get(name, name) for name in node.names]
            return node

        def visit_Nonlocal(self, node: ast.Nonlocal) -> ast.AST:
            node.names = [rename_table.get(name, name) for name in node.names]
            return node

        def visit_ExceptHandler(self, node: ast.ExceptHandler) -> ast.AST:
            self.generic_visit(node)
            if node.name:
                node.name = rename_table.get(node.name, node.name)
            return node

    module = NameRewriter().visit(module)
    ast.fix_missing_locations(module)
    return module


def _replace_literals(module: ast.Module) -> ast.Module:
    used_names = {node.id for node in ast.walk(module) if isinstance(node, ast.Name)}
    table_name = _make_random_name(used_names)
    literal_table: dict[tuple[type, int | str | bytes], str] = {}
    parent_map = {
        child: parent
        for parent in ast.walk(module)
        for child in ast.iter_child_nodes(parent)
    }

    def is_docstring(node: ast.Constant) -> bool:
        parent = parent_map.get(node)
        if not isinstance(parent, ast.Expr) or parent.value is not node:
            return False

        owner = parent_map.get(parent)
        if not isinstance(
            owner,
            (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
        ):
            return False

        return bool(owner.body) and owner.body[0] is parent

    def is_f_string_part(node: ast.Constant) -> bool:
        current = parent_map.get(node)
        while current is not None:
            if isinstance(current, ast.JoinedStr):
                return True
            current = parent_map.get(current)
        return False

    def assign_literal_name(value: int | str | bytes) -> str:
        key = (type(value), value)
        if key not in literal_table:
            literal_table[key] = _make_random_name(used_names)
        return literal_table[key]

    class LiteralRewriter(ast.NodeTransformer):
        def visit_Constant(self, node: ast.Constant) -> ast.AST:
            value = node.value
            if isinstance(value, bool) or value is None:
                return node

            if not isinstance(value, (int, str, bytes)):
                return node

            if is_docstring(node) or is_f_string_part(node):
                return node

            literal_name = assign_literal_name(value)
            return ast.copy_location(
                ast.Subscript(
                    value=ast.Name(id=table_name, ctx=ast.Load()),
                    slice=ast.Constant(value=literal_name),
                    ctx=ast.Load(),
                ),
                node,
            )

    module = LiteralRewriter().visit(module)

    if not literal_table:
        return module

    table_assignment = ast.Assign(
        targets=[ast.Name(id=table_name, ctx=ast.Store())],
        value=ast.Dict(
            keys=[
                ast.Constant(value=literal_name)
                for literal_name in literal_table.values()
            ],
            values=[ast.Constant(value=value) for _, value in literal_table],
        ),
    )

    insert_at = (
        1
        if (
            module.body
            and isinstance(module.body[0], ast.Expr)
            and isinstance(module.body[0].value, ast.Constant)
            and isinstance(module.body[0].value.value, str)
        )
        else 0
    )
    module.body.insert(insert_at, table_assignment)
    ast.fix_missing_locations(module)
    return module


def obfuscate(source_file: str) -> None:
    with open(source_file, "r") as f:
        source_code_ast = ast.parse(f.read())

    source_code_ast = _replace_imports(source_code_ast)
    source_code_ast = _replace_names(source_code_ast)
    source_code_ast = _replace_literals(source_code_ast)
    source_code = ast.unparse(source_code_ast)
    encoded_source = base64.b64encode(source_code.encode()).decode()
    source_code = (
        "import base64\n" f"exec(base64.b64decode({encoded_source!r}).decode())\n"
    )

    with open("dist.py", "w") as f:
        f.write(source_code)


if __name__ == "__main__":
    source_file = sys.argv[1]
    obfuscate(source_file)
