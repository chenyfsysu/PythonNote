# -*- coding:utf-8 -*-

import ast
import tokenize
import token

from collections import defaultdict
from context import Context
from context_visitor import ContextVisitor


def GenerateStep(cls):
	return cls(cls.__tokenizer__(), cls.__visitor__(), cls.__transformer__())


def OptimizeStep(*stepcls):
	def _OptimizeStep(kclass):
		optimize_steps = [GenerateStep(cls) for cls in stepcls]
		tokenizer_steps = defaultdict(list)
		visit_steps = defaultdict(list)
		transform_steps = defaultdict(list)
		self_visitors = {}
		full_visitors = {}

		for step in optimize_steps:
			for attr, func in step._tokenizer_visitors.iteritems():
				tokenizer_steps[attr].append(step)

			for attr, func in step._visit_visitors.iteritems():
				visit_steps[attr].append(step)

			for attr, func in step._transform_visitors.iteritems():
				transform_steps[attr].append(step)

		kclass._tokenizer_steps = tokenizer_steps
		kclass._visit_steps = visit_steps
		kclass._transform_steps = transform_steps
		kclass._optimize_steps = optimize_steps

		return kclass

	return _OptimizeStep


class MessiahNodeVisitor(ContextVisitor):

	def visit(self, node):
		self._generalVisitor = self._genericVisit
		self.context = Context()
		self._visit(node)
		
	def _visit(self, node):
		key = node.__class__.__name__
		if key in self._fullvisitors:
			visitors = self._fullvisitors[key]
			for visitor in visitors:
				visitor(self, node)
		else:
			self._genericVisit(node)

		if key in self._visit_steps:
			for step in self._visit_steps[key]:
				step.visit(key, node, self.context)

		if key in self._selfvisitors:
			for visitor in self._selfvisitors[key]:
				visitor(self, node)

	def _genericVisit(self, node):
		for field, value in ast.iter_fields(node):
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self._visit(item)
			elif isinstance(value, ast.AST):
				self._visit(value)


	def callVisitor(self, visitor, key, node):
		steps = self._visit_steps[key]
		for step in steps:
			step.visitCall(key, node)



class MessiahNodeTransformer(MessiahNodeVisitor):

	def transform(self, node):
		self._generalVisitor = self._generalTransform
		self.context = Context()
		return self._transform(node)

	def _transform(self, node):
		key = node.__class__.__name__
		if key in self._fullvisitors:
			visitors = self._fullvisitors[key]
			for visitor in visitors:
				node = visitor(self, node)
		else:
			node = self._generalTransform(node)

		if key in self._transform_steps:
			for step in self._transform_steps[key]:
				node = step.transform(key, node, self.context)

		if key in self._selfvisitors:
			for visitor in self._selfvisitors[key]:
				visitor(self, node)

		return node

	def _generalTransform(self, node):
		for field, old_value in ast.iter_fields(node):
			old_value = getattr(node, field, None)
			if isinstance(old_value, list):
				new_values = []
				for value in old_value:
					if isinstance(value, ast.AST):
						value = self._transform(value)
						if value is None:
							continue
						elif not isinstance(value, ast.AST):
							new_values.extend(value)
							continue
					new_values.append(value)
				old_value[:] = new_values
			elif isinstance(old_value, ast.AST):
				new_node = self._transform(old_value)
				if new_node is None:
					delattr(node, field)
				else:
					setattr(node, field, new_node)
		return node

	def callTransformers(self, key, node):
		steps = self._transform_steps[key]
		for step in steps:
			new_node = step.visitTransform(key, node)
			if type(new_node != node):
				return new_node
			node = new_node

		return node


class MessiahTokenizer(object):
	TokenMapping = {
		tokenize.COMMENT: 'Comment'
	}

	def tokenize(self, readline):
		tokenize.tokenize(readline, self.tokeneater)

	def tokeneater(self, type, token, srow_scol, erow_ecol, line):
		if type not in self.TokenMapping:
			return
		key = self.TokenMapping[type]
		if key in self._tokenizer_steps:
			self.dispatchTokenizeCall(key, token, srow_scol, erow_ecol, line)

	def dispatchTokenizeCall(self, key, token, srow_scol, erow_ecol, line):
		steps = self._tokenizer_steps[key]
		for step in steps:
			step.visitTokenize(key, token, srow_scol, erow_ecol, line)


class MessiahOptimizer(MessiahNodeTransformer, MessiahTokenizer):

	def executeTokenize(self, path, readline):
		for step in self._optimize_steps:
			step.tokenizer.setupExecuting(path)

		self.tokenize(readline)

	def executeVisit(self, path, tree):
		for step in self._optimize_steps:
			step.visitor.setupExecuting(path)
		self.visit(tree)

	def executeTransform(self, path, tree):
		for step in self._optimize_steps:
			step.transformer.setupExecuting(path)
		return self.transform(tree)

	def endTokenize(self):
		for step in self._optimize_steps:
			step.visitor.load(step.tokenizer.dump())

	def endVisit(self):
		for step in self._optimize_steps:
			step.transformer.load(step.tokenizer.dump(), step.visitor.dump())
