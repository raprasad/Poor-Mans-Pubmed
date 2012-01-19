import xmlparser, sys, traceback
from papers.models import JournalArticle, PaperAuthor, PaperStatus,\
 ResearchJournal, ArticleOrderedAuthorListing

import datetime

def data_for_node(node, field):
    fnode = node.getElements(field)
    if fnode:
        return fnode[0].getData()
    return None

def get_datenode(node):
    if not node:
        return None
    y = int(data_for_node(node[0], 'Year'))
    m = int(data_for_node(node[0], 'Month'))
    d = int(data_for_node(node[0], 'Day'))
    return datetime.date(y, m, d)

def article_for_xmlobj(xmlobj):
    def get_pmid(xmlobj):
        return xmlobj.getElements('MedlineCitation')[0].\
            getElements('PMID')[0].getData()
    def get_datecreated(xmlobj):
        try:
            node = xmlobj.getElements('MedlineCitation')[0].\
                getElements('DateCreated')
            return get_datenode(node)
        except:
            return datetime.date(1970, 1, 1)
    def get_datecompleted(xmlobj):
        node = xmlobj.getElements('MedlineCitation')[0].\
            getElements('DateCompleted')
        return get_datenode(node)
    def get_daterevised(xmlobj):
        node = xmlobj.getElements('MedlineCitation')[0].\
            getElements('DateRevised')
        return get_datenode(node)
    def get_article_node(xmlobj):
        return xmlobj.getElements('MedlineCitation')[0].\
            getElements('Article')[0]        
            
    def get_journalissue(xmlobj):
        article_node = get_article_node(xmlobj)
        journalissue_node = article_node.getElements('Journal')[0].\
            getElements('JournalIssue')[0]
        pubdate_node = journalissue_node.getElements('PubDate')[0]
        return ( data_for_node(pubdate_node, 'Year'), \
                data_for_node(pubdate_node, 'Month'), \
                data_for_node(journalissue_node, 'Issue'), \
                data_for_node(journalissue_node, 'Volume'))
            
            
    def get_abstract(xmlobj):
        article_node = get_article_node(xmlobj)
        abstract = article_node.getElements('Abstract')
        if abstract:
            return abstract[0].getElements('AbstractText')[0].getData()
        return None
        
    def get_pagination(xmlobj):
        article_node = get_article_node(xmlobj)
        pagination = ''
        try:
            pagination = article_node.getElements('Pagination')[0].\
                getElements('MedlinePgn')[0].getData()
        except Exception:
            pass
        
        return pagination
        

    def get_authors(xmlobj):
        article_node = get_article_node(xmlobj)
        authors = article_node.getElements('AuthorList')[0].\
            getElements('Author')
        data = []
        author_lst = []
        for a in authors:
            if a.getElements('CollectiveName'):
                continue
            lastname = a.getElements('LastName')[0].getData()
            #ForeName
            fname = ''
            if a.getElements('ForeName'):
                fname = a.getElements('ForeName')[0].getData()
            elif a.getElements('Initials'):
                fname = a.getElements('Initials')[0].getData()
            try:
                author_obj = PaperAuthor.objects.get(last_name=lastname, first_name=fname)
            except PaperAuthor.DoesNotExist:
                author_obj = PaperAuthor(last_name=lastname, first_name=fname)
                author_obj.save()
            #print author_obj
            author_lst.append(author_obj)
            #data.append("%s %s" % (lastname, initials))
        return author_lst
        
    def get_journal_obj(xmlobj):
        article_node = get_article_node(xmlobj)
        title = article_node.getElements('Journal')[0].getElements('Title')
        if not title:
            title = 'None'
        else:
            title = title[0].getData()
        short = xmlobj.getElements('MedlineCitation')[0].\
            getElements('MedlineJournalInfo')[0].\
            getElements('MedlineTA')[0].getData()
        try:
            rj = ResearchJournal.objects.get(name = title, description = short)
        except ResearchJournal.DoesNotExist:
            rj = ResearchJournal(name = title, description = short)
            rj.save()
        return rj
        
    def get_article_title(xmlobj):
        article_node = get_article_node(xmlobj)
        return article_node.getElements('ArticleTitle')[0].getData()[0:255]
    def get_articleidlist(xmlobj):
        return xmlobj.\
            getElements('PubmedData')[0].\
            getElements('ArticleIdList')[0].\
            getElements('ArticleId')
    def get_pmcid(xmlobj):
        artids = get_articleidlist(xmlobj)
        for aid in artids:
            idtype = aid.getAttribute('IdType') 
            if idtype and idtype == 'pmc':
                return aid.getData()
        return None
        
        
    def get_publicationstatus(xmlobj):
        pstatus = xmlobj.\
            getElements('PubmedData')[0].\
            getElements('PublicationStatus')[0].getData()
        if pstatus is None:
            pstatus = 'UNKNOWN'

        if pstatus == 'ppublish':
            pstatus = pstatus[1:]
        try: 
            p_obj = PaperStatus.objects.get(name=pstatus)
        except PaperStatus.DoesNotExist:
            p_obj = PaperStatus(name=pstatus)
            p_obj.save()
        return p_obj
        
    pmid = get_pmid(xmlobj)

    existing_articles = JournalArticle.objects.filter(pubmed_id=pmid)
    if existing_articles.count() > 0:
        return existing_articles[0]
        
    if 1:#try :
        yr, month, issue, vol = get_journalissue(xmlobj)
        # is yr, month numeric?
        
        #print yr, month, issue, vol
        #print pmid
        #print get_publicationstatus(xmlobj)
        #print get_abstract(xmlobj)
        #print 'page', get_pagination(xmlobj)
        #print 'title',  get_article_title(xmlobj)
        #print 'journal', get_journal_obj(xmlobj)
        
        article_obj =  JournalArticle(
            pubmed_id          = pmid ,
            pmc_id         = get_pmcid(xmlobj),
            status     = get_publicationstatus(xmlobj),
            abstract      = get_abstract(xmlobj),
            year_of_publication = yr,
            month_of_publication = month,
            volume = vol,
            issue = issue,
            page = get_pagination(xmlobj),
            title = get_article_title(xmlobj),
            journal = get_journal_obj(xmlobj))
            #issue         = get_journalissue(xmlobj),
            # here last!!!!
            
            #art_title     = get_article_title(xmlobj),
            #pub_title     = 
            #pagination    = get_pagination(xmlobj),
            #datecreated   = get_datecreated(xmlobj),
            #datecompleted = get_datecompleted(xmlobj),
            #daterevised   = get_daterevised(xmlobj),)
        if article_obj.abstract is not None:
            article_obj.is_abstract_public = True
            
        article_obj.save()
        author_order = 10

        for a in get_authors(xmlobj):
            ordered_author = ArticleOrderedAuthorListing(article=article_obj\
                                    , author=a\
                                    , sort_order=author_order)
            ordered_author.save()
            author_order += 10
        article_obj.save()  # automatically updates author text
        return article_obj
    #except Exception, e:
    #    print 'skipping [%s]' % pmid
    #    traceback.print_exc(file=sys.stdout)        
    #    raise e

def articles_for_pubmed_efetch(xmlstr):
    #print xmlstr
    parser = xmlparser.Xml2Obj()
    root = parser.Parse(xmlstr)
    article_set = root.getElements('PubmedArticle')
    articles = []
    for article in article_set:
        articles.append(article_for_xmlobj(article))
    return articles
'''
python manage.py shell
from pubmed.pubrun import *
test('/Users/rprasad/projects/webfaction_09/webfaction_scd/webfaction_live/scd/pubmed/samples/abstract.txt')

'''    
