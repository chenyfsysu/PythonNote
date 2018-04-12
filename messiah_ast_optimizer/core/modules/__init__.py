# -*- coding:utf-8 -*-

import builtin
import standard
import engine


def setup(loader):
	builtin.setup(loader)
	standard.setup(loader)
	engine.setup(loader)
