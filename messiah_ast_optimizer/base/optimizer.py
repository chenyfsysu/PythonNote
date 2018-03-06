# -*- coding:utf-8 -*-

import ast
import tokenize
import token


def GenerateStep(cls):
	return cls(cls.__tokenizer__(), cls.__visitor__(), cls.__transformer__())


def OptimizeStep(*stepcls):
	def _OptimizeStep(kclass):
		optimize_steps = [GenerateStep(cls) for cls in stepcls]
		tokenizer_steps = {}
		visit_steps = {}
		transform_steps = {}

		for step in optimize_steps:
			for attr, func in step._tokenizer_visitors.iteritems():
				tokenizer_steps.setdefault(attr, list())
				tokenizer_steps[attr].append(step)

			for attr, func in step._visit_visitors.iteritems():
				visit_steps.setdefault(attr, list())
				visit_steps[attr].append(step)

			for attr, func in step._transform_visitors.iteritems():
				transform_steps.setdefault(attr, list())
				transform_steps[attr].append(step)

		kclass._tokenizer_steps = tokenizer_steps
		kclass._visit_steps = visit_steps
		kclass._transform_steps = transform_steps
		kclass._optimize_steps = optimize_steps

		return kclass

	return _OptimizeStep


class MessiahNodeVisitor(ast.NodeVisitor):

	def genericVisit(self, node):
		for field, value in ast.iter_fields(node):
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
			elif isinstance(value, ast.AST):
				self.visit(value)

	def visit(self, node):
		key = node.__class__.__name__
		if key in self._visit_steps:
			return self.dispatchVisitCall(key, node)
		else:
			return self.genericVisit(node)

	def dispatchVisitCall(self, key, node):
		steps = self._visit_steps[key]
		for step in steps:
			step.visitCall(key, node)


class MessiahNodeTransformer(MessiahNodeVisitor):

	def generalTransform(self, node):
		for field, old_value in ast.iter_fields(node):
			old_value = getattr(node, field, None)
			if isinstance(old_value, list):
				new_values = []
				for value in old_value:
					if isinstance(value, ast.AST):
						value = self.transform(value)
						if value is None:
							continue
						elif not isinstance(value, ast.AST):
							new_values.extend(value)
							continue
					new_values.append(value)
				old_value[:] = new_values
			elif isinstance(old_value, ast.AST):
				new_node = self.transform(old_value)
				if new_node is None:
					delattr(node, field)
				else:
					setattr(node, field, new_node)
		return node

	def transform(self, node):
		key = node.__class__.__name__
		if key in self._transform_steps:
			return self.dispatchTransformCall(key, node)
		else:
			return self.generalTransform(node)

	def dispatchTransformCall(self, key, node):
		steps = self._transform_steps[key]
		for step in steps:
			node = step.visitTransform(key, node)

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
		self.dispatchTokenizeCall(key, token, srow_scol, erow_ecol, line)

	def dispatchTokenizeCall(self, key, token, srow_scol, erow_ecol, line):
		steps = self._tokenizer_steps[key]
		for step in steps:
			step.visitTokenize(key, token, srow_scol, erow_ecol, line)


class MessiahOptimizer(MessiahNodeTransformer, MessiahTokenizer):
	def __init__(self):
		super(MessiahOptimizer, self).__init__()

		self.executing_file = ''

	def executeTokenize(self, path, readline):
		self.executing_file = path
		self.tokenize(readline)

	def executeVisit(self, path, tree):
		pass

	def executeTransform(self, path, tree):
		pass

	def endTokenize(self):
		pass

	def endVisit(self):
		pass
