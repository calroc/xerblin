import os
from pysvn import Client, Revision, opt_revision_kind, 


repurl = 'file:///home/sforman/Desktop/heh/test0.svnrep'
wc = '/home/sforman/Desktop/heh/test0WC'

J = os.path.join

HEAD = Revision(opt_revision_kind.head)
UNSPECIFIED = Revision(opt_revision_kind.unspecified)
REVn = lambda n: Revision(opt_revision_kind.number, n)


##WC = os.path.expanduser('~/xerblin')
##path = J(WC, 'setup.py')


c = Client()

##
##file_annotation = c.annotate(
##    path,
##    revision_start=REVn(501),
##    revision_end=HEAD,
##    peg_revision=UNSPECIFIED,
##    )
