# -*- coding: utf-8 -*-

# Copyright 2008 Jaap Karssenberg <pardus@cpan.org>

'''Test cases for the zim.notebook module.'''

import tests

from zim.fs import *
from zim.config import config_file
from zim.notebook import *
from zim.index import LINK_DIR_FORWARD
import zim.errors
from zim.formats import ParseTree

class TestGetNotebook(tests.TestCase):

	slowTest = True

	def setUp(self):
		list = config_file('notebooks.list')
		file = list.file
		if file.exists():
			file.remove()

	def runTest(self):
		root = Dir(tests.create_tmp_dir('notebook_TestGetNotebook'))

		# Start empty - see this is no issue
		list = get_notebook_list()
		self.assertTrue(isinstance(list, NotebookList))
		self.assertFalse(list)

		nb, page = resolve_notebook('foo')
		self.assertTrue(nb is None)
		nb = resolve_default_notebook()
		self.assertTrue(nb is None)

		# Non-existing dir
		dir = root.subdir('/notebook')
		nb, page = resolve_notebook(dir.path)
		self.assertEqual(nb, dir)

		# Now create it
		init_notebook(dir, name='foo')
		file = dir.file('notebook.zim')
		nb, page = resolve_notebook(dir.path)
		self.assertEqual(nb, dir)
		nb, page = resolve_notebook(file.uri)
		self.assertEqual(nb, dir)
		file = dir.file('foo/bar/baz.txt')
		file.touch()
		nb, page = resolve_notebook(file.path)
		self.assertEqual(nb, dir)
		self.assertEqual(page, Path('foo:bar:baz'))

		# And put it in the list and resolve it by name
		list.append(dir.uri)
		list.write()
		list = get_notebook_list()
		self.assertTrue(len(list) == 1)
		nb, page = resolve_notebook('foo')
		self.assertEqual(nb, dir)

		# Single notebook is automatically the default
		nb = resolve_default_notebook()
		self.assertEqual(nb, dir)

		# But not anymore after adding second notebook
		list.append('file:///foo/bar')
		list.write()
		list = get_notebook_list()
		self.assertTrue(len(list) == 2)
		self.assertEqual(list[:], [dir.uri, 'file:///foo/bar'])

		nb, page = resolve_notebook('foo')
		self.assertEqual(nb, dir)
		self.assertTrue(isinstance(get_notebook(nb), Notebook))

		nb = resolve_default_notebook()
		self.assertTrue(nb is None)

		list.default = 'file:///default/foo'
		list.write()
		list = get_notebook_list()
		nb = resolve_default_notebook()
		self.assertEqual(nb, Dir('/default/foo'))
		self.assertEqual(get_notebook(nb), None)

		# Check interwiki parsing
		self.assertEqual(interwiki_link('wp?Foo'), 'http://en.wikipedia.org/wiki/Foo')
		self.assertEqual(interwiki_link('foo?Foo'), dir.uri+'?Foo')
		nb, page = resolve_notebook(dir.uri+'?Foo')
		self.assertEqual(nb, dir)
		self.assertEqual(page, 'Foo')

		# Check backward compatibility
		file = File('tests/data/notebook-list-old-format.list')
		wanted = [Dir('~/Notes').uri, Dir('/home/user/code/zim.debug').uri, Dir('/home/user/Foo Bar').uri]
		list = NotebookList(file)
		self.assertEqual(list[:], wanted)
		self.assertEqual(list.default, Dir('/home/user/code/zim.debug').uri)


