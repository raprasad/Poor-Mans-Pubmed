import sys
import json
import pprint, urllib
from format_article import ArticleFormatter

def pull_article_by_id(pubmed_id):

    
    # parameters for pulling this pubmed article in JSON format
    # http://www.ncbi.nlm.nih.gov/pubmed/22969706
    #
    params = urllib.urlencode({'db': 'pubmed', 'id': pubmed_id, 'apikey': 'c7af1b8854ea29237f164300e39edbbf'}) 

    url_str = 'http://entrezajax.appspot.com/efetch?%s' % params

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

    return pubmed_str
    
    
if __name__=='__main__':
    if len(sys.argv) == 2:
        pull_article_by_id(sys.argv[1])
    else:
        print 'python pull_article_by_pmid.py [pubmed id number]'
        