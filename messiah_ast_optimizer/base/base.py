# -*- coding:utf-8 -*-

import ast
from collections import defaultdict


class VisitorMeta(type):
    def __new__(mcls, name, bases, attrs):
        visitors = defaultdict(list)
        fullvisitors = defaultdict(list)
        for base in bases:
            base_visitors = getattr(base, '_selfvisitors', None)
            base_visitors and visitors.update(base._selfvisitors)
            base_fullvisitors = getattr(base, '_fullvisitors', None)
            base_fullvisitors and fullvisitors.update(base._fullvisitors)

        for key, func in attrs.iteritems():
            if key.startswith('visit_'):
                key = key[6:] 
                visitors[key].append(func)
            elif key.startswith('fullvisit_'):
                key = key[10:]
                fullvisitors[key].append(func)

        attrs['_selfvisitors'] = visitors
        attrs['_fullvisitors'] = fullvisitors

        return super(VisitorMeta, mcls).__new__(mcls, name, bases, attrs)


class NodeVisitor(ast.NodeVisitor):
    __metaclass__ = VisitorMeta
