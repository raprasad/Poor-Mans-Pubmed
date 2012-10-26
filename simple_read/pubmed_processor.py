import xmlparser
#from xml.dom import minidom #import parse, parseString
import xml_to_dict
import json

class ArticleInfo:
    def __init__(self, article_json):
        self.article_json = article_json

    def get_title(self):
        print 'get_title'
        return json.dumps(self.article_json['PubmedArticle']['MedlineCitation']['Article'], indent=4)
        return json.dumps(self.article_json['PubmedArticle']['MedlineCitation']['Article']['ArticleTitle'], indent=4)

    def get_journal(self):
        print 'get_journal'
        #print self.article_json #['PubmedArticle']    #['PubmedData'].values()
        return json.dumps(self.article_json['PubmedArticle']['MedlineCitation']['Article']['Journal']['Title'], indent=4)
        #print json.dumps(self.article_json['PubmedArticle']['MedlineCitation'], indent=4)
        
    def get_authors(self):
        print 'get_authors'
        #print self.article_json #['PubmedArticle']    #['PubmedData'].values()
        print json.dumps(self.article_json['PubmedArticle']['MedlineCitation']['Article']['AuthorList'], indent=4)

class PubMedProcessor:
    """
    Given the Pubmed XML, covert it into JSON
    """    
    def __init__(self, article_xml_str):
        self.start_tag = '<PubmedArticle>'
        self.end_tag = '</PubmedArticle>'
        self.article_xml_str = article_xml_str
        self.xml_articles = []
        self.json_articles = []
        
    def parse_article_xml(self):
        if self.article_xml_str is None:
            return

        start_idx = self.article_xml_str.find(self.start_tag)
        while start_idx > -1:
            end_idx = self.article_xml_str.find(self.end_tag, start_idx+1)
            if end_idx == -1:
                break
            article_xml_str = self.article_xml_str[start_idx:end_idx+len(self.end_tag)]
            self.xml_articles.append(article_xml_str)
            
            article_json = xml_to_dict.parse(article_xml_str)
            print json.dumps(article_json, indent=4)
            self.json_articles.append(ArticleInfo(article_json))

            start_idx = self.article_xml_str.find(self.start_tag, end_idx+len(self.end_tag))

            
        #all_data = xml_to_dict.parse(xmlstr)
        #print json.dumps(pubmed_json, indent=4)
