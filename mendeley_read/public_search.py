import json
import sys
import urllib, urllib2
import config as mendeley_config
from json_example import json_example
import pprint

def msg(m):     print m
def dashes():    msg(40*'-')
def msgt(m):    dashes();    msg(m);    dashes()
def msgx(m, m2=None):   msgt('Error'); msg(m);  sys.exit(0)


SEARCH_BASE_URL = 'http://api.mendeley.com/oapi/documents/search'

DETAILS_BASE_URL = 'http://api.mendeley.com/oapi/documents/details/' #2c8d9cb0-6d00-11df-a2b2-0026b95e3eb7/


#http://api.mendeley.com/oapi/documents/details/10.3168%25jds.2008-1389?type=doi&consumer_key=ecb158ce2c156389a56b6a70b63057af051094ab4

def find_article_by_uuid(uuid):
    if uuid is None:
        msgx('find_article_by_uuid. uuid is None')

    detail_url = '%s/%s/?consumer_key=%s' % (DETAILS_BASE_URL\
                       , uuid\
                       , mendeley_config.MENDELEY_CONSUMER_KEY)
    
    pull_json_from_url(detail_url)

def pull_json_from_url(mendeley_api_url):
    if mendeley_api_url is None:
        msgx('pull_json_from_url. url is None')

    f = urllib2.urlopen(mendeley_api_url)
    json_response_string = f.read()
    json_response = json.loads(json_response_string)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(json_response)
    return json_response
   
def find_article_by_title(title):
    if title is None:
        msgx('find_article_by_title. err: Title is None')

    #formatted_title = urllib.quote('title:%s' % title.strip())
    
    
    title2 = 'Infliximab dose escalation vs. initiation of adalimumab for loss of response in Crohn\'s disease: a cost-effectiveness analysis'
    
    #formatted_title = urllib.quote('author:%s year:2006' % ('Korzenik'))
    formatted_title = urllib.quote('title:%s author:%s' % (title2, 'Korzenik'))
    #formatted_title = 'author:%s year:2006' % ('Korzenik')
    search_url = '%s/%s/?consumer_key=%s' % (SEARCH_BASE_URL\
                        , formatted_title\
                        , mendeley_config.MENDELEY_CONSUMER_KEY)
    msgt(search_url) 
    json_response = pull_json_from_url(search_url)
    """
    f = urllib2.urlopen(search_url)
    json_response_string = f.read()
    json_response = json.loads(json_response_string)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(json_response)
    """
    for doc in json_response.get('documents'):
        print doc.get('title', '(No title)')
    #print json_response
    #pprint(json_response)
    #print json.dumps(json_resposnse, sort_keys=True, indent=4)

def test_json():
    for doc in json_example.get('documents'):
        dashes()
        print doc.get('title', '(No title)')
        print doc.get('year', '(No year)')
        print doc.get('uuid', '(No uuid)')



if __name__=='__main__':
    #test_json()
    #sys.exit(0)
    #find_article_by_uuid('93bfbc30-6d03-11df-a2b2-0026b95e3eb7')
    #msgx('')
    if len(sys.argv) == 2:
        find_article_by_title(sys.argv[1])
    else:
        print '>python public_search.py \'title in quotes\''
        