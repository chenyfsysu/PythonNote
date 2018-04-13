# -*- coding:utf-8 -*-

from astunparse.unparser import Unparser
from six.moves import cStringIO

import sys


class MessiahUnparser(Unparser):
	def __init__(self, tree, file=sys.stdout):
		self._comment = []
		Unparser.__init__(self, tree, file)

	def write(self, text):
		text == '\n' and self.writeComment()
		# self.f.write(text.decode('string_escape'))
		self.f.write(text)

	def fill(self, text=""):
		"Indent a piece of text, according to the current indentation level"
		self.writeComment()
		self.f.write("\n"+"    "*self._indent + text)

	def dispatch(self, tree):
		"Dispatcher function, dispatching tree type T to method _T."
		if isinstance(tree, list):
			for t in tree:
				self.dispatch(t)
			return

		comment = getattr(tree, '__comment__', '')
		if comment and comment not in self._comment:
			self._comment.append(comment)

		meth = getattr(self, "_"+tree.__class__.__name__)
		meth(tree)

	def _Module(self, node):
		Unparser._Module(self, node)
		self.writeComment()

	def writeComment(self):
		if self._comment:
			self.write('  #%s' % ' '.join(self._comment))
		self._comment = []


def unparse(tree, file=None):
	if not file:
		file = cStringIO()
	MessiahUnparser(tree, file=file)
