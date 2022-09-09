def announce(fn):
	def wrapperDef():
		print('About to run the function...')
		fn()
		print('Done with the function.')
	return wrapperDef

@announce
def hello():
	print('Hello, world!')

hello()
