# -*- coding:utf-8 -*-

import ast


class VisitorMeta(type):
    def __new__(mcls, name, bases, attrs):
        visitors = {}
        fullvisitors = {}
        for base in bases:
            base_visitors = getattr(base, '_selfvisitors', None)
            base_visitors and visitors.update(base._selfvisitors)
            base_fullvisitors = getattr(base, '_fullvisitors', None)
            base_fullvisitors and fullvisitors.update(base._fullvisitors)

        for key, func in attrs.iteritems():
            if key.startswith('visit_'):
                key = key[6:] 
                visitors.setdefault(key, list())
                visitors[key].append(func)
            elif key.startswith('fullvisit_'):
                key = key[10:]
                fullvisitors.setdefault(key, list())
                fullvisitors[key].append(func)

        attrs['_selfvisitors'] = visitors
        attrs['_fullvisitors'] = fullvisitors

        return super(VisitorMeta, mcls).__new__(mcls, name, bases, attrs)


class NodeVisitor(ast.NodeVisitor):
    __metaclass__ = VisitorMeta
