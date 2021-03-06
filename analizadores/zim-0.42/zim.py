#!/usr/bin/python

import sys

# Check if we run the correct python version
try:
	version_info = sys.version_info
	assert version_info >= (2, 5)
	assert version_info < (3, 0)
except:
	print >> sys.stderr, 'ERROR: zim needs python >= 2.5   (but < 3.0)'
	sys.exit(1)


# Try importing our modules
import zim
import zim.config
try:
	pass
except ImportError:
	print >>sys.stderr, 'ERROR: Could not find python module files in path:'
	print >>sys.stderr, ' '.join(map(str, sys.path))
	print >>sys.stderr, '\nTry setting PYTHONPATH'
	sys.exit(1)


# Check if we can find our data files
try:
	icon = zim.config.data_file('zim.png')
	assert not icon is None
except:
	print >>sys.stderr, 'ERROR: Could not find data files in path:'
	print >>sys.stderr, ' '.join(map(str, zim.config.data_dirs()))
	print >>sys.stderr, '\nTry setting XDG_DATA_DIRS'
	sys.exit(1)


# Run the application and handle some exceptions
try:
	argv = [arg.decode('utf-8') for arg in sys.argv]
	zim.main(argv)
except zim.GetoptError, err:
	print >>sys.stderr, sys.argv[0]+':', err
	sys.exit(1)
except zim.UsageError, err:
	print >>sys.stderr, zim.usagehelp.replace('zim', sys.argv[0])
	sys.exit(1)
except KeyboardInterrupt: # e.g. <Ctrl>C while --server
	print >>sys.stderr, 'Interrupt'
	sys.exit(1)
else:
	sys.exit(0)