class TestNotebook(tests.TestCase):

	def setUp(self):
		zim.errors.silence_signal_exception_context = True
		if not hasattr(self, 'notebook'):
			self.notebook = tests.get_test_notebook()
			self.notebook.index.update()

	def tearDown(self):
		zim.errors.silence_signal_exception_context = False

	def testAPI(self):
		'''Test various notebook methods'''
		# TODO now do the same with multiple stores
		self.assertEqual(
			self.notebook.get_store(':foo'), self.notebook._stores[''])

		self.assertTrue(
			isinstance(self.notebook.get_home_page(), Page))

		page1 = self.notebook.get_page(Path('Tree:foo'))
		page2 = self.notebook.get_page(Path('Tree:foo'))
		self.assertTrue(page1.valid)
		self.assertTrue(id(page2) == id(page1)) # check usage of weakref
		self.notebook.flush_page_cache(Path('Tree:foo'))
		page3 = self.notebook.get_page(Path('Tree:foo'))
		self.assertTrue(id(page3) != id(page1))
		self.assertFalse(page1.valid)

		pages = list(self.notebook.get_pagelist(Path(':')))
		self.assertTrue(len(pages) > 0)
		for page in pages:
			self.assertTrue(isinstance(page, Page))

		index = set()
		for page in self.notebook.walk():
			self.assertTrue(isinstance(page, Page))
			index.add(page.name)
		self.assertTrue(index.issuperset(self.notebook.testdata_manifest))

	def testManipulate(self):
		'''Test renaming, moving and deleting pages in the notebook'''

		# check test setup OK
		for path in (Path('Test:BAR'), Path('NewPage')):
			page = self.notebook.get_page(path)
			self.assertFalse(page.haschildren)
			self.assertFalse(page.hascontent)

		# check errors
		self.assertRaises(LookupError,
			self.notebook.move_page, Path('NewPage'), Path('Test:BAR'))
		self.assertRaises(PageExistsError,
			self.notebook.move_page, Path('Test:foo'), Path('TODOList'))

		self.notebook.index.update(background=True)
		self.assertTrue(self.notebook.index.updating)
		self.assertRaises(IndexBusyError, 
			self.notebook.move_page, Path('Test:foo'), Path('Test:BAR'))

		for oldpath, newpath in (
			(Path('Test:foo'), Path('Test:BAR')),
			(Path('TODOList'), Path('NewPage:Foo:Bar:Baz')),
		):
			self.notebook.index.ensure_update()
			page = self.notebook.get_page(oldpath)
			text = page.dump('wiki')
			self.assertTrue(page.haschildren)

			self.notebook.move_page(oldpath, newpath)

			# newpath should exist and look like the old one
			page = self.notebook.get_page(newpath)
			self.assertTrue(page.haschildren)
			self.assertEqual(page.dump('wiki'), text)

			# oldpath should be deleted
			page = self.notebook.get_page(oldpath)
			self.assertFalse(page.haschildren)
			self.assertFalse(page.hascontent)

			# let's delete the newpath again
			self.notebook.delete_page(newpath)
			page = self.notebook.get_page(newpath)
			self.assertFalse(page.haschildren)
			self.assertFalse(page.hascontent)

			# delete again should silently fail
			self.notebook.delete_page(newpath)

		# check cleaning up works OK
		page = self.notebook.get_page(Path('NewPage'))
		self.assertFalse(page.haschildren)
		self.assertFalse(page.hascontent)

		#~ print '\n==== DB ===='
		#~ self.notebook.index.ensure_update()
		#~ cursor = self.notebook.index.db.cursor()
		#~ cursor.execute('select * from pages')
		#~ for row in cursor:
			#~ print row
		#~ cursor.execute('select * from links')
		#~ for row in cursor:
			#~ print row

		# Try rename
		page = self.notebook.get_page(Path('Test:wiki'))
		self.assertTrue(page.hascontent)
		copy = page
			# we now have a copy of the page object - this is an important
			# part of the test - see if caching of page objects doesn't bite

		self.notebook.index.ensure_update()
		self.notebook.rename_page(Path('Test:wiki'), 'foo')
		page = self.notebook.get_page(Path('Test:wiki'))
		self.assertFalse(page.hascontent)
		page = self.notebook.get_page(Path('Test:foo'))
			# If we get an error here because notebook resolves Test:Foo
			# probably the index did not clean up placeholders correctly
		self.assertTrue(page.hascontent)

		self.assertFalse(copy.valid)

		self.notebook.index.ensure_update()
		self.notebook.rename_page(Path('Test:foo'), 'Foo')
		page = self.notebook.get_page(Path('Test:foo'))
		self.assertFalse(page.hascontent)
		page = self.notebook.get_page(Path('Test:Foo'))
		self.assertTrue(page.hascontent)

	def testUpdateLinks(self):
		'''Test logic for updating links on move'''

		# creating relative paths
		for source, href, link in (
			('Foo:Bar', 'Foo:Bar', 'Bar'),
			('Foo:Bar', 'Foo:Bar:Baz', '+Baz'),
			('Foo:Bar:Baz', 'Foo:Dus', 'Foo:Dus'),
			('Foo:Bar:Baz', 'Foo:Bar:Dus', 'Bar:Dus'),
			('Foo:Bar', 'Dus:Ja', ':Dus:Ja'),
		):
			#~ print '>', source, href, link
			self.assertEqual(
				self.notebook.relative_link(Path(source), Path(href)), link)

		# update the page that was moved itself
		# moving from Dus:Baz to Foo:Bar:Baz
		text = u'''\
http://foo.org # urls are untouched
[[:Hmmm:OK]] # link way outside move
[[Baz:Ja]] # relative link that does not need change
[[Dus:Ja]] # relative link that needs updating
[[Dus:Ja|Grrr]] # relative link that needs updating - with name
[[:Foo:Bar:Dus]] # Link that could be mde relative, but isn't
'''
		wanted = u'''\
http://foo.org # urls are untouched
[[:Hmmm:OK]] # link way outside move
[[Baz:Ja]] # relative link that does not need change
[[:Dus:Ja]] # relative link that needs updating
[[:Dus:Ja|Grrr]] # relative link that needs updating - with name
[[:Foo:Bar:Dus]] # Link that could be mde relative, but isn't
'''
		notebook, page = tests.get_test_page('Foo:Bar:Baz')
		page.parse('wiki', text)
		notebook._update_links_from(page, Path('Dus:Baz'))
		self.assertEqualDiff(u''.join(page.dump('wiki')), wanted)

		# updating links to the page that was moved
		# moving from Dus:Baz to Foo:Bar:Baz - updating links in Dus:Ja
		text = u'''\
http://foo.org # urls are untouched
[[:Hmmm:OK]] # link way outside move
[[Baz:Ja]] # relative link that needs updating
[[Baz:Ja|Grr]] # relative link that needs updating - with name
[[Dus:Foo]] # relative link that does not need updating
[[:Dus:Baz]] # absolute link that needs updating
[[:Dus:Baz:Hmm]] # absolute link that needs updating
[[:Dus:Baz:Hmm:Ja]] # absolute link that needs updating
'''
		wanted = u'''\
http://foo.org # urls are untouched
[[:Hmmm:OK]] # link way outside move
[[:Foo:Bar:Baz:Ja]] # relative link that needs updating
[[:Foo:Bar:Baz:Ja|Grr]] # relative link that needs updating - with name
[[Dus:Foo]] # relative link that does not need updating
[[:Foo:Bar:Baz]] # absolute link that needs updating
[[:Foo:Bar:Baz:Hmm]] # absolute link that needs updating
[[:Foo:Bar:Baz:Hmm:Ja]] # absolute link that needs updating
'''
		notebook, page = tests.get_test_page('Dus:Ja')
		page.parse('wiki', text)
		notebook._update_links_in_page(page, Path('Dus:Baz'), Path('Foo:Bar:Baz'))
		self.assertEqualDiff(u''.join(page.dump('wiki')), wanted)

		# now test actual move on full notebook
		def links(source, href):
			#~ print '===='
			for link in self.notebook.index.list_links(source, LINK_DIR_FORWARD):
				#~ print 'FOUND LINK', link
				if link.href == href:
					return True
			else:
				return False

		path = Path('Linking:Dus:Ja')
		self.assertTrue(links(path, Path('Linking:Dus')))
		self.assertTrue(links(path, Path('Linking:Foo:Bar')))
		self.assertTrue(links(Path('Linking:Foo:Bar'), path))

		newpath = Path('Linking:Hmm:Ok')
		self.assertFalse(links(newpath, Path('Linking:Dus')))
		self.assertFalse(links(newpath, Path('Linking:Foo:Bar')))
		self.assertFalse(links(Path('Linking:Foo:Bar'), newpath))
		self.notebook.move_page(path, newpath, update_links=True)
		self.assertTrue(links(newpath, Path('Linking:Dus')))
		self.assertTrue(links(newpath, Path('Linking:Foo:Bar')))
		self.assertTrue(links(Path('Linking:Foo:Bar'), newpath))


	def testResolvePath(self):
		'''Test notebook.resolve_path()'''

		# cleaning absolute paths
		for name, wanted in (
			('foo:::bar', 'foo:bar'),
			('::foo:bar:', 'foo:bar'),
			(':foo', 'foo'),
			(':Bar', 'Bar'),
			# TODO more ambigous test cases
		): self.assertEqual(
			self.notebook.resolve_path(name), Path(wanted) )

		# resolving relative paths
		for name, ns, wanted in (
			('foo:bar', 'Test:xxx', 'Test:foo:bar'),
			('test', 'Test:xxx', 'Test'),
			('+test', 'Test:xxx', 'Test:xxx:test'),
			('foo', 'Test:xxx', 'Test:foo'),
			('+foo', 'Test:xxx', 'Test:xxx:foo'),
			('Test', 'TODOList:bar', 'Test'),
			('test:me', 'TODOList:bar', 'Test:me'),
		): self.assertEqual(
			self.notebook.resolve_path(name, Path(ns)), Path(wanted) )

		self.assertRaises(PageNameError, self.notebook.resolve_path, ':::')

	def testResolveFile(self):
		'''Test notebook.resolve_file()'''
		dir = Dir(tests.create_tmp_dir('notebook_testResolveFile'))
		path = Path('Foo:Bar')
		self.notebook.dir = dir
		self.notebook.get_store(path).dir = dir
		self.notebook.config['Notebook']['document_root'] = './notebook_document_root'
		doc_root = self.notebook.get_document_root()
		for link, wanted, cleaned in (
			('~/test.txt', File('~/test.txt'), '~/test.txt'),
			(r'~\test.txt', File('~/test.txt'), '~/test.txt'),
			('file:///test.txt', File('file:///test.txt'), None),
			('file:/test.txt', File('file:///test.txt'), None),
			('file://localhost/test.txt', File('file:///test.txt'), None),
			('/test.txt', doc_root.file('test.txt'), '/test.txt'),
			('./test.txt', dir.file('Foo/Bar/test.txt'), './test.txt'),
			(r'.\test.txt', dir.file('Foo/Bar/test.txt'), './test.txt'),
			('../test.txt', dir.file('Foo/test.txt'), '../test.txt'),
			(r'..\test.txt', dir.file('Foo/test.txt'), '../test.txt'),
			('../Bar/Baz/test.txt', dir.file('Foo/Bar/Baz/test.txt'), './Baz/test.txt'),
			(r'C:\foo\bar', File('file:///C:/foo/bar'), None),
			(r'Z:\foo\bar', File('file:///Z:/foo/bar'), None),
		):
			#~ print link, '>>', self.notebook.resolve_file(link, path)
			self.assertEqual(
				self.notebook.resolve_file(link, path), wanted)
			self.assertEqual(
				self.notebook.relative_filepath(wanted, path), cleaned)

		# check relative path without Path
		self.assertEqual(
			self.notebook.relative_filepath(doc_root.file('foo.txt')), '/foo.txt')

