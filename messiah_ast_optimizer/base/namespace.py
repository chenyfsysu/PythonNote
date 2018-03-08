class NamespaceStep(OptimizerStep):
    def fullvisit_FunctionDef(self, node):
        self.namespace.set(node.name, UNSET)
        global _fndefs
        _fndefs[node.name] = node

    def fullvisit_AsyncFunctionDef(self, node):
        self.namespace.set(node.name, UNSET)

    def fullvisit_ClassDef(self, node):
        self.namespace.set(node.name, UNSET)

    def _namespace_set(self, node, value, unset=False):
        if value is not UNSET:
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                names = (node.id,)
            else:
                names = get_ast_names(node)
                value = UNSET
        else:
            names = get_ast_names(node)

        if names is None:
            if self.namespace.enter_unknown_state():
                self.log(node,
                         "enter unknown namespace state: "
                         "don't support assignment %s",
                         compact_dump(node))
            return False

        for name in names:
            if unset:
                self.namespace.unset(name)
            else:
                self.namespace.set(name, value)
        return True

    def visit_Assign(self, node):
        value = get_constant(node.value)
        for target in node.targets:
            if not self._namespace_set(target, value):
                break

    def visit_AugAssign(self, node):
        self._namespace_set(node.target, UNSET)

    def visit_For(self, node):
        self._namespace_set(node.target, UNSET)

    def _visit_Import(self, node):
        for modname in node.names:
            if modname.asname:
                name = modname.asname
            else:
                name = modname.name
                # replace 'os.path' with 'os'
                name = name.split('.', 1)[0]
            self.namespace.set(name, UNSET)

    def visit_Import(self, node):
        self._visit_Import(node)

    def visit_ImportFrom(self, node):
        self._visit_Import(node)

    def visit_withitem(self, node):
        if node.optional_vars is not None:
            self._namespace_set(node.optional_vars, UNSET)

    def visit_Delete(self, node):
        for target in node.targets:
            if not self._namespace_set(target, UNSET, unset=True):
                break
