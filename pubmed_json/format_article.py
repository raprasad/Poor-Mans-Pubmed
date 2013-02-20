import os, sys
import json
import pprint, urllib


def msg(m): print m
def dashes(): msg('-'*40)

class ArticleFormatter:
    def __init__(self, article_json):
        self.article_json = article_json
        self.title = None
        self.article_year = None
        self.pmid = None
        self.pp = pprint.PrettyPrinter(indent=4)
        
    @staticmethod
    def get_formatter_with_json_str(article_json_str):
        return ArticleFormatter(json.loads(article_json_str))
        
    @staticmethod
    def get_formatter_with_json_file(json_fname):
        content = open(json_fname, 'r').read()
        return ArticleFormatter(json.loads(content))
    
    
    def format_authors(self, authors):
        num_authors = len(authors)
        cnt = 0
        fmt_list = []
        for name_dict in authors:
            cnt += 1
            author_cite_str = '%s, %s.' % (name_dict['LastName'], name_dict['Initials'])
            if cnt > 1 and cnt==num_authors:
                fmt_list.append('and %s' % author_cite_str)
            else:
                fmt_list.append(author_cite_str)
        return ', '.join(fmt_list)
            
        
    def get_t32_citation(self, author_names=[]):
        journal_info = self.article_json.get('result')[0].get('MedlineCitation')['Article']['Journal']
        dashes()
        title = self.article_json['result'][0]['MedlineCitation']['Article']['ArticleTitle']
        if title.endswith('.'):
            title = title[:-1]
        print 'Title: [%s]' % title
        dashes()
        authors = self.article_json['result'][0]['MedlineCitation']['Article']['AuthorList']
        author_str = self.format_authors(authors)
        #for name_dict in authors:
        #    print 'Author: [%s, %s]' % (name_dict['LastName'], name_dict['Initials'])
        dashes()
        article_info = self.article_json['result'][0]['MedlineCitation']['Article']
        journal_info = article_info['Journal']
        journal_issue_info = journal_info['JournalIssue']
        self.pmid = self.article_json['result'][0]['MedlineCitation']['PMID']
        
        try:
            article_year = journal_issue_info['PubDate']['Year']
        except:
            article_year = journal_issue_info['PubDate']['MedlineDate'][:4]
            
        try:
            issue = journal_issue_info['Issue']
        except:
            issue = ''
        volume = journal_issue_info['Volume']
        print 'Year/Issue/Volume: [%s]/[%s]/[%s]' % (article_year, issue, volume)
        dashes()
        journal_iso_abbreviation = journal_info['ISOAbbreviation']
        print 'journal_iso_abbreviation: [%s]' % journal_iso_abbreviation
        dashes()
        pages = article_info['Pagination']['MedlinePgn']
        print 'pages: [%s]' % pages
        
        self.article_year = article_year
        self.title = title
        
        if issue: 
            issue = '(%s)' % issue
        else:
            issue = ''
            
        if pages:
            pages = ':%s' % pages
        else:
            pages = ''

        self.citation = '%s, %s, "%s," %s, %s%s%s.' % (author_str\
                                    , article_year\
                                    , title\
                                    , journal_iso_abbreviation\
                                    , volume\
                                    , issue\
                                    , pages)
        
        print self.citation
        
        #
        
        
        
        
        
        
        
        
if __name__=='__main__':
    from test_json import test_article
    
    af = ArticleFormatter(article_json=test_article)
    
    af.get_t32_citation()