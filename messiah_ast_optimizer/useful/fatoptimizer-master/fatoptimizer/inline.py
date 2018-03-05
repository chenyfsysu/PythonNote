import ast

from .tools import (OptimizerStep, NodeTransformer, NodeVisitor,
                    pretty_dump, get_starargs, get_keywords, get_varkeywords)

class Checker(NodeVisitor):
    '''Gather a list of problems that would prevent inlining a function.'''
    def __init__(self):
        self.problems = []

    def visit_Call(self, node):
        # Reject explicit attempts to use locals()
        # FIXME: detect uses via other names
        if isinstance(node.func, ast.Name):
            if node.func.id == 'locals':
                self.problems.append('use of locals()')


def locate_kwarg(funcdef, name):
    '''Get the index of an argument of funcdef by name.'''
    for idx, arg in enumerate(funcdef.args.args):
        if arg.arg == name:
            return idx
    raise ValueError('argument %r not found' % name)


class RenameVisitor(NodeTransformer):
    # FIXME: Reuse tools.ReplaceVariable

    def __init__(self, callsite, inlinable, actual_pos_args):
        assert get_starargs(callsite) is None
        assert not get_varkeywords(callsite) is not None
        assert inlinable.args.vararg is None
        assert inlinable.args.kwonlyargs == []
        assert inlinable.args.kw_defaults == []
        assert inlinable.args.kwarg is None
        assert inlinable.args.defaults == []

        # Mapping from name in callee to node in caller
        self.remapping = {}
        for formal, actual in zip(inlinable.args.args, actual_pos_args):
            self.remapping[formal.arg] = actual

    def visit_Name(self, node):
        if node.id in self.remapping:
            return self.remapping[node.id]
        return node


class Expansion:
    '''Information about a callsite that's a candidate for inlining, giving
    the funcdef, and the actual positional arguments (having
    resolved any keyword arguments.'''
    def __init__(self, funcdef, actual_pos_args):
        self.funcdef = funcdef
        self.actual_pos_args = actual_pos_args


class InlineSubstitution(OptimizerStep):
    """Function call inlining."""

    def build_positional_args(self, candidate, callsite):
        """Attempt to convert the positional and keyword args supplied at
        the given callsite to the positional args expected by the candidate
        funcdef.

        Return a list of ast.Node instances, or raise ValueError if it
        can't be done.
        """
        if len(callsite.args) > len(candidate.args.args):
            raise ValueError('too many positional arguments')
        slots = {}
        for idx, arg in enumerate(callsite.args):
            slots[idx] = arg
        for actual_kwarg in get_keywords(callsite):
            idx = locate_kwarg(candidate, actual_kwarg.arg)
            if idx in slots:
                raise ValueError('positional slot %i already filled' % idx)
            slots[idx] = actual_kwarg.value
        actual_pos_args = []
        for idx in range(len(candidate.args.args)):
            if idx not in slots:
                raise ValueError('argument %i not filled' % idx)
            actual_pos_args.append(slots[idx])
        return actual_pos_args

    def can_inline(self, callsite):
        '''Given a Call callsite, determine whether we should inline
        the callee.  If so, return an Expansion instance, otherwise
        return None.'''
        # FIXME: size criteria?
        # FIXME: don't do it for recursive functions
        if not isinstance(callsite.func, ast.Name):
            return None
        from .namespace import _fndefs
        if callsite.func.id not in _fndefs:
            return None
        candidate = _fndefs[callsite.func.id]

        # For now, only support simple positional arguments
        # and keyword arguments
        if get_starargs(callsite) is not None:
            return False
        if get_varkeywords(callsite) is not None:
            return False
        if candidate.args.vararg:
            return False
        if candidate.args.kwonlyargs:
            return False
        if candidate.args.kw_defaults:
            return False
        if candidate.args.kwarg:
            return False
        if candidate.args.defaults:
            return False

        # Attempt to match up the calling convention at the callsite
        # with the candidate funcdef
        try:
            actual_pos_args = self.build_positional_args(candidate, callsite)
        except ValueError:
            return None
        # For now, only allow functions that simply return a value
        body = candidate.body
        if len(body) != 1:
            return None
        if not (isinstance(body[0], ast.Return)
                or isinstance(body[0], ast.Pass)):
            return None

        # Walk the candidate's nodes looking for potential problems
        c = Checker()
        c.visit(body[0])
        if c.problems:
            return None

        # All checks passed
        return Expansion(candidate, actual_pos_args)

    def visit_Call(self, node):
        if not self.config.inlining:
            return

        # FIXME: renaming variables to avoid clashes
        # or do something like:
        #   .saved_locals = locals()
        #   set params to args
        #   body of called function
        #   locals() = .saved_locals
        #   how to things that aren't just a return
        #   how to handle early return
        # FIXME: what guards are needed?
        # etc
        expansion = self.can_inline(node)
        if not expansion:
            return node
        funcdef = expansion.funcdef
        # Substitute the Call with the expression of the single return stmt
        # within the callee.
        # This assumes a single Return or Pass stmt
        stmt = funcdef.body[0]
        if isinstance(stmt, ast.Return):
            returned_expr = funcdef.body[0].value
            # Rename params/args
            v = RenameVisitor(node, funcdef, expansion.actual_pos_args)
            new_expr = v.visit(returned_expr)
        else:
            assert isinstance(stmt, ast.Pass)
            new_expr = self.new_constant(stmt, None)
        return new_expr
