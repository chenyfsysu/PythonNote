# -*- coding:utf-8 -*-

import ast
import utils
import const
from collections import defaultdict


class VisitorMeta(type):
	def __new__(mcls, name, bases, attrs):
		visitors = defaultdict(list)
		fullvisitors = defaultdict(list)
		for base in bases:
			base_visitors = getattr(base, '_visitors', None)
			base_visitors and visitors.update(base._visitors)
			base_fullvisitors = getattr(base, '_fullvisitors', None)
			base_fullvisitors and fullvisitors.update(base._fullvisitors)

		for key, func in attrs.iteritems():
			if key.startswith('visit_'):
				visitors[key].append(key)
			elif key.startswith('fullvisit_'):
				fullvisitors[key].append(key)

		attrs['_visitors'] = visitors
		attrs['_fullvisitors'] = fullvisitors

		return super(VisitorMeta, mcls).__new__(mcls, name, bases, attrs)


class IVisitor(object):
	__metaclass__ = VisitorMeta

	def __init__(self, optimizer=None):
		self.optimizer = optimizer


class NodeVisitor(IVisitor, ast.NodeVisitor):
	pass


class MessiahStepTokenizer(IVisitor):
	pass


class MessiahStepVisitor(NodeVisitor):
	pass



class MessiahStepTransformer(NodeVisitor):
	pass


class MessiahOptimizerStep(object):

	def __init__(self, tokenizer=None, visitor=None, transformer=None):
		self.tokenizer = tokenizer
		self.visitor = visitor
		self.transformer = transformer
