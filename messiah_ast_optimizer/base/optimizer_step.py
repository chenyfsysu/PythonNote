# -*- coding:utf-8 -*-


class MessiahBaseVisitorMeta(type):
	def __new__(mcls, name, bases, attrs):
		visitors = {}
		for base in bases:
			base_visitors = getattr(base, '_visitors', None)
			base_visitors and visitors.update(base._visitors)

		for key, func in attrs.iteritems():
			if key.startswith('visit_'):
				visitors[key[6:]] = func
		attrs['_visitors'] = visitors

		return super(MessiahBaseVisitorMeta, mcls).__new__(mcls, name, bases, attrs)


class MessiahBaseVisitor(object):
	__metaclass__ = MessiahBaseVisitorMeta

	def __init__(self):
		super(MessiahBaseVisitor, self).__init__()
		self.executing_file = ''

	def setupExecuting(self, file):
		self.executing_file = file

	def load(self):
		pass

	def dump(self):
		pass


class MessiahStepTokenizer(MessiahBaseVisitor):
	__skip__ = True


class MessiahStepVisitor(MessiahBaseVisitor):
	__skip__ = True

	def __init__(self):
		super(MessiahStepVisitor, self).__init__()

		self.tokenizer_data = None

	def load(self, tokenizer_data):
		self.tokenizer_data = tokenizer_data


class MessiahStepTransformer(MessiahBaseVisitor):
	def __init__(self):
		super(MessiahStepTransformer, self).__init__()

		self.tokenizer_data = None
		self.visitor_data = None

	def load(self, tokenizer_data, visitor_data):
		self.tokenizer_data = tokenizer_data
		self.visitor_data = visitor_data


class MessiahOptimizerStepMeta(type):
	def __new__(mcls, name, bases, attrs):
		tokenizer_visitors = {}
		visit_visitors = {}
		transform_visitors = {}

		for base in bases:
			base_tokenizer = getattr(base, '_tokenizer_visitors', None)
			base_tokenizer and tokenizer_visitors.update(base._tokenizer_visitors)

			base_visitors = getattr(base, '_visit_visitors', None)
			base_visitors and visit_visitors.update(base._visit_visitors)

			base_transformers = getattr(base, '_transform_visitors', None)
			base_transformers and transform_visitors.update(base._transform_visitors)

		for key, func in attrs['__tokenizer__']._visitors.iteritems():
			tokenizer_visitors[key] = func

		for key, func in attrs['__visitor__']._visitors.iteritems():
			visit_visitors[key] = func

		for key, func in attrs['__transformer__']._visitors.iteritems():
			transform_visitors[key] = func

		attrs['_visit_visitors'] = visit_visitors
		attrs['_transform_visitors'] = transform_visitors
		attrs['_tokenizer_visitors'] = tokenizer_visitors

		return super(MessiahOptimizerStepMeta, mcls).__new__(mcls, name, bases, attrs)


class MessiahOptimizerStep(object):
	__metaclass__ = MessiahOptimizerStepMeta

	__tokenizer__ = MessiahStepTokenizer
	__visitor__ = MessiahStepVisitor
	__transformer__ = MessiahStepTransformer


	def __init__(self, tokenizer, visitor, transformer):
		self.tokenizer = tokenizer
		self.visitor = visitor
		self.transformer = transformer

	def visitTokenize(self, key, token, srow_scol, erow_ecol, line):
		func = getattr(self.tokenizer, 'visit_%s' % key, None)
		func and func(token, srow_scol, erow_ecol, line)

	def visitCall(self, key, node):
		func = getattr(self.visitor, 'visit_%s' % key, None)
		func and func(node)

	def visitTransform(self, key, node):
		func = getattr(self.transformer, 'visit_%s' % key, None)
		return func(node)
