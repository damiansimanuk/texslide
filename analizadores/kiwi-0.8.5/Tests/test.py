# -----------------------------------------------------------------------------
# Project           :   Kiwi
# Author            :   Sebastien Pierre
# License           :   BSD License (revised)
# -----------------------------------------------------------------------------
# Creation date     :   10-Feb-2006
# Last mod.         :   10-Feb-2006

import os, sys, re

TEST_FILE  = re.compile("(syntax)\-(.+)\.kwi")
TEST_FILES = {}

DIR  = os.path.dirname(os.path.abspath(__file__) ) + "/results"
KIWI = os.path.abspath(DIR + "/../../Sources/kiwi/main.py")
if not os.path.exists(DIR):
    os.makedirs(DIR)
def do():
	# We populate the test files hash table
	this_dir = os.path.abspath(os.path.dirname(__file__))
	for path in os.listdir(this_dir):
		m = TEST_FILE.match(path)
		if not m: continue
		f = TEST_FILES.setdefault(m.group(1), [])
		f.append((m.group(2), os.path.join(this_dir, path)))

	index_f = file(DIR + "/index.html", "w")
	index_f.write("<html><body><h1>Kiwi test suite</h1><table>")

	# And now execute the tests
	groups = TEST_FILES.keys() ; groups.sort()
	files  = []
	for group in groups:
		index_f.write("<tr><td colspan='3'><code>%s</code></td></tr>" % (group))
		for test, test_path in TEST_FILES[group]:
			print "%4s:%25s " % (group, test),
			inp, out, err = os.popen3("python " + KIWI + " -m " + test_path)
			dest_path = os.path.splitext(test_path)[0] + ".html"
			f = open(dest_path, "w")
			f.write(out.read())
			f.close()
			index_f.write("<tr><td>&nbsp;</td><td><code>%s</code></td><td>[<a href='%s'>KIWI</a> &rArr; <a href='%s'>HTML</a>]</td></tr> " % (
			test, test_path, dest_path))
			files.append(dest_path)
			err =  err.read()
			if err.strip() == "": print "[OK]"
			else: print "[FAILED]", err

	index_f.write("</table></body></html>")
	index_f.close()

if __name__ == "__main__":
	if len(sys.argv) == 1:
		do()
	else:
		os.system("rm %s/*.html" % (os.path.dirname(__file__) or "."))
# EOF
