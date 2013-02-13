import os
import sys
import time
import urllib, urllib2
import io
import xml.etree.ElementTree as etree
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
    req['retmode'] = 'xml'
    req['usehistory'] = 'y'
    #db=$db&retmax=1&usehistory=y&term=
    return req

def pubmed_esearch(search_term):
    if search_term is None:
        return
    
    params = initreqparams()
    params['term'] = search_term
    params['field'] = 'title'#     '[ti]GGTI-2133%2C an inhibitor of geranylgeranyltransferase%2C inhibits infiltration of inflammatory cells into airways in mouse experimental asthma'
        
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
    if xmlstr.find('<Count>1</Count>') > -1:
        print 'GOT IT'
        fh = io.StringIO(xmlstr)
        tree = etree.parse(fh)
        root = tree.getroot()
        try:
            pubmed_id = root.findall('IdList')[0][0].text
            print 'pubmed_id', pubmed_id
            return pubmed_id
        except:
            print 'failed to find pubmed id'
            return None
        #a_file = io.StringIO(a_string)
        
    else:
        return None
    #print ''
        
    #open('retrieved/esearch/test.xml', 'w').write(xmlstr)
    
    
def pubmed_efetch(pubmed_id):
    print 'pubmed fetch for: %s' % pubmed_id
    rp = initreqparams()
    
    fname = 'retrieved/pubmed_xml/%s.xml' % pubmed_id
    if os.path.isfile(fname):
        print 'Already retrieved'
        return
    
    rp['id'] = pubmed_id
    print urllib.urlencode(rp)
    req = urllib2.Request(EFETCH, urllib.urlencode(rp))

    try:
        res = urllib2.urlopen(req)
    except HTTPError:
        return None
    except:
        return None

    xmlstr = res.read()
    print xmlstr

    
    open(fname, 'w').write(xmlstr)
    print 'file written: %s' % fname
    #pubmed_processor = PubMedProcessor(article_xml_str=xmlstr)
    #pubmed_processor.parse_article_xml()

    #for article_info in pubmed_processor.json_articles:
    #    print '=' * 40
    #print article_info.get_authors()
    #    print article_info.get_title()
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
        pubmed_efetch('22969706')#, '13951608'])
    

