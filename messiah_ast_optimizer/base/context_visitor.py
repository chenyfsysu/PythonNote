# -*- coding:utf-8 -*-

import ast
import utils
import const

from base import NodeVisitor
from context import Context, Definition, Namespace


class ContextVisitor(NodeVisitor):

    def __init__(self):
        super(ContextVisitor, self).__init__()
        self.context = Context()
        self._generalVisitor = None

    def visitDefinitionBlock(self, node):
        context = self.context
        definitions = Definition.create(node)
        context.addDefinition(definitions)
        context.frames.append(definitions.values()[0])
        context.locals_stack.append(Namespace())
        
        node = self._generalVisitor(node)

        context.frames.pop()
        context.locals_stack.pop()

        return node

    def visitClosureBlock(self, node):
        self.context.locals_stack.append(Namespace())
        node = self._generalVisitor(node)
        self.context.locals_stack.pop()

        return node

    def visitDefinition(self, node):
        self.context.addDefinition(Definition.create(node))

    def fullvisit_Module(self, node):
        self.context.frames.append(Definition.create(node).values()[0])
        self.context.locals_stack.append(Namespace())
        return self._generalVisitor(node)

    def fullvisit_ClassDef(self, node):
        return self.visitDefinitionBlock(node)

    def fullvisit_FunctionDef(self, node):
        return self.visitDefinitionBlock(node)

    def fullvisit_DictComp(self, node):
        return self.visitClosureBlock(node)

    def fullvisit_ListComp(self, node):
        return self.visitClosureBlock(node)

    def fullvisit_SetComp(self, node): 
        return self.visitClosureBlock(node)

    def fullvisit_GeneratorExp(self, node):
        return self.visitClosureBlock(node)

    def fullvisit_Lambda(self, node):
        return  self.visitClosureBlock(node)

    def visit_Assign(self, node):
        self.visitDefinition(node)
        return node

    def visit_AugAssign(self, node):
        self.context.setDefinition(node.target, const.UNKNOW)
        return node

    def visit_For(self, node):
        return node

    def visit_Import(self, node):
        self.visitDefinition(node)
        return node

    def visit_ImportFrom(self, node):
        self.visitDefinition(node)
        return node

    def visit_Delete(self, node):
        locals_attr = self.context.locals
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in locals_attr:
                del locals_attr[target.id]
        return node
