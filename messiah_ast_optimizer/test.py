class EntryMerger(object):

	def __init__(self, logger):
		self.logger = logger
		self.entries = defaultdict(list)

	def dump(self):
		raise NotImplementedError

	def check(self, node):
		checker = getattr(self, 'check_%s' % node.__class__.__name__)
		return checker(node)

	def merge(self, node):
		merger = getattr(self, 'merge_%s' % node.__class__.__name__)
		return merger(node)


class GlobalEntryMerger(EntryMerger):

	def __init__(self, logger):
		super(GlobalEntryMerger, self).__init__(logger)
		self.names = {}
		self.merged_files = {}

	def dump(self):
		getter = operator.itemgetter('Import', 'ImportFrom', 'Stmt')
		return [body for c in getter(self.entries) for body in c]

	def sameModule(self, src, dst):
		return src.findModule() is dst.findModule()

	def check_Import(self, node):
		accept = True
		for alias in node.names:
			name = alias.inferName()

			if name not in self.names:
				continue

			desc = self.names[name]
			if desc[0] != 'Import':
				accept = False
			else:
				type, fullname, index, _ = self.names[name]
				cur = self.entries[type][index]
				accept = cur.findModule(fullname) is node.findModule(alias.name)

			if not accept:
				self.markDuplicate(name, node.nModule().__file__, desc[-1])
				break

		return accept

	def check_ImportFrom(self, node):
		accept = True
		for alias in node.names:
			name = alias.inferName()

			if name == '*':
				self.logger.warning('componennt %s import star from %s, merge is skip', node.nModule().__file__, node.module)
				return False

			if name not in self.names:
				continue

			desc = self.names[name]
			if desc[0] != 'ImportFrom':
				accept = False
			else:
				type, fromlist, index, _ = self.names[name]
				cur = self.entries[type][index]
				accept = fromlist == alias.name and cur.findModule() is node.findModule()

			if not accept:
				self.markDuplicate(name, node.nModule().__file__, desc[-1])
				break

		return accept

	def check_Assign(self, node):
		for target in node.targets:
			names = get_names(target)

			if not names:
				self.logger.warning('Strange assignment is defined in %s', node.nModule().__file__)
				return False

			for name in names :
				if name in self.names:
					self.markDuplicate(name, node.nModule().__file__, self.names[name][-1])
					return False

		return True

	def check_FunctionDef(self, node):
		return self._checkFunctionOrClass(node)

	def check_ClassDef(self, node):
		return self._checkFunctionOrClass(node)

	def _checkFunctionOrClass(self, node):
		accept = node.name not in self.names
		if not accept:
			name = node.name
			self.markDuplicate(name, node.nModule().__file__, self.names[name][-1])

		return accept

	def merge_Import(self, node):
		self._mergeImport(node)
		for alias in node.names:
			module = node.findModule(alias.name)
			if alias.name != module.__name__:
				alias.name = module.__name__

	def merge_ImportFrom(self, node):
		self._mergeImport(node)
		
		module = node.findModule()
		if module.__name__ != node.module:
			node.module = module.__name__

	def _mergeImport(self, node):
		"""有些相对Import"""
		remove = True
		type = node.__class__.__name__
		path = node.nModule().__file__
		for alias in node.names:
			name = alias.inferName()
			if name in self.names:
				continue

			remove = False
			self.names[name] = (type, alias.name, len(self.entries[type]), path)

		if not remove:
			self.entries[type].append(node)

	def merge_Assign(self, node):
		self.entries['Stmt'].append(node)
		path = node.nModule().__file__

		for target in node.targets:
			names = get_names(target)
			for name in names:
				self.names[name] = ('Stmt', path)

	def merge_FunctionDef(self, node):
		self.entries['Stmt'].append(node)
		self.names[node.name] = ('Stmt', node.nModule().__file__)

	def merge_ClassDef(self, node):
		self.entries['Stmt'].append(node)
		self.names[node.name] = ('Stmt', node.nModule().__file__)

	def markDuplicate(self, name, dst, src):
		self.logger.warning('Global definition of name %s in %s is duplicate with file in %s', name, dst, src)


