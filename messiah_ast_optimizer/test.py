import sys

def trace_func(frame,event,arg):
	print frame, event, arg
	value = frame.f_locals["a"]
	if value % 2 == 0:
		value += 1
		frame.f_locals["a"] = value

def f(a):
	print a

if __name__ == "__main__":
	sys.settrace(trace_func)
	for i in range(0,5):
		f(i)