#	def testResolveLink(self):
#		'''Test page.resolve_link()'''
#		page = self.notebook.get_page(':Test:foo')
#		for link, wanted in (
			#~ (':foo:bar', ('page', ':foo:bar')),
#			('foo:bar', ('page', ':Test:foo:bar')),
#			('Test', ('page', ':Test')),
#			('Test:non-existent', ('page', ':Test:non-existent')),
#			('user@domain.com', ('mailto', 'mailto:user@domain.com')),
#			('mailto:user@domain.com', ('mailto', 'mailto:user@domain.com')),
#			('http://zim-wiki.org', ('http', 'http://zim-wiki.org')),
#			('foo://zim-wiki.org', ('foo', 'foo://zim-wiki.org')),
			#~ ('file://'),
			#~ ('/foo/bar', ('file', '/foo/bar')),
			#~ ('man?test', ('man', 'test')),
#		): self.assertEqual(self.notebook.resolve_link(link, page), wanted)

	#~ def testResolveName(self):
		#~ '''Test store.resolve_name().'''
		#~ print '\n'+'='*10+'\nSTORE: %s' % self.store
#~
		#~ # First make sure basic list function is working
		#~ def list_pages(name):
			#~ for page in self.store.get_pages(name):
				#~ yield page.basename
		#~ self.assertTrue('Test' in list_pages(''))
		#~ self.assertTrue('foo' in list_pages(':Test'))
		#~ self.assertTrue('bar' in list_pages(':Test:foo'))
		#~ self.assertFalse('Dus' in list_pages(':Test:foo'))
