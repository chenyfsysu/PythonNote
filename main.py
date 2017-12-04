import sys
def f():
	for i in (1, 2, 3):
		print i

import dis
dis.dis(f)
# f.func_defaults = None
# f()