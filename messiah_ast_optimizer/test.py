import ast
import astunparse
print astunparse.dump(ast.parse('def func(self, dt): self.call(name)').body[0])
