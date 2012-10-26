import os
import sys
import time
import urllib, urllib2
from pubmed_processor import PubMedProcessor
try:
    import simplejson as json
except:
    import json
from urllib2 import HTTPError
#from pubmed.inhaler import articles_for_pubmed_efetch


#EUTIL_ROOT = 'http://www.ncbi.nlm.nih.gov/entrez/eutils'
EUTIL_ROOT = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
ESEARCH    = '%s/%s' % (EUTIL_ROOT, 'esearch.fcgi')
EFETCH     = '%s/%s' % (EUTIL_ROOT, 'efetch.fcgi')

def initreqparams():
    req = {}
    req['db'] = 'pubmed'
    #req['tool'] = 'inhaler'
    req['email'] = 'raman_prasad@harvard.edu'
    req['retmax'] = '10'
    #req['retmode'] = 'xml'
    req['usehistory'] = 'y'
    #db=$db&retmax=1&usehistory=y&term=
    return req

def pubmed_esearch(search_term):
    if search_term is None:
        return
    
    params = initreqparams()
    params['term'] = search_term
        
    req = urllib2.Request(ESEARCH, urllib.urlencode(params))

    print '%s?%s' % (req.get_full_url(), urllib.urlencode(params))
    print ''
    #print dir(req)
    #return
    try:
        res = urllib2.urlopen(req)
    except HTTPError:
        return None
    except:
        return None

    xmlstr = res.read()
    print xmlstr

    open('retrieved/esearch/test.xml', 'w').write(xmlstr)
    
    
def pubmed_efetch(pmidset):
    rp = initreqparams()
    
    search_val = pmidset[0]
    print 'search val: %s' % search_val
    
    #if search_val.isdigit():
    #    rp['id'] = search_val   #','.join(pmidset)
    #else:
    #    pass
    #rp['term'] = 'Direction selectivity in the larval zebrafish tectum is mediated by asymmetric inhibition'
    #rp['TransSchema'] = 'title'
    #rp['cmd'] = 'detailssearch'
    rp['id'] = '22969706'
    print urllib.urlencode(rp)
    ESEARCH
    #req = urllib2.Request(ESEARCH, urllib.urlencode(rp))
    req = urllib2.Request(EFETCH, urllib.urlencode(rp))

    try:
        res = urllib2.urlopen(req)
    except HTTPError:
        return None
    except:
        return None

    xmlstr = res.read()
    print xmlstr
    pubmed_processor = PubMedProcessor(article_xml_str=xmlstr)
    pubmed_processor.parse_article_xml()

    for article_info in pubmed_processor.json_articles:
        print '=' * 40
        #print article_info.get_authors()
        print article_info.get_title()
        #print json.dumps(json_str, indent=4)


def test(fname):
    f = open(fname, 'r')    #'samples/abstract.txt')
    xmlstr = f.read()
    f.close()
    articles = articles_for_pubmed_efetch(xmlstr)
    for a in articles:
        print a
        
if __name__=='__main__':
    if len(sys.argv)==2:
        pubmed_esearch(sys.argv[1])
        #pubmed_efetch([sys.argv[1]])
    else:
        pubmed_efetch(['22969706'])#, '13951608'])
    

