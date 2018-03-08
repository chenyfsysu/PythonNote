# -*- coding:utf-8 -*-

from astunparse.unparser import Unparser
from six.moves import cStringIO

import sys


class MessiahUnparser(Unparser):
	def __init__(self, tree, file=sys.stdout):
		self._comment = ''
		Unparser.__init__(self, tree, file)

	def fill(self, text = ""):
		"Indent a piece of text, according to the current indentation level"
		if self._comment:
			self.write(' # %s' % self._comment)

		self._comment = ''
		self.f.write("\n"+"    "*self._indent + text)

	def dispatch(self, tree):
		"Dispatcher function, dispatching tree type T to method _T."
		if isinstance(tree, list):
			for t in tree:
				self.dispatch(t)
			return

		comment = getattr(tree, '__comment__', '')
		if comment:
			self._comment = ' '.join([self._comment, comment])

		meth = getattr(self, "_"+tree.__class__.__name__)
		meth(tree)


def unparse(tree):
    v = cStringIO()
    MessiahUnparser(tree, file=v)
    return v.getvalue()