class ComponentEntryMerger(EntryMerger):

	def __init__(self, logger):
		super(ComponentEntryMerger, self).__init__(logger)
		self.stmt_names = {}
		self.func_names = {}
		self.reserved_comp_cls = []
		self.reserved_funcs = defaultdict(list)
		self.reserved_args_tmpl = {}

	def dump(self):
		getter = operator.itemgetter('Stmt', 'FunctionDef')
		bodies = [body for c in getter(self.entries) for body in c]
		bodies.extend(self.dumpReservedFuncs())

		return bodies

	def getEntryModule(self, name):
		return self.stmt_names[name][-1]

	def check_FunctionDef(self, node):
		return True

	def check_Expr(self ,node):
		return True

	def check_Assign(self, node):
		comp_name = node.parent.name
		for target in node.targets:
			names = get_names(target)

			if not names:
				self.logger.warning('Strange assignment is defined in %s, Component(%s)', node.nModule().__file__, comp_name)
				return False

			for name in names :
				if name in self.stmt_names:
					self.markDuplicate(name, comp_name, node.nModule().__file__, self.getEntryModule(name))
					return False

		return True

	def check_ClassDef(self, node):
		accept = node.name not in self.stmt_names
		if not accept:
			self.markDuplicate(node.name, node.parent.name, node.nModule().__file__, self.getEntryModule(node.name))

		return accept

	def merge_FunctionDef(self, node):
		if node.name.endswith('component__'):
			self.handleReservedFunc(node)

		if False and node.name in self.func_names:
			_, _, index = self.func_names[node.name]
			self.entries['FunctionDef'][index] = node
		else:
			self.func_names[node.name] = ('FunctionDef', node.nModule().__file__, len(self.func_names))
			self.entries['FunctionDef'].append(node)

	def merge_Expr(self, node):
		self.entries['Stmt'].append(node)

	def merge_Assign(self, node):
		self.entries['Stmt'].append(node)
		path = node.nModule().__file__

		for target in node.targets:
			names = get_names(target)
			for name in names:
				self.stmt_names[name] = ('Stmt', path)

	def merge_ClassDef(self, node):
		self.entries['Stmt'].append(node)
		self.stmt_names[node.name] = ('Stmt', node.nModule().__file__)

	def handleReservedFunc(self, node):
		name = '%s%s' % (node.name, node.nModule().__name__.replace('.', '_'))
		key = node.name.split('_')[2]

		if key not in self.reserved_args_tmpl:
			self.reserved_args_tmpl[key] = node.args
		else:
			tmpl = self.reserved_args_tmpl[key]
			if tmpl.argsFlag() != node.args.argsFlag():
				self.reserved_args_tmpl[key] = ast.arguments(args=[], vararg='args', kwarg='kwargs', defaults=[])

		self.reserved_funcs[key].append(name)
		node.name = name

	def dumpReservedFuncs(self):
		funcs = []
		for key, containers in self.reserved_funcs.iteritems():
			if not containers:
				continue

			stmts = []			
			tmpl = self.reserved_args_tmpl[key]
			for func in containers:
				stmts.append(self._dumpFuncCall(func, tmpl))

			funcs.append(self._dumpFuncDef(key, tmpl, stmts))

		return funcs

	def _dumpFuncCall(self, func, tmpl):
		func = ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=func, ctx=ast.Load())
		args = [ast.Name(id=name.id, ctx=ast.Load()) for name in tmpl.args[1:]] if tmpl.args else []
		starargs = ast.Name(id=tmpl.vararg, ctx=ast.Load()) if tmpl.vararg else None
		kwargs = ast.Name(id=tmpl.kwarg, ctx=ast.Load()) if tmpl.kwarg else None
		return ast.Expr(value=ast.Call(func=func, args=args, keywords=[], starargs=starargs, kwargs=kwargs))

	def _dumpFuncDef(self, key, args, stmts):
		name = '_host_%s' % key
		return ast.FunctionDef(name=name, args=args, body=stmts, decorator_list=[])

	def markDuplicate(self, name, comp, dst, src):
		self.logger.warning('Component(%s) definition of name %s in %s is duplicate with file in %s', name, comp, dst, src)
