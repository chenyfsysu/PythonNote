
# -*- coding:utf-8 -*-

import ast

from base import NodeVisitor


class Namespace(object):
    pass


class NamespaceVisitor(NodeVisitor):

    def __init__(self):
        super(NamespaceVisitor, self).__init__()
        self.namespaces = []


    def setNamespace(self, node, value):
        pass

    def fullvisit_FunctionDef(self, node):
        self.enterSubNamespace(node)

    def fullvisit_ClassDef(self, node):
        self.enterSubNamespace(node)

    def fullvisit_DictComp(self, node):
        self.enterSubNamespace(node)

    def fullvisit_ListComp(self, node):
        self.enterSubNamespace(node)

    def fullvisit_SetComp(self, node):
        self.enterSubNamespace(node)

    def fullvisit_GeneratorExp(self, node):
        self.enterSubNamespace(node)

    def fullvisit_Lambda(self, node):
        self.enterSubNamespace(node)

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

    def enterSubNamespace(node):
        self.namespaces.append(Namespace())
        node = self.generalVisit(node)
        self.namespaces.pop()

        return node
