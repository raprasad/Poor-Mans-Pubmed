import os, sys
import json
import pprint, urllib
from pull_article_by_pmid import pull_article_by_id

def search_by_author(author_name=" R", result_dir='losick_pubs', return_max=300):

    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)
    
    # parameters for pulling this pubmed article in JSON format
    # http://www.ncbi.nlm.nih.gov/pubmed/22969706
    #
    params = urllib.urlencode({'db': 'pubmed'\
                , 'apikey': 'c7af1b8854ea29237f164300e39edbbf'\
                , 'field': 'author'\
                , 'retmax' : return_max
                , 'term' : author_name}) 

    url_str = 'http://entrezajax.appspot.com/esearch?%s' % params
    ##EUTIL_ROOT = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
    #ESEARCH    = '%s/%s' % (EUTIL_ROOT, 'esearch.fcgi')
    #EFETCH     = '%s/%s' % (EUTIL_ROOT, 'efetch.fcgi')
    # URL to call
    # e.g. http://entrezajax.appspot.com/efetch?apikey=c7af1b8854ea29237f164300e39edbbf&db=pubmed&id=22969706
    print url_str

    # open url
    f = urllib.urlopen(url_str)

    # read in content
    pubmed_str = f.read()

    # convert to JSON
    pubmed_json = json.loads(pubmed_str)

    # print in human readable format, indent is 4 spaces
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(pubmed_json)

    print pubmed_str
    
    cnt =0 
    for pm_id in pubmed_json['result']['IdList']:
        cnt+=1
        print '(%s) %s' % (cnt, pm_id)
        fname = os.path.join(result_dir, 'json_%s.txt' % pm_id)
        if not os.path.isfile(fname):
            json_str = pull_article_by_id(pm_id)
            if json_str is not None:
                open(fname, 'w').write(json_str)
                print 'file written: %s' % fname
        else:
            print 'got it'
    
    
if __name__=='__main__':
    #search_by_author(author_name="Engert F", result_dir='engert_pubs')
    #search_by_author(author_name="Hunter CP", result_dir='hunter_pubs')
    search_by_author(author_name="Murray AW", result_dir='murray_pubs')
    #if len(sys.argv) == 2:
    #    search_by_author(sys.argv[1])
    #else:
    #    print 'python search_by_author.py [author]'