#~
		#~ # Now test the resolving algorithm - only testing low level
		#~ # function in store, so path "anchor" does not work, search
		#~ # is strictly right to left through the namespace, if any
		#~ for link, namespace, name in (
			#~ ('BAR','Test:foo','Test:foo:bar'),
			#~ ('test',None,'Test'),
			#~ ('test','Test:foo:bar','Test'),
			#~ ('FOO:Dus','Test:foo:bar','Test:foo:Dus'),
			#~ # FIXME more ambigous test data
		#~ ):
			#~ print '-'*10+'\nLINK %s (%s)' % (link, namespace)
			#~ r = self.store.resolve_name(link, namespace=namespace)
			#~ print 'RESULT %s' % r
			#~ self.assertEqual(r, name)


class TestPath(tests.TestCase):
	'''Test path object'''

	def generator(self, name):
		return Path(name)

	def runTest(self):
		'''Test Path object'''

		for name, namespace, basename in [
			('Test:foo', 'Test', 'foo'),
			('Test', '', 'Test'),
		]:
			path = self.generator(name)

			# test basic properties
			self.assertEqual(path.name, name)
			self.assertEqual(path.basename, basename)
			self.assertEqual(path.namespace, namespace)
			self.assertTrue(path.name in path.__repr__())

	# TODO test operators on paths > < + - >= <= == !=

class TestPage(TestPath):
	'''Test page object'''

	def setUp(self):
		self.notebook = tests.get_test_notebook()

	def generator(self, name):
		return self.notebook.get_page(Path(name))

	def runTest(self):
		'''Test Page object'''
		TestPath.runTest(self)

		tree = ParseTree().fromstring('''\
<zim-tree>
<link href='foo:bar'>foo:bar</link>
<link href='bar'>bar</link>
</zim-tree>
'''		)
		page = Page(Path('Foo'))
		page.readonly = False
		page.set_parsetree(tree)

		links = list(page.get_links())
		self.assertEqual(links, [
			('page', 'foo:bar', {}),
			('page', 'bar', {}),
		] )

		self.assertEqual(page.get_parsetree().tostring(), tree.tostring())
			# ensure we didn't change the tree

		# TODO test get / set parse tree with and without source

		tree = ParseTree().fromstring('<zim-tree></zim-tree>')
		self.assertFalse(tree.hascontent)
		page.set_parsetree(tree)
		self.assertFalse(page.hascontent)

