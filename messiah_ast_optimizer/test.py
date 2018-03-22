class Optimizer(object):
	def __init__(self):
		self.tokenize_data = {}
		self.visitor_data = {}


class Tokenizer(object):
	def __init__(self):
		pass

	def enter(self):
		"""執行tokenize"""
		pass

	def exit(self):
		"""退出tokenize"""
		pass


問題在於@Optimize在Meta之後！！！
 

TokenizeWalker
VisitWalker
TransformWalker
walker.walk(tokenizers)