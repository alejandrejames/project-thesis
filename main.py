from submodules import topicmodel as t2
from submodules import usrmodules as usmdls
import os
import subprocess


name = 'sample.csv'
#usmdls.collectdata('albay')

##Data Cleaning
cleaned = t2.cleaning(name)
corpus = t2.mkcorpus(cleaned)
#

##Topic Modeling
t2.ldamdl(corpus,cleaned) #LDA Model
#t2.nmfmdl(cleaned) #NMF Model
#
