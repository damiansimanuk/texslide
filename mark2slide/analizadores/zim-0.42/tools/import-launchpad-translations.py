#!/usr/bin/python

import sys
import tarfile
import re

MIN_TRANLATIONS = 175

def count_messages(file):
	return count('msgid', file)

def count_translations(file):
	return count('msgstr', file)

def count(prefix, file):
	count = 0
	l = len(prefix)
	for line in file:
		if line.startswith(prefix):
			string = line[l:].strip().strip('"')
			if string:
				count +=1
	return count

def get_lang(name):
	match = re.search(r'(^|[-/])(\w+).po$', name)
	assert match, 'Could not parse LANG from %s !?' % name
	return match.group(2)

def import_translations_from(archive):
	tfile = tarfile.open(archive, 'r:gz')
	names = tfile.getnames()
	#~ print names

	potfiles = [n for n in names if n.endswith('.pot')]
	assert len(potfiles) == 1, 'Multiple template files in this archive !?'
	total = count_messages(tfile.extractfile(potfiles[0]))
	print '%i messages in catalogue' % total

	pofiles = [] 
	for name in [n for n in names if n.endswith('.po')]:
		lang = get_lang(name)
		file = tfile.extractfile(name).readlines()
		n = count_translations(file)
		pofiles.append((n, lang, file))

	files = []
	for n, lang, file in pofiles:
		perc = float(n) / total * 100
		if n >= MIN_TRANLATIONS:
			status = 'OK'
			files.append(('po/%s.po' % lang, file))
		else:
			status = ''
		print '%-6s %i translated (%i%%) %s' % (lang, n, perc, status) 
		
	for path, file in files:
		print 'Writing %s' % path
		open(path, 'w').writelines(file)
	
	print '\nPlease check `bzr st` for newly added translations and update CHANGELOG'
	print 'You need to run `./setup.py build_trans` to use the newly imported po files'

if __name__ == '__main__':
	assert len(sys.argv) == 2 and sys.argv[1].endswith('.tar.gz')
	import_translations_from(sys.argv[1])
