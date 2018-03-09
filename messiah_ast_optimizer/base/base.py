# -*- coding:utf-8 -*-

import ast


class VisitorMeta(type):
    def __new__(mcls, name, bases, attrs):
        visitors = {}
        fullvisitors = {}
        for base in bases:
            base_visitors = getattr(base, '_visitors', None)
            base_visitors and visitors.update(base._visitors)
            base_fullvisitors = getattr(base, '_fullvisitors', None)
            base_fullvisitors and fullvisitors.update(base._fullvisitors)

        for key, func in attrs.iteritems():
            if key.startswith('visit_'):
                visitors[key[6:]] = func
            elif key.startswith('fullvisit_'):
                fullvisitors[key[10:]] = func

        attrs['_selfvisitors'] = visitors
        attrs['_fullvisitors'] = fullvisitors

        return super(VisitorMeta, mcls).__new__(mcls, name, bases, attrs)


class NodeVisitor(ast.NodeVisitor):
    __metaclass__ = VisitorMeta
