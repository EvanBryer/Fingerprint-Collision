#Key collision using fingerprinting
import argparse
parser = argparse.ArgumentParser(description='Perform PPM clustering with a spell check ranking.')
req = parser.add_argument_group('Required arguments')
parser.add_argument("-p", "--path", help="path to file of new line delimited strings.", required=True)
parser.add_argument("-t", "--tolerance", help="Percent tolerance for considering two strings members of a cluster. Default is 0.7", type=float, default=0.7)
parser.add_argument("-o", "--out", help="Output file containing clustered data. Default is ./out.txt", default="./out.txt")
req = parser.parse_args()

import io
import string
import hunspell
import re
from alive_progress import alive_bar
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import operator

#Select languages
hobj = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
hobj.add_dic('/usr/share/hunspell/fr.dic')
hobj.add_dic('/usr/share/hunspell/de.dic')
hobj.add_dic('/usr/share/hunspell/la.dic')
stpwrds = set()
stpwrds.update(stopwords.words('english'))
stpwrds.update(set(stopwords.words('french')))
stpwrds.update(set(stopwords.words('german')))
stpwrds.update(set(stopwords.words('spanish')))
stpwrds.update(set(stopwords.words('italian')))
stpwrds.update(set(stopwords.words('dutch')))
#Path to files
f1 = open(req.path).readlines()
used = []
clusts = []
def text_process(text):
    '''
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove digits
    3. Remove all stopwords from included languages
   	4. Return the cleaned text as a list of words
    '''
    stemmer = WordNetLemmatizer()
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join([i for i in nopunc if not i.isdigit()])
    nopunc =  [word.lower() for word in nopunc.split() if word not in stpwrds]
    return [stemmer.lemmatize(word) for word in nopunc]

def check(clusts):
	for clust in clusts:
		print(clust)
		if len(set(clust)) == len(clust):
			for c in range(len(clust)):
				clust[c] = clust[0]
		else:
			d = {}
			for c in clust:
				if c not in d:
					d[c] = 0
				d[c]+=1
			key = max(d.items(), key=operator.itemgetter(1))[0]
			for c in range(len(clust)):
				clust[c] = key
		print(clust)

with alive_bar(len(f1)) as bar:
	for l in range(len(f1)):
		f1[l] = re.sub("\n","",f1[l])
		orig = set(text_process(f1[l]))
		clust = [f1[l]]
		for c in range(l+1,len(f1)):
			if c in used: continue
			f1[c] = re.sub("\n","",f1[c])
			comp = set(text_process(f1[c]))
			col = orig.intersection(comp)
			if len(col) > req.tolerance*((len(orig)+len(comp))/2):
				used.append(c)
				clust.append(f1[c])
		if len(clust) > 1:
			clusts.append(clust)
		bar()
	check(clusts)
	with open(req.out,"w") as init:
		init.write("")
		init.close()
	for clust in clusts:
		with open(req.out, "a") as appen:
			for c in clust:
				appen.write(f"{c}\t")
			appen.write("\n")


