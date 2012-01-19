import os
import sys
import time
import urllib, urllib2
from urllib2 import HTTPError
from pubmed.inhaler import articles_for_pubmed_efetch

#EUTIL_ROOT = 'http://www.ncbi.nlm.nih.gov/entrez/eutils'
EUTIL_ROOT = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
ESEARCH    = '%s/%s' % (EUTIL_ROOT, 'esearch.fcgi')
EFETCH     = '%s/%s' % (EUTIL_ROOT, 'efetch.fcgi')

def initreqparams():
    req = {}
    req['db'] = 'pubmed'
    req['tool'] = 'inhaler'
    req['email'] = 'raman_prasad@harvard.edu'
    req['retmax'] = '5000'
    req['retmode'] = 'xml'
#   req['usehistory'] = 'y'
    return req


def pubmed_efetch(pmidset, ckpoint=True):
    rp = initreqparams()
    rp['id'] = ','.join(pmidset)

    req = urllib2.Request(EFETCH, urllib.urlencode(rp))

    try:
        res = urllib2.urlopen(req)
    except HTTPError:
        return None
    except:
        return None

    xmlstr = res.read()
    articles = articles_for_pubmed_efetch(xmlstr)

    return articles


def test(fname):
    f = open(fname, 'r')    #'samples/abstract.txt')
    xmlstr = f.read()
    f.close()
    articles = articles_for_pubmed_efetch(xmlstr)
    for a in articles:
        print a
        
if __name__=='__main__':
    #test(sys.argv[1])
    #pubmed_efetch(['14361377', '15497569'])#, '13951608'])
    pass
